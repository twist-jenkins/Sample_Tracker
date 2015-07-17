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

from app import app, db

from app.dbmodels import (create_unique_object_id, Operator, Sample, SampleTransfer, SampleTransferType, SamplePlate,
    SampleTransferDetail, SamplePlateLayout, SamplePlateType)

from well_mappings import ( get_col_and_row_for_well_id_96, get_well_id_for_col_and_row_96, get_col_and_row_for_well_id_384,
       get_well_id_for_col_and_row_384 )

import StringIO

from well_count_to_plate_type_name import well_count_to_plate_type_name

from logging_wrapper import get_logger
logger = get_logger(__name__)


ALLOWED_EXTENSIONS = set(['xls','xlsx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#
# The route to which the web page posts the spreadsheet detailing the well-to-well movements of 
# samples.
#
def dragndrop():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + filename
        path_and_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_and_file_name)

        workbook = xlrd.open_workbook(path_and_file_name, on_demand = True)
        #print "SHEET NAMES: ", workbook.sheet_names()

        worksheet = workbook.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1

        task_items = []

        #print "NUMBER OF ROWS: ", num_rows

        """
        def get_col_and_row_for_well_id_96(well_id):
    cell = well_id_to_cell_map_96[well_id]
    return cell["col_and_row"]
    
def get_well_id_for_col_and_row_96(col_and_row):
    cell = col_and_row_to_cell_map_96[col_and_row]
    return cell["well_id"]

def get_col_and_row_for_well_id_384(well_id):
    cell = well_id_to_cell_map_384[well_id]
    return cell["col_and_row"]
    
def get_well_id_for_col_and_row_384(col_and_row):
    cell = col_and_row_to_cell_map_384[col_and_row]
    return cell["well_id"]
        """


        curr_row = 0
        while curr_row < num_rows:
            curr_row += 1

            """
            source_col_and_row = worksheet.cell_value(curr_row,2)
            if source_col_and_row

            destination_col_and_row = worksheet.cell_value(curr_row,6)
            """


            task_item = {
                "source_plate_barcode":worksheet.cell_value(curr_row,0),
                #"source_well_id":worksheet.cell_value(curr_row,1),
                "source_col_and_row":worksheet.cell_value(curr_row,1),
                #"destination_plate_type_name":worksheet.cell_value(curr_row,3),
                "destination_plate_barcode":worksheet.cell_value(curr_row,2),
                #"destination_well_id":worksheet.cell_value(curr_row,5),
                "destination_col_and_row":worksheet.cell_value(curr_row,3),
                "destination_well_count":worksheet.cell_value(curr_row,4)
            } 
            row = worksheet.row(curr_row)
            task_items.append(task_item)

        response = {
            "success":True,
            "task_items":task_items
        }

        logger.info(" %s uploaded a spreadsheet into the sample transfer form" % (g.user.first_and_last_name))


    return jsonify(response)  


#
# Returns the JSON representation of a "sample plate" based on the plate's ID.
#
def get_sample_plate(sample_plate_id):
    sample_plate = db.session.query(SamplePlate).filter_by(sample_plate_id=sample_plate_id).first()

    if not sample_plate:
        response = {
            "success":False,
            "errorMessage":"There is no plate with the id: [%s]" % (sample_plate_id)
        }
        return jsonify(response)

    sample_plate_dict = {
       "success":True,
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


#
# Returns the "Sample Plate" report for a specified sample (specified by id). This can return the
# report as either JSON or a CSV.
#
def sample_report(sample_id, format):

    sample = db.session.query(Sample).filter_by(sample_id=sample_id).first()

    if not sample:
        response = {
            "success":False,
            "errorMessage":"There is no sample with the id: [%s]" % (sample_id)
        }
        return jsonify(response)

    rows = db.session.query(SampleTransfer, SampleTransferDetail, SamplePlateLayout,SamplePlate).filter(and_(
        SampleTransferDetail.source_sample_id==sample_id,SampleTransfer.id==SampleTransferDetail.sample_transfer_id,
        SamplePlateLayout.sample_plate_id==SampleTransferDetail.source_sample_plate_id,
        SamplePlateLayout.sample_id==SampleTransferDetail.source_sample_id,
        SamplePlateLayout.well_id==SampleTransferDetail.source_well_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.source_sample_plate_id)).all()

    first_row = None 



    if len(rows) > 0:
        transfer, transfer_detail, well, plate = rows[0]

        number_clusters = plate.sample_plate_type.number_clusters

        #print "number_clusters: ", number_clusters 

        well_to_col_and_row_mapping_fn = {
            96:get_col_and_row_for_well_id_96,
            384:get_col_and_row_for_well_id_384
        }.get(number_clusters,lambda well_id:"missing map")

        first_row = { 
               "date_created": str(well.date_created),
               "date_created_formatted":well.date_created.strftime("%A, %B %d, %Y %I:%M%p"),
               "destination_plate_barcode": plate.external_barcode,
               "well_id": well.well_id,
               "column_and_row": well_to_col_and_row_mapping_fn(well.well_id),
               "task": ""
        }

    rows = db.session.query(SampleTransfer, SampleTransferDetail, SamplePlateLayout,SamplePlate).filter(and_(
        SampleTransferDetail.destination_sample_id==sample_id,SampleTransfer.id==SampleTransferDetail.sample_transfer_id,
        SamplePlateLayout.sample_plate_id==SampleTransferDetail.destination_sample_plate_id,
        SamplePlateLayout.sample_id==SampleTransferDetail.destination_sample_id,
        SamplePlateLayout.well_id==SampleTransferDetail.destination_well_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.destination_sample_plate_id)).all()

    report = []

    for transfer, transfer_detail, well, plate in rows:

        number_clusters = plate.sample_plate_type.number_clusters

        well_to_col_and_row_mapping_fn = {
            96:get_col_and_row_for_well_id_96,
            384:get_col_and_row_for_well_id_384
        }.get(number_clusters,lambda well_id:"missing map")

        row = { 
           "date_created":str(well.date_created),
           "date_created_formatted":well.date_created.strftime("%A, %B %d, %Y %I:%M%p"),
           "destination_plate_barcode": plate.external_barcode,
           "well_id": well.well_id,
           "column_and_row": well_to_col_and_row_mapping_fn(well.well_id),
           "task": transfer.sample_transfer_type.name
        }
        report.append(row)
       

    if first_row:
        report.insert(0,first_row)

    if format == "json":
        response = {
            "success":True,
            "report":report
        }
        resp = Response(response=json.dumps(response),
            status=200, \
            mimetype="application/json")
        return(resp)

    elif format == "csv":

        si = StringIO.StringIO()
        cw = csv.writer(si)
        #w.writerow(["foo","bar"])
        #return

        cw.writerow(["SAMPLE DETAILS REPORT"])
        cw.writerow("")
        cw.writerow("")
        cw.writerow(["","SAMPLE ID", "CREATION DATE/TIME","CREATED BY"])
        cw.writerow(["",sample.sample_id, sample.date_created.strftime("%A, %B %d, %Y %I:%M%p"),sample.operator.first_and_last_name])

        #csv2 = "SAMPLE DETAILS REPORT\n\n"
        #csv2 += """,SAMPLE ID, CREATION DATE/TIME,CREATED BY\n """
        #csv2 += "," + sample.sample_id + "," + "\"" + sample.date_created.strftime("%A, %B %d, %Y %I:%M%p") + "\"" + "," + sample.operator.first_and_last_name

 
        cw.writerow("")
        cw.writerow("")
        cw.writerow(["PLATE-TO-PLATE HISTORY"])
        cw.writerow(["","DATE/TIME", "DESTINATION PLATE", "WELL ID", "COL/ROW", "TASK"])

        #csv2 += "\n\nPLATE-TO-PLATE HISTORY\n\n"
        #csv2 += ", DATE/TIME, DESTINATION PLATE, WELL ID, COL/ROW, TASK\n"

        for plate in report:
            cw.writerow(["",plate["date_created_formatted"],plate["destination_plate_barcode"],plate["well_id"],plate["column_and_row"],plate["task"]])
            #date_created = "\"" + plate["date_created_formatted"] + "\""
            #print "date created [%s]" % (date_created)
            #csv2 += ", " + date_created + " ," + plate["destination_plate_barcode"] + ", " + str(plate["well_id"]) + ", " + str(plate["column_and_row"]) +  ", " + plate["task"] + "\n"



        csvout = si.getvalue().strip('\r\n')
        
        logger.info(" %s downloaded the SAMPLE DETAILS REPORT for sample with id [%s]" % (g.user.first_and_last_name,sample_id))


        #print "CSV: ", csvout


        # We need to modify the response, so the first thing we 
        # need to do is create a response out of the CSV string
        response = make_response(csvout)
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

    if not sample_plate:
        response = {
            "success":False,
            "errorMessage":"There is no plate with the barcode: [%s]" % (sample_plate_barcode)
        }
        return jsonify(response)

    sample_plate_id = sample_plate.sample_plate_id
    number_clusters = sample_plate.sample_plate_type.number_clusters

    #print "number_clusters: ", number_clusters 

    well_to_col_and_row_mapping_fn = {
        96:get_col_and_row_for_well_id_96,
        384:get_col_and_row_for_well_id_384
    }.get(number_clusters,lambda well_id:"missing map")

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
                "dateCreated":str(parent_plate.date_created),
                "dateCreatedFormatted":sample_plate.date_created.strftime("%A, %B %d, %Y %I:%M%p")
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
                "dateCreated":str(child_plate.date_created),
                "dateCreatedFormatted":sample_plate.date_created.strftime("%A, %B %d, %Y %I:%M%p")
            })
            this_to_child_task_name = details.sample_transfer.sample_transfer_type.name



    wells = []

    rows = db.session.query(SamplePlateLayout).filter_by(sample_plate_id=sample_plate_id).all()
    for well in rows:
        well_dict = {
            "well_id":well.well_id,
            "column_and_row":well_to_col_and_row_mapping_fn(well.well_id),
            "sample_id":well.sample_id
        }
        wells.append(well_dict)


    report = {
        "success":True,
        "parentPlates":parent_plates,
        "parentToThisTaskName":parent_to_this_task_name,
        "childPlates":child_plates,
        "thisToChildTaskName":this_to_child_task_name,
        "wells":wells,
        "plateDetails":{
            "dateCreated":str(sample_plate.date_created),
            "dateCreatedFormatted":sample_plate.date_created.strftime("%A, %B %d, %Y %I:%M%p"),
            "createdBy":str(sample_plate.operator.first_and_last_name)
        }
    }

    if format == "json":
        resp = Response(response=json.dumps(report),
            status=200, \
            mimetype="application/json")
        return(resp)

    elif format=="csv":


        si = StringIO.StringIO()
        cw = csv.writer(si)
        #w.writerow(["foo","bar"])
        #return

        cw.writerow(["PLATE REPORT"])
        cw.writerow("")
        cw.writerow("")
        cw.writerow(["","PLATE BARCODE", "CREATION DATE/TIME","CREATED BY"])
        cw.writerow("")
        cw.writerow(["",sample_plate_barcode, report["plateDetails"]["dateCreatedFormatted"],report["plateDetails"]["createdBy"]])

        #csv = "PLATE REPORT\n\n"
        #csv += """,PLATE BARCODE, CREATION DATE/TIME,CREATED BY\n """
        #csv += "," + sample_plate_barcode + "," + "\"" + report["plateDetails"]["dateCreatedFormatted"] + "\" ," + report["plateDetails"]["createdBy"]

        #
        # dt.strftime("%A, %d. %B %Y %I:%M%p")
        #

        if len(parent_plates) > 0:
            cw.writerow("")
            cw.writerow("")
            cw.writerow(["PARENT PLATES"])
            cw.writerow(["","Task:" + report["parentToThisTaskName"]])
            cw.writerow("")
            cw.writerow(["","BAR CODE", "CREATION DATE/TIME"])
            for plate in parent_plates:
                cw.writerow(["",plate["externalBarcode"], plate["dateCreatedFormatted"]])


        if len(child_plates) > 0:
            cw.writerow("")
            cw.writerow("")
            cw.writerow(["CHILD PLATES"])
            cw.writerow(["","Task:" + report["thisToChildTaskName"]])
            cw.writerow("")
            cw.writerow(["","BAR CODE", "CREATION DATE/TIME"])
            for plate in child_plates:
                cw.writerow(["",plate["externalBarcode"], plate["dateCreatedFormatted"]])


        cw.writerow("")
        cw.writerow("")
        cw.writerow(["PLATE WELLS"])
        cw.writerow(["","WELL ID", "COL/ROW", "SAMPLE ID"])


        for well in wells:
            cw.writerow(["",well["well_id"], well_to_col_and_row_mapping_fn(well["well_id"]), well["sample_id"]])

        csvout = si.getvalue().strip('\r\n')

        logger.info(" %s downloaded the PLATE DETAILS REPORT for plate with barcode [%s]" % (g.user.first_and_last_name,sample_plate_barcode))

        # We need to modify the response, so the first thing we 
        # need to do is create a response out of the CSV string
        response = make_response(csvout)
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

    well_from_col_and_row_methods = {
        "96":get_well_id_for_col_and_row_96,
        "384":get_well_id_for_col_and_row_384
    }

    for well in wells:
        source_plate_barcode = well["sourcePlateBarcode"]
        #source_well_id = well["sourceWellId"]
        source_col_and_row = well["sourceColAndRow"]
        #destination_plate_type_name = well["destinationPlateType"]
        destination_plate_barcode = well["destinationPlateBarcode"]
        #destination_well_id = well["destinationWellId"]
        destination_col_and_row = well["destinationColAndRow"]
        destination_well_count = well["destinationWellCount"]

        #print "WELL: ", well

        #print "DEST WELL COUNT: ", destination_well_count

        #
        # well_count_to_plate_type_name
        #

        #if destination_well_count and destination_well_count.strip() != "":
            #print "USING well count rather than destination plate type name"
            #destination_well_count = "invalid"
        destination_plate_type_name = well_count_to_plate_type_name.get(destination_well_count.strip(),None)
        print "\n\nCalculated destination_plate_type_name: %s from well count: %s" % (destination_plate_type_name,destination_well_count)

        if not destination_plate_type_name:
            return {
                "success":False,
                "errorMessage":"There is no plate type with %s wells" % (destination_well_count)
            }

        #
        # 1. Obtain access to the source plate for this line item.
        #
        source_plate = db.session.query(SamplePlate).filter_by(external_barcode=source_plate_barcode).first()

        if not source_plate:
            logger.info(" %s encountered error creating sample transfer. There is no source plate with the barcode: [%s]" % (g.user.first_and_last_name,source_plate_barcode))
            return {
                "success":False,
                "errorMessage":"There is no source plate with the barcode: [%s]" % (source_plate_barcode)
            }

        #
        # 96 well, plastic
        #
        sample_plate_type = source_plate.sample_plate_type
        plate_size = None 
        if sample_plate_type.name == "96 well, plastic":
            plate_size = "96" 
        elif sample_plate_type.name == "384 well, plastic":
            plate_size = "384" 
        else:
            plate_size = None 

        print "\n\nSOURCE PLATE, barcode: %s  plate type: [%s]" % (source_plate.external_barcode,sample_plate_type.name)
        logger.info("SOURCE PLATE, barcode: %s  plate type: [%s]" % (source_plate.external_barcode,sample_plate_type.name))

        source_col_and_row = source_col_and_row.strip()

        #if source_well_id is None or source_well_id.strip() == "":
        if plate_size is None:
            return {
                "success":False,
                "errorMessage":"You must specify a SOURCE well id. Currently this app only has wellid-to-col/row mappings for 96 and 384 size plates and the source plate is this type: [%s]" % (sample_plate_type.name)
            }
        else:
            source_well_id = well_from_col_and_row_methods[plate_size](source_col_and_row)
            logger.info ("calculated source well id: %s from plate size: %s and column/row: %s" % (source_well_id,plate_size, source_col_and_row))
            print "calculated source well id: %s from plate size: %s and column/row: %s" % (source_well_id,plate_size, source_col_and_row)
        
        #else:
        #    source_well_id = well_from_col_and_row_methods[plate_size](row_and_column)
        #    logger.info ("calculated source well id: %s from plate size: %s and column/row: %s" % (source_well_id,plate_size, row_and_column))
        #    print "calculated source well id: %s from plate size: %s and column/row: %s" % (source_well_id,plate_size, row_and_column)

        """
        if source_col_and_row != "":
            parts = source_col_and_row.split(":")
            if len(parts) < 2:
                return {
                    "success":False,
                    "errorMessage":"Please specify both the plate size and the row-and-column ==> Like this: 384:A2"
                }
                plate_size, row_and_column = parts[0], parts[1]
                print "plate size: %s   row and column %s " % (plate_size, row_and_column)
                source_well_id = well_from_col_and_row_methods[plate_size](row_and_column)
                logger.info ("calculated source well id: %s from plate size: %s and column/row: %s" % (source_well_id,plate_size, row_and_column))
                print "calculated source well id: %s from plate size: %s and column/row: %s" % (source_well_id,plate_size, row_and_column)
        """



        #print "source plate barcode [%s]" % (source_plate_barcode)
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
            else:
                logger.info(" %s encountered error creating sample transfer. There are no sample plates with the type: [%s]" % (g.user.first_and_last_name,destination_plate_type_name))
                return {
                    "success":False,
                    "errorMessage":"There are no sample plates with the type: [%s]" % (destination_plate_type_name)
                }





        #
        # 3. Obtain (or create if we haven't yet added a row for it in the database) the row for this well-to-well
        # transfer's destination plate.
        #
        destination_plate = destination_plates_by_barcode.get(destination_plate_barcode)
        if not destination_plate:

            #
            # Is there already a plate in the database with the barcode being specified?
            # If so, that is an error!
            #
            destination_plate = db.session.query(SamplePlate).filter_by(external_barcode=destination_plate_barcode).first()
            if destination_plate:
                logger.info(" %s encountered error creating sample transfer. A plate with the destination plate barcode: [%s] already exists" % (g.user.first_and_last_name,destination_plate_barcode))
                return {
                    "success":False,
                    "errorMessage":"A plate with the destination plate barcode: [%s] already exists" % (destination_plate_barcode)
                }


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

        print "SOURCE PLATE WELL: %s " % str(source_plate_well)
        logger.info("SOURCE PLATE WELL: %s " % str(source_plate_well))

        if sample_plate_type.name == "96 well, plastic":
            plate_size = "96" 
        elif sample_plate_type.name == "384 well, plastic":
            plate_size = "384" 
        else:
            plate_size = None 

        if not source_plate_well:
            error_well_id = source_well_id
            if plate_size:
                if plate_size == "96":
                    try:
                        error_well_id = get_col_and_row_for_well_id_96(source_well_id)
                    except:
                        error_well_id = source_well_id
                elif plate_size == "384":
                    try:
                        error_well_id = get_col_and_row_for_well_id_384(source_well_id)
                    except:
                        error_well_id = source_well_id
            print "*** WARNING ***: There is no well [%s] in the source plate with barcode: [%s]" % (error_well_id,source_plate_barcode)
            logger.info("*** WARNING ***: There is no well [%s] in the source plate with barcode: [%s]" % (error_well_id,source_plate_barcode))
            continue

            """
            return {
                "success":False,
                "errorMessage":"There is no well [%s] in the source plate with barcode: [%s]" % (error_well_id,source_plate_barcode)
            }
            """



        #print "DESTINATION PLATE TYPE: ",sample_plate_type.name

        print "DESTINATION PLATE, barcode: %s  plate type: [%s]" % (destination_plate.external_barcode,sample_plate_type.name)
        logger.info("DESTINATION PLATE, barcode: %s  plate type: [%s]" % (destination_plate.external_barcode,sample_plate_type.name))

        #if destination_well_id is None or destination_well_id.strip() == "":
        if plate_size is None:
            return {
                "success":False,
                "errorMessage":"You must specify a DESTINATION well id. Currently this app only has wellid-to-col/row mappings for 96 and 384 size plates and the source plate is this type: [%s]" % (sample_plate_type.name)
            }
        else:
            destination_well_id = well_from_col_and_row_methods[plate_size](destination_col_and_row)
            logger.info ("calculated DEST well id: %s from plate size: %s and column/row: %s" % (destination_well_id,plate_size, destination_col_and_row))
            print "calculated DEST well id: %s from plate size: %s and column/row: %s" % (destination_well_id,plate_size, destination_col_and_row)


        #print "DEST WELL ID: ", destination_well_id

        existing_sample_plate_layout = db.session.query(SamplePlateLayout).filter(and_(
            SamplePlateLayout.sample_plate_id==destination_plate.sample_plate_id,
            SamplePlateLayout.sample_id==source_plate_well.sample_id,
            SamplePlateLayout.well_id==destination_well_id
            )).first()

        #existing_sample_plate_layout = True 

        if existing_sample_plate_layout:
            return {
                "success":False,
                "errorMessage":"This destination plate [%s] already contains sample [%s] in well [%s]" % (destination_plate.external_barcode,
                    source_plate_well.sample_id,source_plate_well.well_id)
            }


        #
        # 5. Create a row representing a well in the desination plate.
        #

        #
        # FIXED: 7/17/15
        #
        # WRONG! Was depositing in source well id not dest well idn destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
        #    source_plate_well.sample_id,source_plate_well.well_id,operator.operator_id,
        #    source_plate_well.row,source_plate_well.column)
        #db.session.add(destination_plate_well)

        destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
            source_plate_well.sample_id,destination_well_id,operator.operator_id,
            source_plate_well.row,source_plate_well.column)
        db.session.add(destination_plate_well)


        print "DESTINATION PLATE WELL: %s " % (str(destination_plate_well))
        logger.info("DESTINATION PLATE WELL: %s " % (str(destination_plate_well)))

        #
        # 6. Create a row representing a transfer from a well in the "source" plate to a well
        # in the "desination" plate.
        #
        source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
           source_plate.sample_plate_id, source_plate_well.well_id, source_plate_well.sample_id,
           destination_plate.sample_plate_id, destination_plate_well.well_id, destination_plate_well.sample_id)
        db.session.add(source_to_destination_well_transfer)

        order_number += 1

    #return {
    #    "success":False,
    #    "errorMessage":"testing!!!"
    #}

    db.session.commit()

    return {
        "success":True
    }


