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

from app.plate_to_plate_maps import maps_json

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

def sample_transfer_types():
    sample_transfer_types2 = db.session.query(SampleTransferType).order_by(SampleTransferType.id);
    simplified_results = []
    for row in sample_transfer_types2:
        simplified_results.append({"text": row.name, "id": row.id, "source_plate_count": row.source_plate_count, "destination_plate_count": row.destination_plate_count, "transfer_template_id": row.sample_transfer_template_id, "inverted":row.inverted})
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

# creates a destination plate for a transfer
def create_destination_plate(operator, destination_plates, destination_barcode, source_plate_type_id, storage_location_id):
    destination_plate_name = create_unique_object_id("PLATE_")
    destination_plate_description = create_unique_object_id("PLATEDESC_")
    destination_plates.append(SamplePlate(source_plate_type_id,operator.operator_id,storage_location_id,
        destination_plate_name, destination_plate_description, destination_barcode))
    db.session.add(destination_plates[len(destination_plates) - 1])

def create_step_record():
    data = request.json
    operator = g.user

    sample_transfer_type_id = data["sampleTransferTypeId"]
    sample_transfer_template_id = data["sampleTransferTemplateId"]

    source_barcodes = data["sourcePlates"]
    destination_barcodes = data["destinationPlates"]

    source_plates = []
    destination_plates = []

    json_maps = maps_json()

    if sample_transfer_template_id in json_maps:
        templateData = json_maps[sample_transfer_template_id];
    else:
        return jsonify({
            "success": False
            ,"errorMessage": "A template for this transfer type (%s) could not be found." % (sample_transfer_template_id)
        })

    # validate that the plate counts/barcodes expected for a given template are present
    source_barcodes_count = len(source_barcodes)
    destination_barcodes_count = len(destination_barcodes)

    problem_plates = ""

    if templateData["source"]["plate_count"] != source_barcodes_count:
        problem_plates = "source"
    if templateData["destination"]["plate_count"] != destination_barcodes_count:
        problem_plates = "destination"  

    if problem_plates != "":
        return jsonify({
            "success": False
            ,"errorMessage": "The number of %s plates does not match the template." % (problem_plates)
        })

    #Create a "sample_transfer" row representing this entire transfer.
    sample_transfer = SampleTransfer(sample_transfer_type_id, operator.operator_id)
    db.session.add(sample_transfer)

    for barcode in source_barcodes: #load our source plates into an array for looping
        source_plate = db.session.query(SamplePlate).filter_by(external_barcode=barcode).first()
        if not source_plate:
            logger.info(" %s encountered error creating sample transfer. There is no source plate with the barcode: %s" % (g.user.first_and_last_name,barcode))
            return jsonify({
                "success":False,
                "errorMessage":"There is no source plate with the barcode: %s" % (barcode)
            })
        source_plates.append(source_plate)

    #the easy case: source and destination plates have same layout and there's only 1 of each
    if sample_transfer_template_id == 1:
        
        order_number = 1
        source_plate = source_plates[0]

        # create the destination plate
        create_destination_plate(operator, destination_plates, destination_barcodes[0], source_plate.type_id, source_plate.storage_location_id)
        db.session.flush()

        destination_plate = destination_plates[0]

        for source_plate_well in source_plate.wells:

            destination_plate_well_id = source_plate_well.well_id

            existing_sample_plate_layout = db.session.query(SamplePlateLayout).filter(and_(
                SamplePlateLayout.sample_plate_id==destination_plate.sample_plate_id,
                SamplePlateLayout.sample_id==source_plate_well.sample_id,
                SamplePlateLayout.well_id==destination_plate_well_id
                )).first()

            # error if there is already a sample in this dest well
            if existing_sample_plate_layout:
                return jsonify({
                    "success":False,
                    "errorMessage":"Plate [%s] already contains sample %s in well %s" % (destination_plate.external_barcode,
                        source_plate_well.sample_id,source_plate_well.well_id)
                })

            # create a row representing a well in the desination plate.
            destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
                source_plate_well.sample_id,destination_plate_well_id,operator.operator_id,source_plate_well.row,source_plate_well.column)

            db.session.add(destination_plate_well)

            # Create a row representing a transfer from a well in the "source" plate to a well
            # in the "desination" plate.

            source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
               source_plate.sample_plate_id, source_plate_well.well_id, source_plate_well.sample_id,
               destination_plate.sample_plate_id, destination_plate_well.well_id, destination_plate_well.sample_id)
            db.session.add(source_to_destination_well_transfer)

            order_number += 1

    # source(s) and destination(s) are not the same plate type/layout
    else:

        storage_location_id = source_plates[0].storage_location_id
        target_plate_type_id = templateData["destination"]["plate_type_id"];

        # create the destination plate(s)
        for destination_barcode in destination_barcodes:
            create_destination_plate(operator, destination_plates, destination_barcode, target_plate_type_id, storage_location_id)


        base_plates = source_plates;
        target_plates = destination_plates;

        db.session.flush()

        plate_well_to_well_maps = templateData["plate_well_to_well_maps"]

        plate_number = 0;
        for source_plate in source_plates:
            well_to_well_map = plate_well_to_well_maps[plate_number];
            plate_number+= 1

            order_number = 1

            for source_plate_well in source_plate.wells:
                print source_plate_well    

                map_item = well_to_well_map[source_plate_well.well_id];

                print map_item

                destination_plate_well_id = map_item["destination_well_id"];
                destination_plate_number = map_item["destination_plate_number"];
                destination_plate = destination_plates[destination_plate_number - 1];

                print destination_plate_well_id

                existing_sample_plate_layout = db.session.query(SamplePlateLayout).filter(and_(
                    SamplePlateLayout.sample_plate_id==destination_plate.sample_plate_id,
                    SamplePlateLayout.sample_id==source_plate_well.sample_id,
                    SamplePlateLayout.well_id==destination_plate_well_id
                    )).first()

                # error if there is already a sample in this dest well
                if existing_sample_plate_layout:
                    return jsonify({
                        "success":False,
                        "errorMessage":"Plate [%s] already contains sample %s in well %s" % (destination_plate.external_barcode,
                            source_plate_well.sample_id,source_plate_well.well_id)
                    })

                # create a row representing a well in the desination plate.
                destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
                    source_plate_well.sample_id,destination_plate_well_id,operator.operator_id, "Z", "-1") # TO DO: assign non-bogus row and column values

                db.session.add(destination_plate_well)

                # Create a row representing a transfer from a well in the "source" plate to a well
                # in the "desination" plate.

                source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
                   source_plate.sample_plate_id, source_plate_well.well_id, source_plate_well.sample_id,
                   destination_plate.sample_plate_id, destination_plate_well.well_id, destination_plate_well.sample_id)
                db.session.add(source_to_destination_well_transfer)

                order_number += 1


    db.session.commit()

    return jsonify({
        "success":True
    })
