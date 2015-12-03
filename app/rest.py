import json
import logging
from datetime import datetime

import flask_restful
from flask import request
from flask.ext.restful import abort
from flask_login import current_user

from sqlalchemy.sql import func

from app import app
from app import db
from app.utils import scoped_session
from dbmodels import SampleTransformSpec, SampleTransfer, NGS_BARCODE_PLATE
from dbmodels import NGSPreppedSample, NGSBarcodePair, create_unique_object_id
from dbmodels import barcode_sequence_to_barcode_sample
from app.routes.spreadsheet import create_adhoc_sample_movement
from app import miseq

api = flask_restful.Api(app)

from marshmallow import Schema, fields


class SpecSchema(Schema):
    spec_id = fields.Int()
    type_id = fields.Int()
    status = fields.Str()
    operator_id = fields.Str()
    date_created = fields.Date()
    date_executed = fields.Date()
    data_json = fields.Dict()


spec_schema = SpecSchema()


def json_api_success(data, status_code, headers=None):
    json_api_response = {"data": data,
                         "errors": [],
                         "meta": {}
                         }
    if headers is None:
        return json_api_response, status_code
    else:
        return json_api_response, status_code, headers

"""
TODO:
def json_api_error(err_list, status_code, headers=None):
    json_api_response = {"data": {},
                         "errors": err_list,
                         "meta": {}
                         }
    if headers is None:
        return json_api_response, status_code
    else:
        return json_api_response, status_code, headers
"""


def formatted(db_session, data, fmt, spec):
    if fmt == 'miseq.csv':
        nps_ids = [el["source_sample_id"]
                   for el in data["data_json"]["operations"]]
        csv = miseq.miseq_csv_for_nps(db_session, nps_ids)
        if csv:
            return csv
        else:
            abort(404, message="Could not create miseq csv")
    if fmt == 'echo.csv':
        operations = data["data_json"]["operations"]
        csv = miseq.echo_csv_for_nps(operations)
        if csv:
            return csv
        else:
            abort(404, message="Could not create echo csv")
    elif fmt == 'execute':
        # egregious hack, the client is supposed to PUT the spec
        # with header Execution:Immediate, instead here we allow
        # the client to GET the spec with format = 'execute'...
        cls = TransformSpecResource
        cls.execute(db_session, spec)
        db_session.add(spec)
        result = spec_schema.dump(spec).data
        return json_api_success(result, 200)
    elif fmt == 'json':
        return json_api_success(data, 200)
    else:
        abort(404, message="Invalid format {}".format(fmt))


