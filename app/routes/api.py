"""Handlers for all JSON/REST API routes used by this application."""
######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: app/routes/api.py
#
#
#
######################################################################################

import os
import csv
import time
import json
import xlrd  # FIXME if this isn't actually used, we should remove
import StringIO

from math import floor
from flask import g, make_response, request, Response, jsonify

from sqlalchemy import and_

from werkzeug import secure_filename

from app import app, db

from twistdb import create_unique_id
from twistdb.sampletrack import Plate, Transfer, TransferDetail, Sample

from well_mappings import (get_col_and_row_for_well_id_48,
                           get_col_and_row_for_well_id_96,
                           get_col_and_row_for_well_id_384)

from logging_wrapper import get_logger
logger = get_logger(__name__)


ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def dragndrop():
    """
    The route to which the web page posts the spreadsheet
    detailing the well-to-well movements of samples.
    """
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + filename
        path_and_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_and_file_name)

        workbook = xlrd.open_workbook(path_and_file_name, on_demand=True)

        worksheet = workbook.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1

        curr_row = 0
        task_items = []
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



def sample_plate_external_barcode(plate_id):
    """
    Returns a sample plate id and the barcode for that plate. Or if a POST
    is sent to this URL, updates the barcode for the passed-in sample plate id.
    """
    sample_plate = db.session.query(Plate).filter_by(plate_id=plate_id).first()

    if request.method == 'GET':
        sample_plate_dict = {
            "plate_id": plate_id,
            "externalBarcode": sample_plate.external_barcode,
        }

        resp = Response(response=json.dumps(sample_plate_dict),
                        status=200, mimetype="application/json")
        return(resp)

    elif request.method == 'POST':
        external_barcode = request.json["externalBarcode"]

        if not sample_plate:
            response = {
                "success": False,
                "errorMessage": "There is no sample plate with the id: [%s]" %
                                (plate_id)
            }
            return jsonify(response)

        #
        # Is there a row in the database that already has this barcode? If so, bail, it is aready in use!
        #
        sample_plate_with_this_barcode = db.session.query(Plate).filter_by(external_barcode=external_barcode).first()
        if sample_plate_with_this_barcode and sample_plate_with_this_barcode.plate_id != sample_plate.id:
            logger.info(" %s encountered an error trying to update the plate with id [%s]. The barcode [%s] is already assigned to the plate with id: [%s]" %
                (g.user.first_and_last_name,plate_id,external_barcode,sample_plate_with_this_barcode.plate_id))
            response = {
                "success": False,
                "errorMessage": "The barcode [%s] is already assigned to the plate with id: [%s]" % (external_barcode,sample_plate_with_this_barcode.plate_id)
            }
            return jsonify(response)

        sample_plate.external_barcode = external_barcode
        db.session.commit()
        response = {
            "success": True
        }

        logger.info(" %s set the barcode [%s] for plate with id [%s]" % (g.user.first_and_last_name,external_barcode,plate_id))
        return jsonify(response)

def sample_report(sample_id, format):
    """
    Returns the "Sample Plate" report for a specified sample (specified by id).
    This can return the report as either JSON or a CSV.
    """
    sample = db.session.query(Sample).filter(Sample.id == sample_id).first()

    if not sample:
        response = {
            "success": False,
            "errorMessage": "There is no sample with the id: [%s]" % (sample_id)
        }
        return jsonify(response)

    rows = db.session.query(Transfer, TransferDetail, Sample, Plate).filter(
        TransferDetail.source_sample_id == sample_id,
        Transfer.id == TransferDetail.transfer_id,
        Sample.plate_id == TransferDetail.source_plate_id,
        Sample.sample_id == TransferDetail.source_sample_id,
        Sample.well_id == TransferDetail.source_well_id,
        Plate.id == TransferDetail.source_plate_id).all()

    first_row = None

    if len(rows) > 0:
        transfer, transfer_detail, well, plate = rows[0]

        number_clusters = plate.plate_type.layout.feature_count

        well_to_col_and_row_mapping_fn = {
            48: get_col_and_row_for_well_id_48,
            96: get_col_and_row_for_well_id_96,
            384: get_col_and_row_for_well_id_384
        }.get(number_clusters, lambda well_id: "missing map")

        first_row = {
            "date_created": str(well.date_created),
            "date_created_formatted": well.date_created.strftime("%A, %B %d, %Y %I:%M%p"),
            "destination_plate_barcode": plate.external_barcode,
            "well_id": well.well_id,
            "column_and_row": well_to_col_and_row_mapping_fn(well.well_id),
            "task": ""
        }

    rows = db.session.query(Transfer, TransferDetail, Sample, Plate).filter(
        TransferDetail.destination_sample_id == sample_id,
        Transfer.id == TransferDetail.transfer_id,
        Sample.plate_id == TransferDetail.destination_plate_id,
        Sample.id == TransferDetail.destination_sample_id,
        Sample.well.well_number == TransferDetail.destination_well_id,
        Plate.id == TransferDetail.destination_plate_id).all()

    report = []
    for transfer, transfer_detail, well, plate in rows:

        number_clusters = plate.plate_type.layout.feature_count

        well_to_col_and_row_mapping_fn = {
            48: get_col_and_row_for_well_id_48,
            96: get_col_and_row_for_well_id_96,
            384: get_col_and_row_for_well_id_384
        }.get(number_clusters, lambda well_id: "missing map")

        row = {
            "date_created": str(well.date_created),
            "date_created_formatted": well.date_created.strftime("%A, %B %d, %Y %I:%M%p"),
            "destination_plate_barcode": plate.external_barcode,
            "well_id": well.well_id,
            "column_and_row": well_to_col_and_row_mapping_fn(well.well_id),
            "task": transfer.transfer_type.name
        }
        report.append(row)

    if first_row:
        report.insert(0, first_row)

    if format == "json":
        response = {
            "success": True,
            "report": report
        }
        resp = Response(response=json.dumps(response),
            status=200, mimetype="application/json")
        return(resp)

    elif format == "csv":

        si = StringIO.StringIO()
        cw = csv.writer(si)

        cw.writerow(["SAMPLE DETAILS REPORT"])
        cw.writerow("")
        cw.writerow("")
        cw.writerow(["", "SAMPLE ID", "CREATION DATE/TIME","CREATED BY"])
        cw.writerow(["", sample.id, sample.date_created.strftime("%A, %B %d, %Y %I:%M%p"),sample.operator.first_and_last_name])

        cw.writerow("")
        cw.writerow("")
        cw.writerow(["PLATE-TO-PLATE HISTORY"])
        cw.writerow(["", "DATE/TIME", "DESTINATION PLATE", "WELL ID", "COL/ROW", "TASK"])

        for plate in report:
            cw.writerow(["",plate["date_created_formatted"],plate["destination_plate_barcode"],plate["well_id"],plate["column_and_row"],plate["task"]])

        csvout = si.getvalue().strip('\r\n')

        logger.info(" %s downloaded the SAMPLE DETAILS REPORT for sample with id [%s]" % (g.user.first_and_last_name,sample_id))

        # We need to modify the response, so the first thing we
        # need to do is create a response out of the CSV string
        response = make_response(csvout)
        # This is the key: Set the right header for the response
        # to be downloaded, instead of just printed on the browser
        response.headers["Content-Disposition"] = "attachment; filename=Sample_" + sample.id + "_Report.csv"
        return response


