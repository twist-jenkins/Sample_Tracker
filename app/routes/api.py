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

from app import app, db

from twistdb import create_unique_id
from twistdb.public import *
from twistdb.sampletrack import *

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
            48:get_col_and_row_for_well_id_48,
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
            48:get_col_and_row_for_well_id_48,
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
    raise DeprecationWarning


#
# If the user uploaded a spreadsheet with each row representing a well-to-well transfer, this is where we
# process that spreadsheet data.
#
def create_sample_movement_from_spreadsheet_data(operator,sample_transfer_type_id,wells):
    raise DeprecationWarning

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


##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
######## ROUTES USED BY ANGULAR APP - Copying these to angular.py
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################


# creates a destination plate for a transfer
def create_destination_plate_DEPRECATED(operator, destination_plates, destination_barcode, source_plate_type_id, storage_location_id):
    raise DeprecationWarning

    destination_plate_name = create_unique_id("PLATE_")()
    destination_plate_description = create_unique_id("PLATEDESC_")()
    destination_plates.append(SamplePlate(source_plate_type_id,operator.operator_id,storage_location_id,
        destination_plate_name, destination_plate_description, destination_barcode))
    db.session.add(destination_plates[len(destination_plates) - 1])

#
# If the user simply entered a "source plate" barcode and a "destination plate" barcode, we assume all wells in
# the "source" plate will be moved to the exact same locations in the "destination" plate.
#