class TransformSpecResource(flask_restful.Resource):
    """get / delete / put a single spec"""

    def get(self, spec_id):
        """fetches a single spec"""
        fmt = 'json'
        if '.' in spec_id:
            tokens = spec_id.split('.')
            spec_id = tokens[0]
            fmt = '.'.join(tokens[1:])
        with scoped_session(db.engine) as sess:
            spec = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if spec:
                data = spec_schema.dump(spec).data
                # sess.expunge(row)
                return formatted(sess, data, fmt, spec)
            abort(404, message="Spec {} doesn't exist".format(spec_id))

    def delete(self, spec_id):
        """deletes a single spec"""
        with scoped_session(db.engine) as sess:
            spec = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if spec:
                transfer = sess.query(SampleTransfer).filter(
                    SampleTransfer.sample_transform_spec_id == spec_id).first()
                if transfer:
                    transfer.sample_transform_spec_id = None
                    sess.flush()
                sess.delete(spec)
                sess.flush()
                return json_api_success('', 204)
            abort(404, message="Spec {} doesn't exist".format(spec_id))

    def put(self, spec_id):
        """creates or replaces a single specified spec"""
        return self.create_or_replace('PUT', spec_id)

    @classmethod
    def response_headers(cls, spec):
        """dry"""
        return {'location': api.url_for(cls, spec_id=spec.spec_id),
                'etag': str(spec.spec_id)}

    @classmethod
    def create_or_replace(cls, method, spec_id=None):
        with scoped_session(db.engine) as sess:
            execution = request.headers.get('Transform-Execution')
            immediate = (execution == "Immediate")

            if method == 'POST':
                assert spec_id is None
                spec = SampleTransformSpec()         # create new, unknown id
                assert "plan" in request.json
                spec.data_json = request.json["plan"]
                spec.operator_id = current_user.operator_id

                # workaround for poor input marshaling
                if type(spec.data_json) in (str, unicode):
                    spec.data_json = json.loads(spec.data_json)

                if modify_before_insert(sess, spec):
                    # HACK FOR NGS BARCODING
                    # FIXME: the client should not set execution: immediate
                    # for this case
                    immediate = False

                if immediate:
                    cls.execute(sess, spec)
                sess.add(spec)
                sess.flush()  # required to get the id from the database sequence
                result = spec_schema.dump(spec).data
                return json_api_success(result, 201,
                                        cls.response_headers(spec))
            elif method == 'PUT':
                assert spec_id is not None

                # create or replace known spec_id
                row = sess.query(SampleTransformSpec).filter(
                    SampleTransformSpec.spec_id == spec_id).first()
                if row:
                    spec = row                    # replace existing, known id
                else:
                    spec = SampleTransformSpec()        # create new, known id
                    spec.spec_id = spec_id

                if request.json and request.json["plan"]:
                    spec.data_json = request.json["plan"]

                # workaround for poor input marshaling
                if type(spec.data_json) in (str, unicode):
                    spec.data_json = json.loads(spec.data_json)

                spec.operator_id = current_user.operator_id
                # TODO: allow execution operator_id != creation operator_id
                if immediate:
                    cls.execute(sess, spec)

                sess.add(spec)
                result = spec_schema.dump(spec).data
                return json_api_success(result, 201,
                                        cls.response_headers(spec))
            else:
                raise ValueError(method, spec_id)
        # TODO:
        # sess.expunge(row)
        # result = spec_schema.dump(row).data
        # return result, 200 # ?? updated

    @classmethod
    def execute(cls, sess, spec):
        if not spec.data_json:
            raise KeyError("spec.data_json is null or empty")
        details = spec.data_json["details"]
        try:
            transfer_type_id = details["transfer_type_id"]
        except:
            transfer_type_id = details["id"]  # FIXME: REMOVE SHIM
        transfer_template_id = details["transfer_template_id"]
        operations = spec.data_json["operations"]
        wells = operations  # (??)
        result = create_adhoc_sample_movement(sess,
                                              transfer_type_id,
                                              transfer_template_id,
                                              wells,
                                              transform_spec_id=spec.spec_id)
        if not result:
            raise ValueError("create_adhoc_sample_movement returned nothing")
        if not result["success"]:
            abort(400, message="Failed to execute step (sample_movement)")
        spec.date_executed = datetime.utcnow()
        spec.operator_id = current_user.operator_id
        # TODO: allow execution operator_id != creation operator_id


class TransformSpecListResource(flask_restful.Resource):
    """get a list of all specs, and post a new spec"""

    def get(self):
        """returns a list of all specs"""
        result = []
        with scoped_session(db.engine) as sess:
            rows = (sess.query(SampleTransformSpec)
                    .order_by(SampleTransformSpec.spec_id.desc())
                    .all()
                    )
            result = spec_schema.dump(rows, many=True).data
            #    sess.expunge(rows)
            #print "^" * 10000
            #print str(result)
        return json_api_success(result, 200)  # FIXME
        # return result, 200

    def post(self):
        """creates new spec returning a nice geeky Location header"""
        return TransformSpecResource.create_or_replace('POST')


