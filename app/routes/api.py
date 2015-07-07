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



from app import app, db

from app.dbmodels import (create_unique_object_id, Operator, Sample, SampleTransfer, SampleTransferType, SamplePlate,
    SampleTransferDetail, SamplePlateLayout, SamplePlateType)

#
# Returns the JSON representation of a "sample plate" based on the plate's ID.
#
def get_sample_plate(sample_plate_id):
    sample_plate = db.session.query(SamplePlate).filter_by(sample_plate_id=sample_plate_id).first()

    sample_plate_dict = {
       "sample_plate_id":sample_plate_id,
       "name":sample_plate.name,
       "description":sample_plate.description,
       "samplePlateType":sample_plate.sample_plate_type.name,
       "storageLocation":sample_plate.storage_location.name,
       "status":sample_plate.status,
       "externalBarcode":sample_plate.external_barcode,
    }

    resp = Response(response=json.dumps(sample_plate_dict),
        status=200, \
        mimetype="application/json")
    return(resp)


#
# Returns a sample plate id and the barcode for that plate. Or if a POST is sent to this URL,
# updates the barcode for the passed-in sample plate id.
#
def sample_plate_external_barcode(sample_plate_id):
    sample_plate = db.session.query(SamplePlate).filter_by(sample_plate_id=sample_plate_id).first()

    if request.method == 'GET':
        sample_plate_dict = {
           "sample_plate_id":sample_plate_id,
           "externalBarcode":sample_plate.external_barcode,
        }

        resp = Response(response=json.dumps(sample_plate_dict),
            status=200, \
            mimetype="application/json")
        return(resp)
    elif request.method == 'POST':
        external_barcode = request.json["externalBarcode"]
        sample_plate.external_barcode = external_barcode
        db.session.commit()
        print "external_barcode: ", external_barcode
        response = {
            "success":True
        }
        return jsonify(response)  


#
# Returns the "Sample Plate" report for a specified sample (specified by id). This can return the
# report as either JSON or a CSV.
#
def sample_report(sample_id, format):

    sample = db.session.query(Sample).filter_by(sample_id=sample_id).first()

    rows = db.session.query(SampleTransfer, SampleTransferDetail, SamplePlateLayout,SamplePlate).filter(and_(
        SampleTransferDetail.source_sample_id==sample_id,SampleTransfer.id==SampleTransferDetail.sample_transfer_id,
        SamplePlateLayout.sample_plate_id==SampleTransferDetail.source_sample_plate_id,
        SamplePlateLayout.sample_id==SampleTransferDetail.source_sample_id,
        SamplePlateLayout.well_id==SampleTransferDetail.source_well_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.source_sample_plate_id)).all()

    first_row = None 

    if len(rows) > 0:
        transfer, transfer_detail, well, plate = rows[0]
        first_row = { 
               "date_created": str(well.date_created),
               "destination_plate_barcode": plate.external_barcode,
               "well_id": well.well_id,
               "column": well.column,
               "row": well.row,
               "task": ""
        }

    rows = db.session.query(SampleTransfer, SampleTransferDetail, SamplePlateLayout,SamplePlate).filter(and_(
        SampleTransferDetail.destination_sample_id==sample_id,SampleTransfer.id==SampleTransferDetail.sample_transfer_id,
        SamplePlateLayout.sample_plate_id==SampleTransferDetail.destination_sample_plate_id,
        SamplePlateLayout.sample_id==SampleTransferDetail.destination_sample_id,
        SamplePlateLayout.well_id==SampleTransferDetail.destination_well_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.destination_sample_plate_id)).all()

    report = [
       { 
           "date_created":str(well.date_created),
           "destination_plate_barcode": plate.external_barcode,
           "well_id": well.well_id,
           "column": well.column,
           "row": well.row,
           "task": transfer.sample_transfer_type.name
       }
       for transfer, transfer_detail, well, plate in rows
    ]

    if first_row:
        report.insert(0,first_row)

    if format == "json":
        resp = Response(response=json.dumps(report),
            status=200, \
            mimetype="application/json")
        return(resp)
    elif format == "csv":
        csv = "SAMPLE DETAILS REPORT\n\n"
        csv += """,SAMPLE ID, CREATION DATE/TIME,CREATED BY\n """
        csv += "," + sample.sample_id + "," + str(sample.date_created) + "," + sample.operator.first_and_last_name

        """
        Destination Plate   Well Id Well Col    Well Row    Task
        """

        csv += "\n\nPLATE-TO-PLATE HISTORY\n\n"
        csv += ", DATE/TIME, DESTINATION PLATE, WELL ID, COLUMN, ROW, TASK\n"

        for plate in report:
            csv += ", " + str(plate["date_created"]) + "," + plate["destination_plate_barcode"] + ", " + str(plate["well_id"]) + ", " + str(plate["column"]) + ", " + str(plate["row"]) +  ", " + plate["task"] + "\n"


        # We need to modify the response, so the first thing we 
        # need to do is create a response out of the CSV string
        response = make_response(csv)
        # This is the key: Set the right header for the response
        # to be downloaded, instead of just printed on the browser
        response.headers["Content-Disposition"] = "attachment; filename=Sample_" + sample.sample_id + "_Report.csv"
        return response

