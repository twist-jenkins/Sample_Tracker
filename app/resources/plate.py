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
from app import db, constants, miseq
from app.utils import scoped_session
from app.dbmodels import NGS_BARCODE_PLATE, barcode_sequence_to_barcode_sample
from app.routes.spreadsheet import create_adhoc_sample_movement

from twistdb.sampletrack import Sample, Transfer, Plate

api = flask_restful.Api(app)

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
        logger.debug('@@ create_or_replace')
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
        # TODO:
        # sess.expunge(row)
        # result = plate_schema.dump(row).data
        # return result, 200 # ?? updated


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
            #    sess.expunge(rows)
            # print "^" * 10000
            # print str(result)
        return json_api_success(result, 200)  # FIXME
        # return result, 200

    def post(self):
        """creates new plate returning a nice geeky Location header"""
        return PlateResource.create_or_replace('POST')