def create_plate_sample_movement(operator,sample_transfer_type_id,source_barcodes,destination_barcodes,sample_transfer_template_id):
    print "source_barcode: ", source_barcodes
    print "destination_barcode: ", destination_barcodes

    destination_plates = []

    if (len(source_barcodes) < 2): # single source plate
        source_barcode = source_barcodes[0]

        source_plate = db.session.query(SamplePlate).filter_by(external_barcode=source_barcode).first()
        if not source_plate:
            logger.info(" %s encountered error creating sample transfer. There is no source plate with the barcode: [%s]" % (g.user.first_and_last_name,source_barcode))
            return {
                "success":False,
                "errorMessage":"There is no source plate with the barcode: [%s]" % (source_barcode)
            }

        source_plate_type_id = source_plate.type_id
        storage_location_id = source_plate.storage_location_id

        #
        # 1. Create a "sample_transfer" row representing this entire transfer.
        #
        sample_transfer = SampleTransfer(sample_transfer_type_id, operator.operator_id)
        db.session.add(sample_transfer)

        # create destination plate(s)
        if sample_transfer_template_id == 1:
            create_destination_plate_DEPRECATED(operator, destination_plates, destination_barcodes[0], source_plate_type_id, storage_location_id)
        elif sample_transfer_template_id == 13 or sample_transfer_template_id == 14: # 1 to multiple
            for destination_barcode in destination_barcodes:
                create_destination_plate_DEPRECATED(operator, destination_plates, destination_barcode, source_plate_type_id, storage_location_id)
        else:
            return {
                "success":False,
                "errorMessage":"Unrecognized sample transfer template id: [%s]" % (sample_transfer_template_id)
            }

        db.session.flush()

        #
        # 3. Iterate through all the wells in the "source" plate. We'll create similar wells for the
        # destination plate.
        #

        order_number = 1

        for source_plate_well in source_plate.wells:


            #determine the destination plate
            if sample_transfer_template_id == 1: # same source well count to destination well count
                destination_plate_index = 0
                destination_plate_well_id = source_plate_well.well_id
            elif sample_transfer_template_id == 13: # 384 -> 4x96
                # for 1-to-4 transfer, we go in quadrants - everyo-other column + every-other row
                src_row_length = 24
                dest_row_length = 12
                rowIndex = floor(source_plate_well.well_id/src_row_length) + 1
                destination_plate_row_index = floor(rowIndex/2) + rowIndex%2
                normalized_well_id = source_plate_well.well_id - src_row_length*(rowIndex - 1)
                normalized_row_index = floor(normalized_well_id/2) + normalized_well_id%2
                destination_plate_well_id = normalized_row_index + dest_row_length*(destination_plate_row_index-1)
                #destination_plate_well_id =

                if rowIndex % 2 == 0:
                    #quad 3 or 4
                    if source_plate_well.well_id % 2 == 0:
                        destination_plate_index = 3
                    else:
                        destination_plate_index = 2
                else:
                    #quad 1 or 2
                    if source_plate_well.well_id % 2 == 0:
                        destination_plate_index = 1
                    else:
                        destination_plate_index = 0
            elif sample_transfer_template_id == 14: # 96 -> 2x48
                src_row_length = 12
                dest_row_length = 6
                rowIndex = floor(source_plate_well.well_id/src_row_length) + 1
                normalized_row_index = source_plate_well.well_id%src_row_length

                if normalized_row_index > 6 or normalized_row_index == 0:
                    destination_plate_index = 1
                    destination_row_index = normalized_row_index;
                else:
                    destination_plate_index = 0
                    destination_row_index = source_plate_well.well_id%dest_row_length

                destination_plate_well_id = destination_row_index + dest_row_length*(rowIndex - 1)


            destination_plate = destination_plates[destination_plate_index]

            existing_sample_plate_layout = db.session.query(SamplePlateLayout).filter(and_(
                SamplePlateLayout.sample_plate_id==destination_plate.sample_plate_id,
                SamplePlateLayout.sample_id==source_plate_well.sample_id,
                SamplePlateLayout.well_id==destination_plate_well_id
                )).first()

            #existing_sample_plate_layout = True

            #print source_plate_well.well_id

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
                source_plate_well.sample_id,destination_plate_well_id,operator.operator_id,source_plate_well.row,source_plate_well.column)

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

        else:
            if sample_transfer_template_id == 18: # 4x96 -> 384
                source_plates = []

                for barcode in source_barcodes: #load our source plates into an array for looping
                    source_plates.append(db.session.query(SamplePlate).filter_by(external_barcode=barcode).first())

                ind = 0;
                for plate in source_plates: #validate we have source plates
                    if not plate:
                        logger.info(" %s encountered error creating sample transfer. There is no source plate with the barcode: [%s]" % (g.user.first_and_last_name,source_barcodes[ind]))
                        return {
                            "success":False,
                            "errorMessage":"There is no source plate with the barcode: [%s]" % (source_barcodes[ind])
                        }
                    ind += 1

                #
                # 1. Create a "sample_transfer" row representing this entire transfer.
                #
                sample_transfer = SampleTransfer(sample_transfer_type_id, operator.operator_id)
                db.session.add(sample_transfer)

                # create destination plate
                create_destination_plate_DEPRECATED(operator, destination_plates, destination_barcodes[0], source_plate_type_id, storage_location_id)

                destination_plate = destination_plates[0]

                db.session.flush()

                order_number = 1

                for destination_plate_well in destination_plates[0].wells:
                    # for 1-to-4 transfer, we go in quadrants - everyo-other column + every-other row
                    dest_row_length = 24
                    src_row_length = 12
                    rowIndex = floor(order_number/dest_row_length) + 1;

                    if rowIndex % 2 == 0:
                        #quad 3 or 4
                        if order_number % 2 == 0:
                            source_plate_index = 3
                        else:
                            source_plate_index = 2
                    else:
                        #quad 1 or 2
                        if order_number % 2 == 0:
                            source_plate_index = 1
                        else:
                            source_plate_index = 0

                    source_plate = source_plates[source_plate_index];

                    source_plate_row_index = floor(rowIndex/2) + rowIndex%2;
                    normalized_well_id = order_number - dest_row_length*(rowIndex - 1)
                    normalized_row_index = floor(normalized_well_id/2) + normalized_well_id%2
                    source_plate_well_id = normalized_row_index + src_row_length*(source_plate_row_index-1)

                    existing_sample_plate_layout = db.session.query(SamplePlateLayout).filter(and_(
                        SamplePlateLayout.sample_plate_id==destination_plate.sample_plate_id,
                        SamplePlateLayout.sample_id==source_plate.wells[source_plate_well_id].sample_id,
                        SamplePlateLayout.well_id==order_number
                        )).first()

                    if existing_sample_plate_layout:
                        return {
                            "success":False,
                            "errorMessage":"This plate [%s] already contains sample [%s] in well [%s]" % (destination_plate.external_barcode,
                                source_plate.wells[source_plate_well_id].sample_id,source_plate_well_id)
                        }

                    #
                    # 3a. Create a row representing a well in the desination plate.
                    #
                    destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
                        source_plate.wells[source_plate_well_id].sample_id,order_number,operator.operator_id,source_plate.wells[source_plate_well_id].row,source_plate.wells[source_plate_well_id].column)

                    db.session.add(destination_plate_well)

                    #
                    # 3.b. Create a row representing a transfer from a well in the "source" plate to a well
                    # in the "desination" plate.
                    #
                    source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
                       source_plate.sample_plate_id, source_plate_well_id, source_plate.wells[source_plate_well_id].sample_id,
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

    if "sampleTransferTemplateId" in data:
        sample_transfer_template_id = data["sampleTransferTemplateId"]
    else:
        sample_transfer_template_id = 1

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

        source_barcodes = [data["sourceBarcodeId"]]
        destination_barcodes = [data["destinationBarcodeId"]]

        response = create_plate_sample_movement(operator,sample_transfer_type_id,source_barcodes,destination_barcodes,sample_transfer_template_id)

        #if response["success"]:
            #logger.info(" %s created a new sample one-plate-to-one-plate sample movement from plate [%s] to new plate [%s]." % (g.user.first_and_last_name,source_barcode,destination_barcode))
            #logger.info(" %s created a new sample one-plate-to-one-plate sample movement from plate [%s] to new plate [%s]." % (g.user.first_and_last_name,source_barcode,destination_barcodes))

    return Response(response=json.dumps(response),
        status=200, \
        mimetype="application/json")


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