#
# If the user simply entered a "source plate" barcode and a "destination plate" barcode, we assume all wells in 
# the "source" plate will be moved to the exact same locations in the "destination" plate.
#
def create_one_plate_to_one_plate_sample_movement(operator,sample_transfer_type_id,source_barcode,destination_barcode):
    print "source_barcode: ", source_barcode
    print "destination_barcode: ", destination_barcode

    source_plate = db.session.query(SamplePlate).filter_by(external_barcode=source_barcode).first()
    if not source_plate:
        logger.info(" %s encountered error creating sample transfer. There is no source plate with the barcode: [%s]" % (g.user.first_and_last_name,source_barcode))
        return {
            "success":False,
            "errorMessage":"There is no source plate with the barcode: [%s]" % (source_barcode)
        }
    #print "SOURCE PLATE: ", source_plate

    destination_plate = db.session.query(SamplePlate).filter_by(external_barcode=destination_barcode).first()
    if destination_plate:
        logger.info(" %s encountered error creating sample transfer. A plate with the destination plate barcode: [%s] already exists" % (g.user.first_and_last_name,destination_barcode))
        return {
            "success":False,
            "errorMessage":"A plate with the destination plate barcode: [%s] already exists" % (destination_barcode)
        }

    #print "SOURCE PLATE: ", source_plate

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

        existing_sample_plate_layout = db.session.query(SamplePlateLayout).filter(and_(
            SamplePlateLayout.sample_plate_id==destination_plate.sample_plate_id,
            SamplePlateLayout.sample_id==source_plate_well.sample_id,
            SamplePlateLayout.well_id==source_plate_well.well_id
            )).first()

        #existing_sample_plate_layout = True 

        if existing_sample_plate_layout:
            return {
                "success":False,
                "errorMessage":"This plate [%s] already contains sample [%s] in well [%s]" % (destination_plate.external_barcode,
                    source_plate_well.sample_id,source_plate_well.well_id)
            }

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

    return {
        "success":True
    }


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
        response = create_sample_movement_from_spreadsheet_data(operator,sample_transfer_type_id,wells)

        if response["success"]:
            logger.info(" %s created a new sample movement using spreadsheet data." % (g.user.first_and_last_name))



    #
    # If the user simply entered a "source plate" barcode and a "destination plate" barcode, we assume all wells in 
    # the "source" plate will be moved to the exact same locations in the "destination" plate.
    #
    else:
        source_barcode = data["sourceBarcodeId"]
        destination_barcode = data["destinationBarcodeId"]

        response = create_one_plate_to_one_plate_sample_movement(operator,sample_transfer_type_id,source_barcode,destination_barcode)

        if response["success"]:
            logger.info(" %s created a new sample one-plate-to-one-plate sample movement from plate [%s] to new plate [%s]." % (g.user.first_and_last_name,source_barcode,destination_barcode))


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




