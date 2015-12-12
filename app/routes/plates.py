import json
import logging
from datetime import datetime

import flask_restful
from flask import request
from flask.ext.restful import abort
from flask_login import current_user

from sqlalchemy.sql import func

from app import db
from app.utils import scoped_session
from app.dbmodels import PlatePriorStepView
from app.rest import json_api_success

from marshmallow import Schema, fields


class PlateInfoSchema(Schema):
    externalBarcode = fields.Str(attribute="external_barcode")


plate_info_schema = PlateInfoSchema()


class PlateListResource(flask_restful.Resource):
    """get a list of all specs, and post a new spec"""

    def get(self):
        """Returns a list of all plates ready for step N.
        We might refactor some of the other plate-centric queries
        (e.g. search by barcode) into here when we get a chance."""
        step_id = request.args.get('ready_for_step')
        if step_id is not None:
            return self.plates_ready_for_step(step_id)
        raise NotImplementedError

    def plates_ready_for_step(self, step_id):
        result = []
        with scoped_session(db.engine) as sess:
            view = PlatePriorStepView
            qry = (
                sess.query(view)
                .filter(view.prior_transfer_type_id == step_id)
                .order_by(view.external_barcode)
            )
            rows = qry.all()
            result = plate_info_schema.dump(rows, many=True).data
        return json_api_success(result, 200)  # FIXME
