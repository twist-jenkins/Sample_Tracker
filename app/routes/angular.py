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

from logging_wrapper import get_logger
logger = get_logger(__name__)

MAX_SAMPLE_TRANSFER_QUERY_ROWS = 100000

#
# This is the "home" page, which is actually the "enter a sample movement" page.
#
def new_home():
    return app.send_static_file('index.html')


def error_response(status_code, message):
    response = jsonify({'success': False, 'message': message})
    response.status_code = status_code
    return response


def user_data():
    user = None

    if hasattr(g, 'user') and hasattr(g.user, 'first_and_last_name'):
        user = {
            "name": g.user.first_and_last_name,
            "env": app.config['ENV']
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
        errmsg = "There is no sample plate with the id: [%s]"
        return error_response(404, errmsg % sample_plate_id)

    #
    # Is there a row in the database that already has this barcode? If so, bail, it is aready in use!
    #
    sample_plate_with_this_barcode = db.session.query(SamplePlate).filter_by(external_barcode=external_barcode).first()
    if sample_plate_with_this_barcode and sample_plate_with_this_barcode.sample_plate_id != sample_plate.sample_plate_id:
        logger.info(" %s encountered an error trying to update the plate with id [%s]. The barcode [%s] is already assigned to the plate with id: [%s]" %
            (g.user.first_and_last_name,sample_plate_id,external_barcode,sample_plate_with_this_barcode.sample_plate_id))
        errmsg = "The barcode [%s] is already assigned to the plate with id: [%s]"
        return error_response(400, errmsg % (external_barcode, sample_plate_with_this_barcode.sample_plate_id))


    sample_plate.external_barcode = external_barcode
    db.session.commit()
    logging.info("external_barcode: %s", external_barcode)
    response = {
        "success":True
    }

    logger.info(" %s set the barcode [%s] for plate with id [%s]" % (g.user.first_and_last_name,external_barcode,sample_plate_id))

    return jsonify(response)

def sample_transfers(limit=MAX_SAMPLE_TRANSFER_QUERY_ROWS):

    qry = (
        db.session.query(
            SampleTransfer,
            SampleTransferDetail
        )
        .options(subqueryload(SampleTransferDetail.source_plate))
        .options(subqueryload(SampleTransferDetail.destination_plate))
        .options(subqueryload(SampleTransfer.sample_transfer_type))
        .options(subqueryload(SampleTransfer.operator))
        .filter(SampleTransferDetail.sample_transfer_id == SampleTransfer.id)
        .order_by(SampleTransfer.date_transfer.desc())
    )
    if limit is None:
        rows = qry.all()
    else:
        rows = qry.limit(limit)

    sample_transfer_details = []

    seen = []

    for transfer, details in rows:
        key = (transfer.id,
               details.source_sample_plate_id,
               details.destination_sample_plate_id)
        if key not in seen:
            seen.append(key)
            sample_transfer_details.append((transfer, details))

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
            }
        else:
            already = False
            for barcode in transfers_data[sample_transfer.id]["source_barcodes"]:
                if barcode == details.source_plate.external_barcode:
                    already = True
                    break
            if not already:
                transfers_data[sample_transfer.id]["source_barcodes"].append(details.source_plate.external_barcode)
            already = False
            for barcode in transfers_data[sample_transfer.id]["destination_barcodes"]:
                if barcode == details.destination_plate.external_barcode:
                    already = True
                    break
            if not already:
                transfers_data[sample_transfer.id]["destination_barcodes"].append(details.destination_plate.external_barcode)

    # ugliness here to turn the map created above into an ordered array
    transfersDataArray = []
    for item in transfers_data:
        transfersDataArray.insert(transfers_data[item]['id'], transfers_data[item])

    fullDataArray = []
    for item in transfersDataArray:
        if item is not None:
            fullDataArray.append(item)

    fullDataArray.reverse()

    resp = Response(response=json.dumps(fullDataArray),
        status=200, \
        mimetype="application/json")
    return(resp)


def create_step_record_adhoc(sample_transfer_type_id,
                             sample_transfer_template_id,
                             wells):

    operator = g.user
    with scoped_session(db.engine) as db_session:
        result = create_adhoc_sample_movement(db_session, operator,
                                              sample_transfer_type_id,
                                              sample_transfer_template_id,
                                              wells)
        if result["success"]:
            return jsonify({
                "success": True
            })
        else:
            return error_response(400, result["errorMessage"])

