"""Define REST resources for CRUD on plates."""

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

from twistdb.sampletrack import Sample, Plate

api = flask_restful.Api(app)


class PlateSchema(Schema):
    plate_id = fields.Int()
    type_id = fields.Int()
    status = fields.Str()
    operator_id = fields.Str()
    date_created = fields.Date()
    date_executed = fields.Date()


plate_schema = PlateSchema()


class PlateResource(flask_restful.Resource):
    """get / delete / put a single plate"""

    def get(self, plate_id):
        """fetches a single plate"""
        with scoped_session(db.engine) as sess:
            plate = sess.query(Plate).filter(
                Plate.plate_id == plate_id).first()
            if not plate:
                abort(404, message="plate {} doesn't exist".format(plate_id))
            data = plate_schema.dump(plate).data
            return data

    def delete(self, plate_id):
        """deletes a single plate"""
        raise NotImplementedError

    def put(self, plate_id):
        """creates or replaces a single plateified plate"""
        raise NotImplementedError

    @classmethod
    def response_201_headers(cls, plate):
        """dry"""
        return {'location': api.url_for(cls, plate_id=plate.plate_id),
                'etag': str(plate.plate_id)}

    @classmethod
    def create_or_replace(cls, method, plate_id=None):
        """ Functionality common to POST and PUT.
            POST: create new, unknown id
            PUT: create new, known id, OR, replace existing, known id
        """
        with scoped_session(db.engine) as sess:
            if method == 'POST':
                assert plate_id is None
                plate = Plate()            # create new, unknown id
                plate.operator_id = current_user.operator_id

                sess.add(plate)
                sess.flush()  # required to get the id from the database sequence
                result = plate_schema.dump(plate).data
                return json_api_success(result, 201,
                                        cls.response_201_headers(plate))
            elif method == 'PUT':
                assert plate_id is not None

                row = sess.query(Plate).filter(
                    Plate.plate_id == plate_id).first()
                if row:
                    plate = row            # replace existing, known id
                else:
                    plate = Plate()        # create new, known id
                    plate.plate_id = plate_id

                plate.operator_id = current_user.operator_id

                sess.add(plate)
                result = plate_schema.dump(plate).data
                return json_api_success(result, 201,
                                        cls.response_headers(plate))
            else:
                raise ValueError(method, plate_id)


class PlateListResource(flask_restful.Resource):
    """get a list of all plates, and post a new plate"""

    def get(self):
        """returns a list of all plates"""
        result = []
        with scoped_session(db.engine) as sess:
            rows = (sess.query(Plate)
                    .order_by(Plate.plate_id.desc())
                    .all()
                    )
            result = plate_schema.dump(rows, many=True).data
        return json_api_success(result, 200)  # FIXME

    def post(self):
        """creates new plate returning a nice geeky Location header"""
        return PlateResource.create_or_replace('POST')

