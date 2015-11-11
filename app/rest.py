import flask_restful
from flask import request
from flask.ext.restful import abort
from flask_login import current_user

from sqlalchemy.sql import func

from app import app
from app import db
from app.utils import scoped_session
from dbmodels import SampleTransformSpec

api = flask_restful.Api(app)

from marshmallow import Schema, fields


class SpecSchema(Schema):
    spec_id = fields.Int()
    type_id = fields.Int()
    status = fields.Str()
    operator_id = fields.Str()
    date_created = fields.Date()
    data_json = fields.Dict()


spec_schema = SpecSchema()


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
                return result, 200
            abort(404, message="Spec {} doesn't exist".format(spec_id))

    def delete(self, spec_id):
        """deletes a single spec"""
        with scoped_session(db.engine) as sess:
            spec = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if spec:
                sess.delete(spec)
                return '', 204
            abort(404, message="Spec {} doesn't exist".format(spec_id))

    def put(self, spec_id):
        """creates or replaces a single specified spec"""
        with scoped_session(db.engine) as sess:
            row = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if row:
                spec = row
                # sess.expunge(row)
                #result = spec_schema.dump(row).data
                #return result, 200 # ?? updated
            else:
                spec = SampleTransformSpec()
                spec.spec_id = spec_id
            spec.data_json = request.json
            spec.operator_id = current_user.operator_id
            sess.add(spec)
            result = spec_schema.dump(spec).data
            return result, 201, self.response_headers(spec)

    @classmethod
    def response_headers(cls, spec):
        """dry"""
        return {'location': api.url_for(cls, spec_id=spec.spec_id),
                'etag': str(spec.spec_id)}


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
            print "^" * 1000
            print result
            print "^" * 1000
            #    sess.expunge(rows)
        return result, 200

    def post(self):
        """creates new spec returning a nice geeky Location header"""
        with scoped_session(db.engine) as sess:
            spec = SampleTransformSpec()
            spec.data_json = request.json
            spec.operator_id = current_user.operator_id
            sess.add(spec)
            sess.flush()  # required to get the id from the database sequence
            result = spec_schema.dump(spec).data
            return result, 201, TransformSpecResource.response_headers(spec)