def create_step_record():
    data = request.json
    operator = g.user

    sample_transfer_type_id = data["sampleTransferTypeId"]
    sample_transfer_template_id = data["sampleTransferTemplateId"]

    if "transferMap" in data:
        transfer_map = data["transferMap"]
        return create_step_record_adhoc(sample_transfer_type_id,
                                        sample_transfer_template_id,
                                        transfer_map)

    else:
        source_barcodes = data["sourcePlates"]
        destination_barcodes = data["destinationPlates"]

        source_plates = []
        destination_plates = []

        json_maps = maps_json()

        if sample_transfer_template_id in json_maps["transfer_maps"]:
            templateData = json_maps["transfer_maps"][sample_transfer_template_id]
        else:
            errmsg = "A template for this transfer type (%s) could not be found."
            return error_response(404, errmsg % sample_transfer_template_id)

        # validate that the plate counts/barcodes expected for a given template are present
        source_barcodes_count = len(source_barcodes)
        destination_barcodes_count = len(destination_barcodes)

        problem_plates = ""

        if templateData["source"]["plate_count"] != source_barcodes_count:
            problem_plates = "source"
        if templateData["destination"]["plate_count"] != destination_barcodes_count:
            problem_plates = "destination"

        if problem_plates != "":
            errmsg = "The number of %s plates does not match the template."
            return error_response(400, errmsg % problem_plates)

        with scoped_session(db.engine) as db_session:

            # Create a "sample_transfer" row representing this entire transfer.
            sample_transfer = SampleTransfer(sample_transfer_type_id,
                                             None,
                                             operator.operator_id)
            db_session.add(sample_transfer)

            for barcode in source_barcodes:
                # load our source plates into an array for looping
                source_plate = db_session.query(SamplePlate).filter_by(external_barcode=barcode).first()
                if not source_plate:
                    errmsg = "There is no source plate with the barcode: %s"
                    errmsg %= barcode
                    logger.info(" %s encountered error creating sample transfer: " % g.user.first_and_last_name + errmsg)
                    return error_response(404, errmsg)
                source_plates.append(source_plate)

            # the easy case: source and destination plates have same layout and there's only 1 of each
            if sample_transfer_template_id == 1:

                order_number = 1
                source_plate = source_plates[0]

                # create the destination plate
                plate = create_destination_plate(db_session, operator,
                                                 destination_barcodes[0],
                                                 source_plate.type_id,
                                                 source_plate.storage_location_id,
                                                 sample_transfer_template_id)
                destination_plates.append(plate)
                db_session.flush()

                destination_plate = destination_plates[0]

                for source_plate_well in source_plate.wells:

                    destination_plate_well_id = source_plate_well.well_id

                    try:
                        create_well_transfer(
                            db_session, operator, sample_transfer,
                            order_number, source_plate, source_plate_well,
                            destination_plate, destination_plate_well_id,
                            source_plate_well.row, source_plate_well.column
                        )
                    except IndexError as err:
                        return error_response(400, err)

                    order_number += 1

            # source(s) and destination(s) are not the same plate type/layout
            else:

                storage_location_id = source_plates[0].storage_location_id
                target_plate_type_id = templateData["destination"]["plate_type_id"]

                # create the destination plate(s)
                for destination_barcode in destination_barcodes:
                    plate = create_destination_plate(db_session, operator,
                                                     destination_barcode,
                                                     target_plate_type_id,
                                                     storage_location_id,
                                                     sample_transfer_template_id)
                    destination_plates.append(plate)

                db_session.flush()

                plate_well_to_well_maps = templateData["plate_well_to_well_maps"]

                plate_number = 0
                order_number = 1

                for source_plate in source_plates:
                    well_to_well_map = plate_well_to_well_maps[plate_number]

                    plate_number += 1

                    for source_plate_well in source_plate.wells:
                        logging.debug(source_plate_well)

                        map_item = well_to_well_map[source_plate_well.well_id]

                        logging.debug(map_item)

                        destination_plate_well_id = map_item["destination_well_id"]
                        destination_plate_number = map_item["destination_plate_number"]
                        destination_plate = destination_plates[destination_plate_number - 1]

                        plate_map = json_maps["row_column_maps"][target_plate_type_id]

                        row_and_column = plate_map[destination_plate_well_id]

                        logging.debug(destination_plate_well_id, " ", row_and_column)

                        try:
                            create_well_transfer(
                                db_session, operator, sample_transfer,
                                order_number, source_plate, source_plate_well,
                                destination_plate, destination_plate_well_id,
                                row_and_column["row"], row_and_column["column"]
                            )
                            # TO DO: assign non-bogus row and column values)
                        except IndexError as err:
                            return error_response(400, err)

                        order_number += 1

                    db_session.flush()  # insert one plate at time

    return jsonify({
        "success": True
    })


