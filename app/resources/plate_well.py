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

from twistdb.sampletrack import Sample, Plate, PlateWell

from app.resources.sample import sample_schema

api = flask_restful.Api(app)

class PlateWellResource(flask_restful.Resource):
    """get a single sample from a well on a plate"""

    def get(self, plate_barcode, well_number):
        """fetches the HEAD sample 'commit' for a given plate & well"""
        with scoped_session(db.engine) as sess:
            sample = (sess.query(Sample)
                      .join(Plate)
                      .join(PlateWell, Sample.well)
                      .filter(Plate.external_barcode == plate_barcode,
                              PlateWell.well_number == well_number)
                      .order_by(Sample.date_created.desc())  # most recent
                      .first())
            if not sample:
                abort(404, message="plate {} well {} doesn't exist"
                                   .format(plate_barcode, well_number))
            data = sample_schema.dump(sample).data
            return json_api_success(data, 200)