#
# Returns the "Plate Details Report" for a specific plate (specified by its barcode). This can return
# the report as either JSON or a CSV.
#
def plate_report(sample_plate_barcode, format):

    #
    # "ccccccc1234"
    #
    sample_plate = db.session.query(SamplePlate).filter_by(external_barcode=sample_plate_barcode).first()
    sample_plate_id = sample_plate.sample_plate_id

    rows = db.session.query(SamplePlate,SampleTransferDetail).filter(and_(
        SampleTransferDetail.destination_sample_plate_id==sample_plate_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.source_sample_plate_id)).all()

    parent_to_this_task_name = None
    seen=[]
    parent_plates=[]
    for parent_plate, details in rows:
        if parent_plate.sample_plate_id not in seen:
            seen.append(parent_plate.sample_plate_id)
            parent_plates.append({
                "externalBarcode":parent_plate.external_barcode,
                "dateCreated":str(parent_plate.date_created)
            })
            parent_to_this_task_name = details.sample_transfer.sample_transfer_type.name
    

    rows = db.session.query(SamplePlate,SampleTransferDetail).filter(and_(
        SampleTransferDetail.source_sample_plate_id==sample_plate_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.destination_sample_plate_id)).all()
    
    this_to_child_task_name = None
    seen=[]
    child_plates=[]
    for child_plate, details in rows:
        if child_plate.sample_plate_id not in seen:
            seen.append(child_plate.sample_plate_id)
            child_plates.append({
                "externalBarcode":child_plate.external_barcode,
                "dateCreated":str(child_plate.date_created)
            })
            this_to_child_task_name = details.sample_transfer.sample_transfer_type.name



    wells = []

    rows = db.session.query(SamplePlateLayout).filter_by(sample_plate_id=sample_plate_id).all()
    for well in rows:
        well_dict = {
            "well_id":well.well_id,
            "column":well.column,
            "row":well.row,
            "sample_id":well.sample_id
        }
        wells.append(well_dict)


    report = {
        "parentPlates":parent_plates,
        "parentToThisTaskName":parent_to_this_task_name,
        "childPlates":child_plates,
        "thisToChildTaskName":this_to_child_task_name,
        "wells":wells,
        "plateDetails":{
            "dateCreated":str(sample_plate.date_created),
            "createdBy":str(sample_plate.operator.first_and_last_name)
        }
    }

    if format == "json":
        resp = Response(response=json.dumps(report),
            status=200, \
            mimetype="application/json")
        return(resp)
    elif format=="csv":

        csv = "PLATE REPORT\n\n"
        csv += """,PLATE ID, CREATION DATE/TIME,CREATED BY\n """
        csv += "," + sample_plate_barcode + "," + report["plateDetails"]["dateCreated"] + "," + report["plateDetails"]["createdBy"]

        if len(parent_plates) > 0:
            csv += "\n\n"
            csv += "PARENT PLATES\n\n"
            csv += ",TASK: " + report["parentToThisTaskName"] + "\n\n"
            csv += ",BAR CODE, CREATION DATE/TIME\n"
            for plate in parent_plates:
                csv += "," + plate["externalBarcode"] + "," + plate["dateCreated"] + "\n"

        if len(child_plates) > 0:
            csv += "\n\n"
            csv += "CHILD PLATES\n\n"
            csv += ",TASK: " + report["thisToChildTaskName"] + "\n\n"
            csv += ",BAR CODE, CREATION DATE/TIME\n"
            for child_plate in child_plates:
                csv += "," + child_plate["externalBarcode"] + "," + child_plate["dateCreated"] + "\n"


        csv += "\n\n"
        csv += "PLATE WELLS\n\n"
        csv += ",WELL ID, COLUMN, ROW, SAMPLE ID\n"

        """
         "well_id":well.well_id,
            "column":well.column,
            "row":well.row,
            "sample_id":well.sample_id
        """

        for well in wells:
            csv += "," + str(well["well_id"]) + "," + str(well["column"]) + ", " + str(well["row"]) + ", " + well["sample_id"] + "\n"





        # We need to modify the response, so the first thing we 
        # need to do is create a response out of the CSV string
        response = make_response(csv)
        # This is the key: Set the right header for the response
        # to be downloaded, instead of just printed on the browser
        response.headers["Content-Disposition"] = "attachment; filename=Plate_" + sample_plate_barcode + "_Report.csv"
        return response












