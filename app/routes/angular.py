######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: app/routes/api.py
#
# These are the handlers for all JSON/REST API routes used by this application.
# 
######################################################################################

import csv 

import os, sys

import time

import hashlib 

import random

import xlrd

import collections

import json

from flask import ( g, Flask, render_template, make_response, request, Response, redirect, url_for, 
    abort, session, send_from_directory, jsonify )

from sqlalchemy import and_

from werkzeug import secure_filename

from app import app, db, googlelogin

from app.dbmodels import (create_unique_object_id, Operator, Sample, SampleTransfer, SampleTransferType, SamplePlate,
    SampleTransferDetail, SamplePlateLayout, SamplePlateType)

from well_mappings import ( get_col_and_row_for_well_id_48, get_well_id_for_col_and_row_48,
       get_col_and_row_for_well_id_96, get_well_id_for_col_and_row_96, get_col_and_row_for_well_id_384,
       get_well_id_for_col_and_row_384 )

import StringIO

from well_count_to_plate_type_name import well_count_to_plate_type_name

from logging_wrapper import get_logger
logger = get_logger(__name__)


#
# This is the "home" page, which is actually the "enter a sample movement" page.
#
def new_home():
    return app.send_static_file('index.html')


def user_data():
    user = None

    if hasattr(g, 'user') and hasattr(g.user, 'first_and_last_name'):
        user = {
            "name" : g.user.first_and_last_name
        }

    returnData = {
        "success": True
        ,"user": user
    }
    resp = Response(response=json.dumps(returnData),
        status=200, \
        mimetype="application/json")
    return(resp)

def google_login():
    returnData = {
        "login_url": googlelogin.login_url(scopes=['https://www.googleapis.com/auth/userinfo.email'])
    }
    resp = Response(response=json.dumps(returnData),
        status=200, \
        mimetype="application/json")
    return(resp)

def sample_tranfer_types():
    sample_tranfer_types2 = db.session.query(SampleTransferType).order_by(SampleTransferType.name);
    simplified_results = []
    for row in sample_tranfer_types2:
        simplified_results.append({"text": row.name, "value": row.id})
    returnData = {
        "success": True
        ,"results": simplified_results 
    }

    resp = Response(response=json.dumps(returnData),
        status=200, \
        mimetype="application/json")
    return(resp)

#
# Returns barcodes for all current sample plates
#
def sample_plate_barcodes():
    plates = db.session.query(SamplePlate).order_by(SamplePlate.sample_plate_id).all()

    plate_barcodes = [plate.external_barcode for plate in plates if plate.external_barcode is not None]
    
    resp = Response(response=json.dumps(plate_barcodes),
        status=200, \
        mimetype="application/json")
    return(resp)
