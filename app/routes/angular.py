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
import os
import time
import json

from flask import g, make_response, request, Response, session, jsonify
from math import floor

from sqlalchemy import and_

from werkzeug import secure_filename

from app import app, db, googlelogin

from app.dbmodels import (create_unique_object_id, Sample, SampleTransfer,
                          SamplePlate, SamplePlateLayout, SamplePlateType, SampleTransferDetail, SampleTransferType)

from well_mappings import (get_col_and_row_for_well_id_48,
                           get_well_id_for_col_and_row_48,
                           get_col_and_row_for_well_id_96,
                           get_well_id_for_col_and_row_96,
                           get_col_and_row_for_well_id_384,
                           get_well_id_for_col_and_row_384)

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
        simplified_results.append({"text": row.name, "id": row.id, "source_plate_count": row.source_plate_count, "destination_plate_count": row.destination_plate_count, "transfer_template_id": row.sample_transfer_template_id})
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

def update_plate_barcode():

    data = request.json

    sample_plate_id = data["plateId"]
    external_barcode = data["barcode"]

    sample_plate = db.session.query(SamplePlate).filter_by(sample_plate_id=sample_plate_id).first()


    if not sample_plate:
        response = {
            "success":False,
            "errorMessage":"There is no sample plate with the id: [%s]" % (sample_plate_id)
        }
        return jsonify(response)

    #
    # Is there a row in the database that already has this barcode? If so, bail, it is aready in use!
    #
    sample_plate_with_this_barcode = db.session.query(SamplePlate).filter_by(external_barcode=external_barcode).first()
    if sample_plate_with_this_barcode and sample_plate_with_this_barcode.sample_plate_id != sample_plate.sample_plate_id:
        logger.info(" %s encountered an error trying to update the plate with id [%s]. The barcode [%s] is already assigned to the plate with id: [%s]" % 
            (g.user.first_and_last_name,sample_plate_id,external_barcode,sample_plate_with_this_barcode.sample_plate_id))
        response = {
            "success":False,
            "errorMessage":"The barcode [%s] is already assigned to the plate with id: [%s]" % (external_barcode,sample_plate_with_this_barcode.sample_plate_id)
        }
        return jsonify(response)  


    sample_plate.external_barcode = external_barcode
    db.session.commit()
    print "external_barcode: ", external_barcode
    response = {
        "success":True
    }

    logger.info(" %s set the barcode [%s] for plate with id [%s]" % (g.user.first_and_last_name,external_barcode,sample_plate_id))

    return jsonify(response)

def sample_transfers():
    rows = db.session.query(SampleTransfer, SampleTransferDetail).filter(
        SampleTransferDetail.sample_transfer_id==SampleTransfer.id).order_by(
        SampleTransfer.date_transfer.desc()).all()

    sample_transfer_details = []

    seen = []

    for transfer,details in rows:
        if (transfer.id,details.source_sample_plate_id,details.destination_sample_plate_id) not in seen:
            seen.append((transfer.id,details.source_sample_plate_id,details.destination_sample_plate_id))
            sample_transfer_details.append((transfer,details))  

    transfers_data = {}

    # and create a serializable data array for the response
    for sample_transfer, details in sample_transfer_details:
        if (sample_transfer.id not in transfers_data):
            transfers_data[sample_transfer.id] = {
                "id": sample_transfer.id
                ,"name": sample_transfer.sample_transfer_type.name
                ,"date": sample_transfer.date_transfer.strftime("%A, %B %d %Y, %I:%M%p")
                ,"operator": sample_transfer.operator.first_and_last_name
                ,"source_barcodes": [details.source_plate.external_barcode]
                ,"destination_barcodes": [details.destination_plate.external_barcode]
            };
        else:
            transfers_data[sample_transfer.id]["destination_barcodes"].append(details.destination_plate.external_barcode)
            sourceAlready = False;
            for barcode in transfers_data[sample_transfer.id]["source_barcodes"]:
                if barcode == details.source_plate.external_barcode:
                    sourceAlready = True
                    break

            if not sourceAlready:
                transfers_data[sample_transfer.id]["source_barcodes"].append(details.source_plate.external_barcode) 

    resp = Response(response=json.dumps(transfers_data),
        status=200, \
        mimetype="application/json")
    return(resp)     