def modify_before_insert(db_session, spec):
    # Hack for ngs barcoding.
    # Client currently sends the plate to be barcoded as the source_plate
    # until it sends that plate as the destination plate, backend
    # needs to rejigger the transform spec to make sense.
    # Similar thing might be needed for primer hitpicking etc.

    if "details" not in spec.data_json:
        return False

    # if not "ngs barcoding" step, do nothing
    details = spec.data_json["details"]
    if "transfer_type_id" in details:
        if details["transfer_type_id"] != 26:
            return False

    operations = spec.data_json["operations"]
    new_operations = []
    for oper in operations:
        """ assumes oper looks like {
                "source_plate_barcode":"SRN 000577 SM-37",
                "source_well_name":"K13",
                "source_sample_id":"CS_563fd11f785b1a7dd06dc817",
                "destination_plate_barcode":"SRN 000577 SM-37",
                "destination_well_name":"K13",
                "destination_plate_well_count":384
            }
        """
        source_sample_id = oper["source_sample_id"]
        destination_well_id = oper["destination_well_name"]  # goes into notes
        nps_id, ngs_pair = make_ngs_prepped_sample(db_session,
                                                   source_sample_id,
                                                   destination_well_id)

        i7_rowcol = "%s%d" % (ngs_pair.reverse_primer_i7_well_row,
                              ngs_pair.reverse_primer_i7_well_column)
        i7_oper = oper.copy()
        i7_oper["source_plate_barcode"] = NGS_BARCODE_PLATE
        i7_oper["source_well_name"] = i7_rowcol
        i7_oper["source_sample_id"] = barcode_sequence_to_barcode_sample(ngs_pair.i7_sequence_id)
        i7_oper["source_plate_well_count"] = 384
        i7_oper["destination_sample_id"] = nps_id
        new_operations.append(i7_oper)

        i5_rowcol = "%s%d" % (ngs_pair.forward_primer_i5_well_row,
                              ngs_pair.forward_primer_i5_well_column)
        i5_oper = oper.copy()
        i5_oper["source_plate_barcode"] = NGS_BARCODE_PLATE
        i5_oper["source_well_name"] = i5_rowcol
        i5_oper["source_sample_id"] = barcode_sequence_to_barcode_sample(ngs_pair.i5_sequence_id)
        i5_oper["source_plate_well_count"] = 384
        i5_oper["destination_sample_id"] = nps_id
        new_operations.append(i5_oper)

    spec.data_json["operations"] = new_operations
    spec.data_json["destinations"] = spec.data_json["sources"]
    spec.data_json["sources"] = [{
        "id": None,
        "type": "plate",
        "details": {
            "text": "NGS barcoding source plate",
            "id": NGS_BARCODE_PLATE,
        }
    }]
    return True


def make_ngs_prepped_sample(db_session, source_sample_id,
                            destination_well_id):
    operator = current_user

    # Grab next pair of barcodes
    ngs_pair = None
    tries_remaining = 1000
    while not ngs_pair and tries_remaining > 0:
        tries_remaining -= 1
        next_index_sql = db.Sequence('ngs_barcode_pair_index_seq')
        if not next_index_sql:
            raise KeyError("sequence ngs_barcode_pair_index_seq is missing")
        ngs_barcode_pair_index = db_session.execute(next_index_sql)
        ngs_pair = (db.session.query(NGSBarcodePair)
                    .filter_by(pk=ngs_barcode_pair_index)
                    .first())
    if not ngs_pair:
        raise KeyError("ngs_barcode_pair_index %s not found"
                       % ngs_barcode_pair_index)

    # Create NPS
    nps_id = create_unique_object_id("NPS_")
    description = 'SMT stub descr.'  # e.g. "RCA 16 hours  Gene 12 Clone 2"
    notes = 'SMT - well %s' % destination_well_id  # e.g. "" for alpha NPSs
    insert_size_expected = -1
    parent_process_id = None  # e.g. 'SPP_0008' for alpha NPSs
    external_barcode = None
    reagent_type_set_lot_id = None  # e.g. 'RTSL_5453e163e208466dd26d3aa4'
    status = None
    parent_transfer_process_id = None
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nps_sample = NGSPreppedSample(nps_id, source_sample_id,
                                  description,
                                  ngs_pair.i5_sequence_id,
                                  ngs_pair.i7_sequence_id,
                                  notes,
                                  insert_size_expected,
                                  date_created,
                                  operator.operator_id,
                                  parent_process_id,
                                  external_barcode,
                                  reagent_type_set_lot_id,
                                  status,
                                  parent_transfer_process_id)

    logging.debug('NPS_ID %s for %s assigned [%s, %s]',
                  nps_id, source_sample_id,
                  ngs_pair.i5_sequence_id,
                  ngs_pair.i7_sequence_id)

    db_session.add(nps_sample)
    db_session.flush()

    return nps_id, ngs_pair
