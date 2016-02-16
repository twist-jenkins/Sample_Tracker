"""Define REST resources for CRUD on samples."""

import json
import logging
from datetime import datetime

import flask_restful
from flask import request
from flask.ext.restful import abort
from flask_login import current_user

from marshmallow import Schema, fields

from app import app
from app import db, constants
from app.utils import scoped_session, json_api_success

from twistdb.sampletrack import Plate, Sample

api = flask_restful.Api(app)


class SampleSchema(Schema):
    id = fields.Str()
    plate_id = fields.Str()
    plate_well_code = fields.Int()
    order_item_id = fields.Str()
    parent_sample_id = fields.Str()
    root_sample_id = fields.Str()
    type_id = fields.Str()
    operator_id = fields.Str()
    vector_id = fields.Str()
    cloning_process_id = fields.Str()
    date_created = fields.Date()


sample_schema = SampleSchema()


class SampleResource(flask_restful.Resource):
    """get / delete / put a single sample"""

    def get(self, sample_id):
        """fetches a single sample"""
        with scoped_session(db.engine) as sess:
            sample = sess.query(Sample).filter(
                Sample.id == sample_id).first()
            if not sample:
                abort(404, message="sample {} doesn't exist".format(sample_id))
            data = sample_schema.dump(sample).data
            return json_api_success(data, 200)

    def delete(self, sample_id):
        """deletes a single sample"""
        raise NotImplementedError

    def put(self, sample_id):
        """creates or replaces a single sampleified sample"""
        raise NotImplementedError

    @classmethod
    def response_201_headers(cls, sample):
        """dry"""
        return {'location': api.url_for(cls, sample_id=sample.sample_id),
                'etag': str(sample.sample_id)}

    @classmethod
    def create_or_replace(cls, method, sample_id=None):
        """ Functionality common to POST and PUT.
            POST: create new, unknown id
            PUT: create new, known id, OR, replace existing, known id
        """
        raise NotImplementedError
        with scoped_session(db.engine) as sess:
            if method == 'POST':
                assert sample_id is None
                sample = Sample()            # create new, unknown id
                sample.operator_id = current_user.operator_id

                sess.add(sample)
                sess.flush()  # required to get the id from the database sequence
                result = sample_schema.dump(sample).data
                return json_api_success(result, 201,
                                        cls.response_201_headers(sample))
            elif method == 'PUT':
                assert sample_id is not None

                row = sess.query(Sample).filter(
                    Sample.sample_id == sample_id).first()
                if row:
                    sample = row            # replace existing, known id
                else:
                    sample = Sample()        # create new, known id
                    sample.sample_id = sample_id

                sample.operator_id = current_user.operator_id

                sess.add(sample)
                result = sample_schema.dump(sample).data
                return json_api_success(result, 201,
                                        cls.response_headers(sample))
            else:
                raise ValueError(method, sample_id)


class SampleListResource(flask_restful.Resource):
    """get a list of all samples, and post a new sample"""

    def get(self):
        """returns a list of all samples"""
        result = []
        with scoped_session(db.engine) as sess:
            rows = (sess.query(Sample)
                    .order_by(Sample.sample_id.desc())
                    .all()
                    )
            result = sample_schema.dump(rows, many=True).data
        return json_api_success(result, 200)  # FIXME

    def post(self):
        """creates new sample returning a nice geeky Location header"""
        raise NotImplementedError
        return SampleResource.create_or_replace('POST')