#
# If the user uploaded a spreadsheet with each row representing a well-to-well transfer, this is where we 
# process that spreadsheet data.
#
def create_sample_movement_from_spreadsheet_data(operator,sample_transfer_type_id,wells):
    #
    # FIRST. Create a "sample_transfer" row representing this row's transfer.
    #
    sample_transfer = SampleTransfer(sample_transfer_type_id, operator.operator_id)
    db.session.add(sample_transfer)
    db.session.flush()

    destination_plates_by_barcode = {}
    sample_plate_types_by_name = {}

    #
    # NEXT: Now, do the transfer for each source-plate-well to each destination-plate-well...
    #
    order_number = 1

    for well in wells:
        source_plate_barcode = well["sourcePlateBarcode"]
        source_well_id = well["sourceWellId"]
        source_col_and_row = well["sourceColAndRow"]
        destination_plate_type_name = well["destinationPlateType"]
        destination_plate_barcode = well["destinationPlateBarcode"]
        destination_well_id = well["destinationWellId"]
        destination_col_and_row = well["destinationColAndRow"]

        #
        # 1. Obtain access to the source plate for this line item.
        #
        source_plate = db.session.query(SamplePlate).filter_by(external_barcode=source_plate_barcode).first()

        print "source plate barcode [%s]" % (source_plate_barcode)
        storage_location_id = source_plate.storage_location_id

        #
        # 2. Obtain (or create if we haven't yet grabbed it) the sample plate type row for the type of plate
        # specified for the destination of this line item.
        #
        sample_plate_type = sample_plate_types_by_name.get(destination_plate_type_name)
        if not sample_plate_type:
            sample_plate_type = db.session.query(SamplePlateType).filter_by(name=destination_plate_type_name).first()
            if sample_plate_type:
                sample_plate_types_by_name[destination_plate_type_name] = sample_plate_type

        #
        # 3. Obtain (or create if we haven't yet added a row for it in the database) the row for this well-to-well
        # transfer's destination plate.
        #
        destination_plate = destination_plates_by_barcode.get(destination_plate_barcode)
        if not destination_plate:
            destination_plate_name = create_unique_object_id("PLATE_")
            destination_plate_description = create_unique_object_id("PLATEDESC_")

            destination_plate = SamplePlate(sample_plate_type.type_id,operator.operator_id,storage_location_id,
            destination_plate_name, destination_plate_description, destination_plate_barcode)
            db.session.add(destination_plate)
            db.session.flush()
            destination_plates_by_barcode[destination_plate_barcode] = destination_plate


        #
        # 4. Get the "source plate well"
        #
        source_plate_well = db.session.query(SamplePlateLayout).filter(and_(
            SamplePlateLayout.sample_plate_id==source_plate.sample_plate_id,
            SamplePlateLayout.well_id==source_well_id
        )).first()


        #
        # 5. Create a row representing a well in the desination plate.
        #
        destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
            source_plate_well.sample_id,source_plate_well.well_id,operator.operator_id,
            source_plate_well.row,source_plate_well.column)
        db.session.add(destination_plate_well)


        #
        # 6. Create a row representing a transfer from a well in the "source" plate to a well
        # in the "desination" plate.
        #
        source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
           source_plate.sample_plate_id, source_plate_well.well_id, source_plate_well.sample_id,
           destination_plate.sample_plate_id, destination_plate_well.well_id, destination_plate_well.sample_id)
        db.session.add(source_to_destination_well_transfer)

        order_number += 1

    db.session.commit()


