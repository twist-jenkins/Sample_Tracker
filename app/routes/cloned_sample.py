######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: app/routes/cloned_sample.py
#
# These are the handlers for the cloned_sample routes used by this application.
#
######################################################################################

import csv
import json
import logging
import StringIO

from flask import g, make_response, request, Response, jsonify, abort

from sqlalchemy import and_
from sqlalchemy.orm import joinedload, subqueryload
from app.utils import scoped_session
from app.routes.spreadsheet import create_adhoc_sample_movement

from app import app, db, googlelogin

from app.dbmodels import (SampleTransfer, GeneAssemblySampleView,
                          SamplePlate, SamplePlateLayout, SamplePlateType, SampleTransferDetail, SampleTransferType)
from app.models import create_destination_plate

from well_mappings import (get_col_and_row_for_well_id_48,
                           get_well_id_for_col_and_row_48,
                           get_col_and_row_for_well_id_96,
                           get_well_id_for_col_and_row_96,
                           get_col_and_row_for_well_id_384,
                           get_well_id_for_col_and_row_384)

from app.plate_to_plate_maps import maps_json

from well_count_to_plate_type_name import well_count_to_plate_type_name




