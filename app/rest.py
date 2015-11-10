import flask_restful
from flask import request
from flask.ext.restful import abort
from flask.ext.restful import fields
from flask_login import current_user

from sqlalchemy.sql import func

from app import app
from app import db
from app.utils import scoped_session
from dbmodels import SampleTransformSpec

api = flask_restful.Api(app)


def row_to_dict(row):
    attrs = ('type_id', 'status', 'operator_id', 'date_created', 'data_json')
    return {a: getattr(row, a) for a in attrs}


class TransformSpecResource(flask_restful.Resource):
    """get / delete / patch / put a single spec"""

    def get(self, spec_id):
        """fetches a single spec"""
        with scoped_session(db.engine) as sess:
            row = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if row:
                # sess.expunge(row)
                return {row.spec_id: row_to_dict(row)}
        abort(404, message="Spec {} doesn't exist".format(spec_id))

    def delete(self, spec_id):
        """deletes a single spec"""
        with scoped_session(db.engine) as sess:
            spec = sess.query(SampleTransformSpec).filter(
                SampleTransformSpec.spec_id == spec_id).first()
            if spec:
                sess.delete(spec)
                # sess.commit()
                return '', 204
            abort(404, message="Spec {} doesn't exist".format(spec_id))

    def put(self, spec_id):
        """creates or replaces a single specific spec"""
        data_json = request.json
        with scoped_session(db.engine) as sess:
            spec = SampleTransformSpec()
            spec.spec_id = spec_id
            spec.data_json = data_json
            spec.operator_id = current_user.operator_id
            sess.add(spec)

            response_headers = {'location': api.url_for(TransformSpecResource,
                                                        spec_id=spec_id),
                                'etag': str(spec_id)}
            response = {spec_id: data_json}
            return response, 201, response_headers


class TransformSpecListResource(flask_restful.Resource):
    """get a list of all specs, and post a new spec"""

    def get(self):
        """returns a list of all specs"""
        with scoped_session(db.engine) as sess:
            rows = (sess.query(SampleTransformSpec)
                    .order_by(SampleTransformSpec.spec_id)
                    .all()
                    )
            result = [{row.spec_id: row_to_dict(row)} for row in rows]
            #for row in rows:
            #    sess.expunge(rows)
            return result
        return []

    def post(self):
        """creates new spec returning a nice geeky Location header"""
        with scoped_session(db.engine) as sess:
            spec = SampleTransformSpec()
            spec.data_json = request.json
            spec.operator_id = current_user.operator_id
            sess.add(spec)
            sess.flush()  # required to get the id from the implicit sequence

            response_headers = {'location': api.url_for(TransformSpecResource,
                                                        spec_id=spec.spec_id),
                                'etag': str(spec.spec_id)}
            response = {spec.spec_id: spec.data_json}
            return response, 201, response_headers