#
# If the user simply entered a "source plate" barcode and a "destination plate" barcode, we assume all wells in 
# the "source" plate will be moved to the exact same locations in the "destination" plate.
#
def create_one_plate_to_one_plate_sample_movement(operator,sample_transfer_type_id,source_barcode,destination_barcode):
    print "source_barcode: ", source_barcode
    print "destination_barcode: ", destination_barcode

    source_plate = db.session.query(SamplePlate).filter_by(external_barcode=source_barcode).first()
    print "SOURCE PLATE: ", source_plate

    source_plate_type_id = source_plate.type_id 
    storage_location_id = source_plate.storage_location_id

    destination_plate_name = create_unique_object_id("PLATE_")
    destination_plate_description = create_unique_object_id("PLATEDESC_")

    #
    # 1. Create the destination sample plate.
    #
    destination_plate = SamplePlate(source_plate_type_id,operator.operator_id,storage_location_id,
        destination_plate_name, destination_plate_description, destination_barcode)
    db.session.add(destination_plate)
    db.session.flush()

    #
    # 2. Create a "sample_transfer" row representing this entire transfer.
    #
    sample_transfer = SampleTransfer(sample_transfer_type_id, operator.operator_id)
    db.session.add(sample_transfer)
    db.session.flush()


    #
    # 3. Iterate through all the wells in the "source" plate. We'll create similar wells for the
    # destination plate.
    #
    order_number = 1
    for source_plate_well in source_plate.wells:

        #
        # 3a. Create a row representing a well in the desination plate.
        #
        destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
            source_plate_well.sample_id,source_plate_well.well_id,operator.operator_id,source_plate_well.row,source_plate_well.column)
        db.session.add(destination_plate_well)

        #
        # 3.b. Create a row representing a transfer from a well in the "source" plate to a well
        # in the "desination" plate.
        #
        source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
           source_plate.sample_plate_id, source_plate_well.well_id, source_plate_well.sample_id,
           destination_plate.sample_plate_id, destination_plate_well.well_id, destination_plate_well.sample_id)
        db.session.add(source_to_destination_well_transfer)

        order_number += 1

    #
    # Commit the transaction here.
    #
    db.session.commit()


#
# This creates a new "sample movement" or "sample transfer."
#
def create_sample_movement():
    data = request.json

    operator = g.user

    sample_transfer_type_id = data["sampleTransferTypeId"]

    wells = data.get("wells",None)

    #
    # If the user uploaded a spreadsheet with each row representing a well-to-well transfer, this is where we 
    # process that spreadsheet data.
    #
    if wells:
        create_sample_movement_from_spreadsheet_data(operator,sample_transfer_type_id,wells)



    #
    # If the user simply entered a "source plate" barcode and a "destination plate" barcode, we assume all wells in 
    # the "source" plate will be moved to the exact same locations in the "destination" plate.
    #
    else:
        source_barcode = data["sourceBarcodeId"]
        destination_barcode = data["destinationBarcodeId"]

        create_one_plate_to_one_plate_sample_movement(operator,sample_transfer_type_id,source_barcode,destination_barcode)



    response = {
        "success":True
    }


    return jsonify(response)  



#
# Returns ids of all sample plates. (Used in the UI's "type ahead" field so that the user can specify
# a sample plate by its id).
#
def get_sample_plates_list():
    plates = db.session.query(SamplePlate).order_by(SamplePlate.sample_plate_id).all()

    plate_ids = [plate.sample_plate_id for plate in plates]
    
    resp = Response(response=json.dumps(plate_ids),
        status=200, \
        mimetype="application/json")
    return(resp)


#
# Returns barcodes of all sample plates. (Used in the UI's "type ahead" field so that the user can specify
# a sample plate by its barcode).
#
def get_sample_plate_barcodes_list():
    plates = db.session.query(SamplePlate).order_by(SamplePlate.sample_plate_id).all()

    plate_barcodes = [plate.external_barcode for plate in plates if plate.external_barcode is not None]
    
    resp = Response(response=json.dumps(plate_barcodes),
        status=200, \
        mimetype="application/json")
    return(resp)


#
# Returns the list of sample ids. (Used in the UI's "type ahead" field so that the user can specify
# a sample by its id).
#
def get_samples_list():
    result = db.engine.execute('select sample_id from sample order by sample_id')
    sample_ids = []
    for row in result:
        sample_ids.append(row[0])
     
    resp = Response(response=json.dumps(sample_ids),
        status=200, \
        mimetype="application/json")
    return(resp)