def create_well_transfer(db_session, operator, sample_transfer, order_number,
                         source_plate, source_plate_well,
                         destination_plate, destination_plate_well_id,
                         row, column):
    """helper function for create_step_record"""

    spl = SamplePlateLayout
    existing_sample_plate_layout = db_session.query(spl).filter(and_(
        spl.sample_plate_id == destination_plate.sample_plate_id,
        spl.sample_id == source_plate_well.sample_id,
        spl.well_id == destination_plate_well_id
    )).first()

    # error if there is already a sample in this dest well
    if existing_sample_plate_layout:
        err = ("Plate [%s] already contains "
               "sample %s in well %s") % (
                   destination_plate.external_barcode,
                   source_plate_well.sample_id,
                   source_plate_well.well_id)
        raise IndexError(err)

    # create a row representing a well in the destination plate.
    destination_plate_well = SamplePlateLayout(
        destination_plate.sample_plate_id,
        source_plate_well.sample_id,
        destination_plate_well_id,
        operator.operator_id,
        row,
        column)

    db_session.add(destination_plate_well)

    # Create a row representing a transfer from a well in
    # the "source" plate to a well in the "destination" plate.
    source_to_dest_well_transfer = SampleTransferDetail(
        sample_transfer.id,
        order_number,
        source_plate.sample_plate_id,
        source_plate_well.well_id,
        source_plate_well.sample_id,
        destination_plate.sample_plate_id,
        destination_plate_well.well_id,
        destination_plate_well.sample_id)
    db_session.add(source_to_dest_well_transfer)


