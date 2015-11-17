from datetime import datetime
import json

import flask_restful
from flask import request
from flask.ext.restful import abort
from flask_login import current_user

from sqlalchemy.sql import func

from app import app
from app import db
from app.utils import scoped_session
from dbmodels import SampleTransformSpec, SampleTransfer
from app.routes.spreadsheet import create_adhoc_sample_movement

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


class TransformSpecResource(flask_restful.Resource):
    """get / delete / put a single spec"""

    def get(self, spec_id):
        """fetches a single spec"""
        with scoped_session(db.engine) as sess:
            row = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if row:
                # sess.expunge(row)
                result = spec_schema.dump(row).data
                return json_api_success(result, 200)
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

    def put(self, spec_id, action=None):
        """creates or replaces a single specified spec"""
        return self.create_or_replace('PUT', spec_id, action)

    @classmethod
    def response_headers(cls, spec):
        """dry"""
        return {'location': api.url_for(cls, spec_id=spec.spec_id),
                'etag': str(spec.spec_id)}

    @classmethod
    def create_or_replace(cls, method, spec_id=None, action=None):
        with scoped_session(db.engine) as sess:
            execution = request.headers.get('Transform-Execution')
            immediate = (execution == "Immediate")
            if method == 'POST':
                assert spec_id is None
                spec = SampleTransformSpec()         # create new, unknown id
                assert "plan" in request.json
                spec.data_json = request.json["plan"]
                spec.operator_id = current_user.operator_id
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
                if immediate:
                    cls.execute(sess, spec)
                spec.operator_id = current_user.operator_id
                # TODO: set execution operator != creation operator
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
        if type(spec.data_json) in (str, unicode):
            spec.data_json = json.loads(spec.data_json)
        details = spec.data_json["details"]
        try:
            transfer_type_id = details["transfer_type_id"]
        except:
            transfer_type_id = details["id"]  # REMOVE
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
        spec.date_executed = datetime.utcnow()


class TransformSpecListResource(flask_restful.Resource):
    """get a list of all specs, and post a new spec"""

    def get(self):
        """returns a list of all specs"""
        result = []
        with scoped_session(db.engine) as sess:
            rows = (sess.query(SampleTransformSpec)
                    .order_by(SampleTransformSpec.spec_id)
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

