"""Define REST resources for CRUD on transform specs."""

import json
import logging
from datetime import datetime

import flask_restful
from flask import request, g
from flask.ext.restful import abort
from flask_login import current_user

from marshmallow import Schema, fields

from app import api
from app import db, constants, miseq
from app.utils import scoped_session
from app.dbmodels import NGS_BARCODE_PLATE, barcode_sequence_to_barcode_sample
from app.routes.spreadsheet import create_adhoc_sample_movement

from twistdb.sampletrack import Sample, TransformSpec, Transform, Plate, PlateType

logger = logging.getLogger()


def json_api_success(data, status_code, headers=None):
    json_api_response = {"data": data,
                         "errors": [],
                         "meta": {}
                         }
    if headers is None:
        return json_api_response, status_code
    else:
        return json_api_response, status_code, headers

# TODO:
# def json_api_error(err_list, status_code, headers=None):
#     json_api_response = {"data": {},
#                          "errors": err_list,
#                          "meta": {}
#                          }
#     if headers is None:
#         return json_api_response, status_code
#     else:
#         return json_api_response, status_code, headers


def formatted(db_session, data, fmt, spec):
    if fmt in ('miseq.csv', 'sample_map.xlsx'):
        nps_ids = [el["source_sample_id"]
                   for el in data["data_json"]["operations"]]
        rows = miseq.nps_id_details(db_session, nps_ids)

        if fmt == 'miseq.csv':
            return miseq.miseq_csv_response(rows)
        elif fmt == 'sample_map.xlsx':
            return miseq.sample_map_response(rows)
        else:
            raise ValueError(fmt)
    elif fmt == 'echo.csv':
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


class SpecSchema(Schema):
    spec_id = fields.Int()
    type_id = fields.Int()
    status = fields.Str()
    operator_id = fields.Str()
    date_created = fields.Date()
    date_executed = fields.Date()
    data_json = fields.Dict()