def plate_details(sample_plate_barcode, format, basic_data_only=False):

    sample_plate = db.session.query(SamplePlate).filter_by(external_barcode=sample_plate_barcode).first()

    if not sample_plate:
        errmsg = "There is no plate with the barcode: [%s]"
        return error_response(404, errmsg % sample_plate_barcode)

    sample_plate_id = sample_plate.sample_plate_id

    if not sample_plate.sample_plate_type:
        response = {
            "success": False,
            "errorMessage": "Plate with barcode [%s] has no plate type" % (sample_plate_barcode)
        }
        return jsonify(response)

    number_clusters = sample_plate.sample_plate_type.number_clusters

    #print "number_clusters: ", number_clusters

    well_to_col_and_row_mapping_fn = {
        48:get_col_and_row_for_well_id_48,
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

    rows = (
        db.session.query(
            SamplePlate,
            SampleTransfer,
            SampleTransferDetail
        )
        .filter(SampleTransferDetail.source_sample_plate_id == sample_plate_id)
        .filter(SamplePlate.sample_plate_id ==
                SampleTransferDetail.destination_sample_plate_id)
        .filter(SampleTransferDetail.sample_transfer_id == SampleTransfer.id)
        .options(subqueryload(SampleTransfer.sample_transfer_type))
        # .options(subqueryload(SampleTransfer.operator))
        .all()
    )

    this_to_child_task_name = None
    seen=[]
    child_plates=[]
    for child_plate, transfer, details in rows:
        if child_plate.sample_plate_id not in seen:
            seen.append(child_plate.sample_plate_id)
            child_plates.append({
                "externalBarcode":child_plate.external_barcode,
                "dateCreated":str(child_plate.date_created),
                "dateCreatedFormatted":sample_plate.date_created.strftime("%A, %B %d, %Y %I:%M%p")
            })
            this_to_child_task_name = details.sample_transfer.sample_transfer_type.name

    wells = []


    if basic_data_only:
        dbQ = db.session.query(SamplePlateLayout)

    else:
        dbQ = (
            db.session.query(
                SamplePlateLayout,
                GeneAssemblySampleView
            ).filter(SamplePlateLayout.sample_id == GeneAssemblySampleView.sample_id)
        )

    qry = dbQ.filter_by(sample_plate_id=sample_plate_id).order_by(SamplePlateLayout.well_id)
    rows = qry.all()

    sample_view_attrs = (
        'sample_type',
        'sample_date_created',
        'resistance_marker_plan',
        'cloning_process_id_plan',
        'cloning_process_id_actual',
        'sample_name',
        'sample_operator_id',
        'sample_operator_first_and_last_name',
        'sample_description',
        'sample_parent_process_id',
        'sample_status',
        'cor_order_id',
        'cor_order_date',
        'cor_customer_id',
        'cid_institution_id',
        'coi_order_item_id',
        'coi_line_item_number',
        'coi_order_configuration_id',
        'coi_received_datetime',
        'coi_due_datetime',
        'coi_priority',
        'coi_order_item_status_id',
        'coi_order_item_type_id',
        'coi_order_item_delivery_format_id',
        'coi_customer_sequence_num',
        'coi_customer_line_item_id',
        'coi_customer_line_item_description',
        'coi_description',
        'coi_notes',
        'ga_sagi_id',
        'sagi_sag_id',
        'sagi_date_created',
        'sagg_date_created',
        'sagg_fivep_ps_id',
        'sagg_threep_ps_id',
        'sagg_fivep_as_id',
        'sagg_fivep_as_dir',
        'sagg_threep_as_id',
        'sagg_threep_as_dir',
        'gs_sequence_id',
        'gs_seq',
        'gs_name',
        'gs_description'
    )

    if basic_data_only:
        for well in rows:
            wells.append({
                "well_id": well.well_id,
                "column_and_row": well_to_col_and_row_mapping_fn(well.well_id),
                "sample_id": well.sample_id
            })

    else:
        for well, ga in rows:
            well_dict = {
                "well_id": well.well_id,
                "column_and_row": well_to_col_and_row_mapping_fn(well.well_id),
                "sample_id": well.sample_id
            }
            for attr_name in sample_view_attrs:
                val = getattr(ga, attr_name, None)
                if val is not None:
                    val = str(val)
                well_dict[attr_name] = val
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
            "createdBy":str(sample_plate.operator.first_and_last_name),
            "type":str(sample_plate.type_id)
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
        col_header_names = ["","WELL ID", "COL/ROW", "SAMPLE ID"]
        for attr_name in sample_view_attrs:
            col_header_names.append(attr_name)
        cw.writerow(col_header_names)


        for well in wells:
            cols = ["",
                    well["well_id"],
                    well_to_col_and_row_mapping_fn(well["well_id"]),
                    well["sample_id"]
                    ]
            for attr_name in sample_view_attrs:
                cols.append(well[attr_name])
            cw.writerow(cols)

        csvout = si.getvalue().strip('\r\n')

        logger.info(" %s downloaded the PLATE DETAILS REPORT for plate with barcode [%s]" % (g.user.first_and_last_name,sample_plate_barcode))

        # We need to modify the response, so the first thing we
        # need to do is create a response out of the CSV string
        response = make_response(csvout)
        # This is the key: Set the right header for the response
        # to be downloaded, instead of just printed on the browser
        response.headers["Content-Disposition"] = "attachment; filename=Plate_" + sample_plate_barcode + "_Report.csv"
        return response

def source_plate_well_data():
    data = request.json
    plateBarcodes = data["plateBarcodes"]
    plateWellData = {}

    for barcode in plateBarcodes:

        sample_plate = db.session.query(SamplePlate).filter_by(external_barcode=barcode).first()

        if not sample_plate:
            response = {
                "success": False,
                "errorMessage": "There is no plate with the barcode: [%s]" % (barcode)
            }
            return jsonify(response)

        rows = db.session.query(SamplePlateLayout).filter_by(sample_plate_id=sample_plate.sample_plate_id).all()

        well_to_col_and_row_mapping_fn = {
            48:get_col_and_row_for_well_id_48,
            96:get_col_and_row_for_well_id_96,
            384:get_col_and_row_for_well_id_384
        }.get(sample_plate.sample_plate_type.number_clusters,lambda well_id:"missing map")

        wells = {}
        for well in rows:

            col_row = well_to_col_and_row_mapping_fn(well.well_id)

            well_data = {
                "well_id":well.well_id,
                "column_and_row":col_row,
                "sample_id":well.sample_id
            }
            wells[col_row] = well_data;

        plateWellData[barcode] = {
            "wells": wells
        }

    respData = {
        "success": True
        ,"plateWellData": plateWellData
    }
    resp = Response(response=json.dumps(respData),
            status=200, \
            mimetype="application/json")
    return(resp)

def check_plates_are_new():
    data = request.json
    plateBarcodes = data["plateBarcodes"]

    existPlates = [];

    for barcode in plateBarcodes:
        sample_plate = db.session.query(SamplePlate).filter_by(external_barcode=barcode).first()

        if sample_plate:
            existPlates.append(barcode)


    if len(existPlates):
        response = {
                "success": False,
                "errorMessage": "Plates already exist in the database: %s" % (', '.join(existPlates))
            }
        return jsonify(response)

    respData = {
        "success": True
    }
    resp = Response(response=json.dumps(respData),
            status=200, \
            mimetype="application/json")
    return(resp)