def plate_report(sample_plate_barcode, format):
    """
    Returns the "Plate Details Report" for a specific plate (specified by
    its barcode). This can return the report as either JSON or a CSV.
    """
    raise DeprecationWarning


def create_sample_movement_from_spreadsheet_data(operator, transfer_type_id,
                                                 wells):
    """
    If the user uploaded a spreadsheet with each row representing a
    well-to-well transfer, this is where we process that spreadsheet data.
    """
    raise DeprecationWarning


def get_sample_plate_barcodes_list():
    """
    Returns barcodes of all sample plates. (Used in the UI's "type ahead" field
    so that the user can specify a sample plate by its barcode).
    """
    plates = db.session.query(Plate).order_by(Plate.id).all()

    plate_barcodes = [plate.external_barcode for plate in plates if
                      plate.external_barcode is not None]

    resp = Response(response=json.dumps(plate_barcodes),
                    status=200, mimetype="application/json")
    return(resp)


def get_samples_list():
    """
    Returns the list of sample ids. (Used in the UI's "type ahead" field so
    that the user can specify a sample by its id).
    """
    result = db.engine.execute('select id from sampletrack.sample order by id')
    sample_ids = []
    for row in result:
        sample_ids.append(row[0])

    resp = Response(response=json.dumps(sample_ids),
                    status=200, mimetype="application/json")
    return(resp)


##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
######## ROUTES USED BY ANGULAR APP - Copying these to angular.py
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################


def create_sample_movement():
    """This creates a new "sample movement" or "sample transfer."""
    raise DeprecationWarning

    data = request.json

    operator = g.user
    transfer_type_id = data["sampleTransferTypeId"]

    if "sampleTransferTemplateId" in data:
        transfer_template_id = data["sampleTransferTemplateId"]
    else:
        transfer_template_id = 1

    wells = data.get("wells",None)

    #
    # If the user uploaded a spreadsheet with each row representing a well-to-well transfer, this is where we
    # process that spreadsheet data.
    #
    if wells:
        response = create_sample_movement_from_spreadsheet_data(operator,transfer_type_id,wells)

        if response["success"]:
            logger.info(" %s created a new sample movement using spreadsheet data." % (g.user.first_and_last_name))


    #
    # If the user simply entered a "source plate" barcode and a "destination plate" barcode, we assume all wells in
    # the "source" plate will be moved to the exact same locations in the "destination" plate.
    #
    else:

        source_barcodes = [data["sourceBarcodeId"]]
        destination_barcodes = [data["destinationBarcodeId"]]

        response = create_plate_sample_movement(operator,transfer_type_id,source_barcodes,destination_barcodes,transfer_template_id)

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

    raise DeprecationWarning

    plates = db.session.query(Plate).order_by(Plate.id).all()

    plate_ids = [plate.id for plate in plates]

    resp = Response(response=json.dumps(plate_ids),
        status=200, \
        mimetype="application/json")
    return(resp)

#
# Returns the JSON representation of a "sample plate" based on the plate's ID.
#
def get_sample_plate(plate_id):

    raise DeprecationWarning

    sample_plate = db.session.query(Plate).filter_by(plate_id=plate_id).first()

    if not sample_plate:
        response = {
            "success":False,
            "errorMessage":"There is no plate with the id: [%s]" % (plate_id)
        }
        return jsonify(response)

    sample_plate_dict = {
       "success":True,
       "plate_id":plate_id,
       "name":sample_plate.name,
       "description":sample_plate.description,
       "samplePlateType":sample_plate.plate_type.name,
       "storageLocation":sample_plate.storage_location.name,
       "status":sample_plate.status,
       "externalBarcode":sample_plate.external_barcode,
    }

    resp = Response(response=json.dumps(sample_plate_dict),
        status=200, \
        mimetype="application/json")
    return(resp)