spec_schema = SpecSchema()


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
            spec = sess.query(TransformSpec).filter(
                TransformSpec.spec_id == spec_id).first()
            if spec:
                data = spec_schema.dump(spec).data
                # sess.expunge(row)
                return formatted(sess, data, fmt, spec)
            abort(404, message="Spec {} doesn't exist".format(spec_id))

    def delete(self, spec_id):
        """deletes a single spec"""
        with scoped_session(db.engine) as sess:
            spec = sess.query(TransformSpec).filter(
                TransformSpec.spec_id == spec_id).first()
            if spec:
                transform = sess.query(Transform).filter(
                    Transform.transform_spec_id == spec_id).first()
                if transform:
                    transform.transform_spec_id = None
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

        def perform_common_operations(sess, spec, plan_required):
            """operations common to PUT and POST"""

            # load the json data
            j = request.json
            if plan_required:
                spec.data_json = j["plan"]
            else:
                if j and j["plan"]:
                    spec.data_json = j["plan"]
            # workaround for poor input marshaling
            if type(spec.data_json) in (str, unicode):
                spec.data_json = json.loads(spec.data_json)

            # set some basic spec metadata
            spec.type_id = (spec.data_json.get('details', {})
                            .get('transform_type_id'))
            spec.operator_id = current_user.operator_id

            # perform addnl operations for certain transform_template_id values
            if modify_before_insert(sess, spec):
                # HACK FOR NGS BARCODING
                # FIXME: the client should not set execution: immediate
                # for this case
                immediate = False
            if 'details' in spec.data_json \
               and 'transform_template_id' in spec.data_json['details']:
                if spec.data_json['details']['transform_template_id'] == 32:
                    from ..worklist.hamilton import miniprep_hitpicking
                    csv = miniprep_hitpicking(sess, spec)
                    spec.data_json['details']['worklist'] = {"content": csv}

            # now execute the spec
            execution = request.headers.get('Transform-Execution')
            immediate = (execution == "Immediate")
            # TODO: allow execution operator_id != creation operator_id
            if immediate:
                cls.execute(sess, spec)
            sess.add(spec)

        with scoped_session(db.engine) as sess:

            if method == 'POST':
                # create new, unknown id
                assert spec_id is None
                spec = TransformSpec()
                perform_common_operations(sess, spec, plan_required=True)
                sess.flush()  # required (?) to get the id from the database sequence

            elif method == 'PUT':
                # create or replace known spec_id
                assert spec_id is not None
                row = sess.query(TransformSpec).filter(
                    TransformSpec.spec_id == spec_id).first()
                if row:
                    spec = row                    # replace existing, known id
                else:
                    spec = TransformSpec()        # create new, known id
                    spec.spec_id = spec_id
                perform_common_operations(sess, spec, plan_required=False)

            else:
                raise ValueError(method, spec_id)

            result = spec_schema.dump(spec).data
            return json_api_success(result, 201,
                                    cls.response_headers(spec))

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
            transform_type_id = details["transform_type_id"]
        except:
            transform_type_id = details["id"]  # FIXME: REMOVE SHIM
        transform_template_id = details["transform_template_id"]
        operations = spec.data_json["operations"]
        wells = operations  # (??)

        if 'requestedData' in spec.data_json['details'] \
           and transform_type_id in (constants.TRANS_TYPE_UPLOAD_QUANT,
                                     constants.TRANS_TYPE_ECR_PCR_PLANNING,
                                     constants.TRANS_TYPE_PCA_PREPLANNING, ):
            if transform_type_id == constants.TRANS_TYPE_UPLOAD_QUANT:
                aliquot_plate = spec.data_json['operations'][0]['source_plate_barcode']
                quant_data = spec.data_json['details']['requestedData']['instrument_data']
                result = store_quant_data(sess, aliquot_plate, quant_data)
                if not result["success"]:
                    abort(400, message="Failed to execute step (sample_movement) -- store_quant_data failed")

            else:
                """
                this 'spec' really just binds the bulk plate barcode to the destination plates

                FIXME: this used to be necessary, but now the spec is saved by create_or_replace
                """

                #ts = TransformSpec( type_id=transform_type_id,
                #                    operator_id=current_user.operator_id,
                #                    data_json=spec.data_json )
                #db.session.add(ts)
                #db.session.commit()

        else:
            result = create_adhoc_sample_movement(sess,
                                                  transform_type_id,
                                                  transform_template_id,
                                                  wells,
                                                  transform_spec_id=spec.spec_id)
            if not result:
                abort(400, message="Failed to execute step (sample_movement) -- create_adhoc_sample_movement returned nothing")

        spec.date_executed = datetime.utcnow()
        spec.operator_id = current_user.operator_id
        # TODO: allow execution operator_id != creation operator_id


class TransformSpecListResource(flask_restful.Resource):
    """get a list of all specs, and post a new spec"""

    def get(self):
        """returns a list of all specs"""
        result = []
        with scoped_session(db.engine) as sess:
            rows = (sess.query(TransformSpec)
                    .order_by(TransformSpec.spec_id.desc())
                    .all()
                    )
            result = spec_schema.dump(rows, many=True).data
            reduce_data_size(result)
            #    sess.expunge(rows)
            # print "^" * 10000
            # print str(result)
        return json_api_success(result, 200)  # FIXME
        # return result, 200

    def post(self):
        """creates new spec returning a nice geeky Location header"""
        return TransformSpecResource.create_or_replace('POST')


def reduce_data_size(spec_list):
    for spec in spec_list:
        if "data_json" in spec:
            data = spec["data_json"]
            if "operations" in data:
                data["operations"] = []


def modify_before_insert(db_session, spec):
    # Hack for ngs barcoding.
    # Client currently sends the plate to be barcoded as the source_plate
    # until it sends that plate as the destination plate, backend
    # needs to rejigger the transform spec to make sense.
    # Similar thing might be needed for primer hitpicking etc.

    if "details" not in spec.data_json:
        return False

    # if not "ngs barcoding" or one of the hamilton worklist steps, do nothing
    details = spec.data_json["details"]
    if "transform_type_id" in details:
        if details["transform_type_id"] not in (
                constants.TRANS_TYPE_NGS_INDEX_HITPICKING,
                constants.TRANS_TYPE_POST_PCA_NORM):
            return False

    if details["transform_type_id"] == constants.TRANS_TYPE_NGS_INDEX_HITPICKING:
        res = alter_spec_ngs_barcodes(db_session, spec)
    elif details["transform_type_id"] == constants.TRANS_TYPE_POST_PCA_NORM:
        res = alter_spec_post_pca_hamilton_worklist(db_session, spec)

    return res


def alter_spec_post_pca_hamilton_worklist(db_session, spec):
    """Inject a Hamilton worklist for post-PCA normalization."""
    from app.worklist import hamilton
    spec.data_json['details']['worklist'] = {}
    spec.data_json['details']['worklist']['filename'] = "Test!"  # For the UI

    plate_id = spec.data_json['sources'][0]['details']['id']
    worklist = hamilton.post_pca_normalization_worklist(db_session, plate_id)
    spec.data_json['details']['worklist']['content'] = worklist

    return True


def alter_spec_ngs_barcodes(db_session, spec):
    """Inject NGS-specific info into the POSTed transform spec.
    This needs to happen as the spec is saved, but beore the spec is executed.
    """

    # TODO: figure out how to allow multiple ngs barcode plates
    # while still keeping all barcode pairs in a single NGSBarcodePair table

    # sources = spec.data_json["sources"]

    destinations = spec.data_json["destinations"]

    destination_barcodes = [dest["details"]["id"] for dest in destinations]

    operations = []
    for dest_plate_barcode in destination_barcodes:
        try:
            destination_plate = db_session.query(Plate).\
                filter(Plate.external_barcode == dest_plate_barcode).one()
        except:
            logging.warn("%s encountered error preparing NGS transform spec. "
                         "There is no plate with the barcode: [%s]",
                         g.user.first_and_last_name, dest_plate_barcode)

        for sample in destination_plate.current_well_contents(db_session):

            ngs_pair = miseq.next_ngs_pair(db_session)

            for (row, column, seq_id) in [
                (ngs_pair.reverse_primer_i7_well_row,
                 ngs_pair.reverse_primer_i7_well_column,
                 ngs_pair.i7_sequence_id),
                (ngs_pair.forward_primer_i5_well_row,
                 ngs_pair.forward_primer_i5_well_column,
                 ngs_pair.i5_sequence_id)
            ]:
                new_oper = {}
                new_oper["source_plate_barcode"] = NGS_BARCODE_PLATE
                new_oper["source_well_name"] = "%s%d" % (row, column)
                new_oper["source_sample_id"] = barcode_sequence_to_barcode_sample(seq_id)
                new_oper["source_plate_well_count"] = 384
                new_oper["destination_plate_barcode"] = dest_plate_barcode
                new_oper["destination_plate_well_count"] = 384
                # destination_sample_id is accessioned during execution
                new_oper["destination_plate_type"] = destination_plate.type_id
                new_oper["destination_well_number"] = sample.well.well_number
                new_oper["destination_well_name"] = sample.well.well_label
                operations.append(new_oper)
                logging.debug("alter_spec operX : %s", new_oper)

    spec.data_json["operations"] = operations

    # TODO: determine whether we still want / need the "sources" to
    # look like this:
    spec.data_json["sources"] = [{
        "id": None,
        "type": "plate",
        "details": {
            "text": "NGS barcoding source plate",
            "id": NGS_BARCODE_PLATE,
        }
    }]
    return True


def store_quant_data(db, plate_id, quant_str):
    """Associated quant data from an uploaded file with an aliquot plate."""
    from app.parser import spectramax

    try:
        plate = db.query(Plate).\
            filter(Plate.external_barcode == plate_id).one()
    except:
        logger.error("Failed to find plate %s" % plate_id)

    for conc in spectramax.parse(quant_str):
        well = plate.get_well_by_number(conc[0])

        # Get the latest Sample in this plate/well
        curr_s = db.query(Sample).filter(
            Sample.plate == plate,
            Sample.well == well
        ).order_by(Sample.date_created.desc()).first()

        if curr_s:
            curr_s.conc_ng_ul = conc[2]
            # Store concentration for now to all parent samples
            # FIXME this is DUMB for blended samples; we should ideally here
            # check to see which parent came from whatever transfer ID is
            # from the aliquot for quant step but who has the time for that?!?
            for psample in curr_s.parents:
                psample.conc_ng_ul = conc[2]

    logger.info("Flushing updates for parsed concentration data")
    db.flush()

    return {'success': True}  # caller is expecting this
