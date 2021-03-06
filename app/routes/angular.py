###############################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
###############################################################################

import csv
import json
import logging
import StringIO
import datetime

from flask import g, make_response, request, Response, jsonify

from sqlalchemy import distinct
from sqlalchemy.orm import subqueryload, aliased
from sqlalchemy.orm.exc import NoResultFound  # , MultipleResultsFound

from app.utils import scoped_session
from app import app, db, googlelogin, constants
from app.plate_to_plate_maps import maps_json
from app.models import create_destination_plate
from app.routes.spreadsheet import create_step_record_adhoc

from twistdb.sampletrack import TransformType, Plate, Transform, \
    TransformDetail, Sample

from well_mappings import (get_col_and_row_for_well_id_48,
                           get_col_and_row_for_well_id_96,
                           get_col_and_row_for_well_id_384)


from logging_wrapper import get_logger
logger = get_logger(__name__)

MAX_SAMPLE_TRANSFORM_QUERY_ROWS = 100000

SAMPLE_VIEW_ATTRS = (
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


def new_home():
    """This is the "home" page, which is actually the "enter a sample movement" page."""
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
        "success": True, "user": user
    }
    resp = Response(response=json.dumps(returnData),
                    status=200, mimetype="application/json")
    return(resp)


def google_login():
    returnData = {
        "login_url": googlelogin.login_url(scopes=['https://www.googleapis.com/auth/userinfo.email'])
    }
    resp = Response(response=json.dumps(returnData),
                    status=200, mimetype="application/json")
    return(resp)


def sample_transform_types():
    sample_transform_types2 = db.session.query(TransformType).\
        order_by(TransformType.menu_ordering)
    simplified_results = []
    for row in sample_transform_types2:
        simplified_results.append({"text": row.name, "id": row.id,
                                   "source_plate_count": row.source_plate_count,
                                   "destination_plate_count": row.destination_plate_count,
                                   "transform_template_id": row.transform_template_id})
    returnData = {
        "success": True, "results": simplified_results
    }

    resp = Response(response=json.dumps(returnData),
                    status=200, mimetype="application/json")
    return(resp)


def sample_plate_barcodes():
    """Returns barcodes for all current sample plates."""
    plates = db.session.query(Plate).order_by(Plate.id).all()

    plate_barcodes = [plate.external_barcode for plate in plates if plate.external_barcode is not None]

    resp = Response(response=json.dumps(plate_barcodes),
                    status=200, mimetype="application/json")
    return(resp)


def update_plate_barcode():

    data = request.json

    plate_id = data["plateId"]
    external_barcode = data["barcode"]

    sample_plate = db.session.query(Plate).filter_by(plate_id=plate_id).first()

    if not sample_plate:
        errmsg = "There is no sample plate with the id: [%s]"
        return error_response(404, errmsg % plate_id)

    #
    # Is there a row in the database that already has this barcode? If so, bail, it is aready in use!
    #
    sample_plate_with_this_barcode = db.session.query(Plate).filter_by(external_barcode=external_barcode).first()
    if sample_plate_with_this_barcode and sample_plate_with_this_barcode.plate_id != sample_plate.id:
        logger.info(" %s encountered an error trying to update the plate with id [%s]. The barcode [%s] is already assigned to the plate with id: [%s]" %
                    (g.user.first_and_last_name, plate_id, external_barcode,
                     sample_plate_with_this_barcode.plate_id))
        errmsg = "The barcode [%s] is already assigned to the plate with id: [%s]"
        return error_response(400, errmsg % (external_barcode, sample_plate_with_this_barcode.plate_id))

    sample_plate.external_barcode = external_barcode
    db.session.commit()
    logging.info("external_barcode: %s", external_barcode)
    response = {
        "success": True
    }

    logger.info(" %s set the barcode [%s] for plate with id [%s]" %
                (g.user.first_and_last_name, external_barcode, plate_id))

    return jsonify(response)


def sample_transforms(limit=MAX_SAMPLE_TRANSFORM_QUERY_ROWS):

    qry = (
        db.session.query(
            Transform,
            TransformDetail
        )
        .options(subqueryload(TransformDetail.source_plate))
        .options(subqueryload(TransformDetail.destination_plate))
        .options(subqueryload(Transform.transform_type))
        .options(subqueryload(Transform.operator))
        .filter(TransformDetail.transform_id == Transform.id)
        .order_by(Transform.date_transform.desc())
    )
    if limit is None:
        rows = qry.all()
    else:
        rows = qry.limit(limit)

    sample_transform_details = []

    seen = []

    for transform, details in rows:
        key = (transform.id,
               details.source_plate_id,
               details.destination_plate_id)
        if key not in seen:
            seen.append(key)
            sample_transform_details.append((transform, details))

    transforms_data = {}

    # and create a serializable data array for the response
    for sample_transform, details in sample_transform_details:
        if (sample_transform.id not in transforms_data):
            transforms_data[sample_transform.id] = {
                "id": sample_transform.id,
                "name": sample_transform.transform_type.name,
                "date": sample_transform.date_transform.strftime("%A, %B %d %Y, %I:%M%p"),
                "operator": sample_transform.operator.first_and_last_name,
                "source_barcodes": [details.source_plate.external_barcode],
                "destination_barcodes": [details.destination_plate.external_barcode]
            }
        else:
            already = False
            for barcode in transforms_data[sample_transform.id]["source_barcodes"]:
                if barcode == details.source_plate.external_barcode:
                    already = True
                    break
            if not already:
                transforms_data[sample_transform.id]["source_barcodes"].append(details.source_plate.external_barcode)
            already = False
            for barcode in transforms_data[sample_transform.id]["destination_barcodes"]:
                if barcode == details.destination_plate.external_barcode:
                    already = True
                    break
            if not already:
                transforms_data[sample_transform.id]["destination_barcodes"].append(details.destination_plate.external_barcode)

    # ugliness here to turn the map created above into an ordered array
    transformsDataArray = []
    for item in transforms_data:
        transformsDataArray.insert(transforms_data[item]['id'], transforms_data[item])

    fullDataArray = []
    for item in transformsDataArray:
        if item is not None:
            fullDataArray.append(item)

    fullDataArray.reverse()

    resp = Response(response=json.dumps(fullDataArray),
                    status=200, mimetype="application/json")
    return(resp)


def create_step_record():
    data = request.json
    operator = g.user

    transform_type_id = data["sampleTransformTypeId"]
    transform_template_id = data["sampleTransformTemplateId"]

    if "transformMap" in data:
        transform_map = data["transformMap"]
        return create_step_record_adhoc(transform_type_id,
                                        transform_template_id,
                                        transform_map)

    else:
        raise NotImplementedError("transformMap is required")

        source_barcodes = data["sourcePlates"]
        destination_barcodes = data["destinationPlates"]

        source_plates = []
        destination_plates = []

        json_maps = maps_json()

        if transform_template_id in json_maps["transform_maps"]:
            templateData = json_maps["transform_maps"][transform_template_id]
        else:
            errmsg = "A template for this transform type (%s) could not be found."
            return error_response(404, errmsg % transform_template_id)

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

            # Create a transform row representing this entire transform.
            sample_transform = Transform(transform_type_id=transform_type_id,
                                         operator_id=operator.operator_id)
            db_session.add(sample_transform)

            for barcode in source_barcodes:
                # load our source plates into an array for looping
                source_plate = db_session.query(Plate).filter_by(external_barcode=barcode).first()
                if not source_plate:
                    errmsg = "There is no source plate with the barcode: %s"
                    errmsg %= barcode
                    logger.info(" %s encountered error creating transform: " %
                                g.user.first_and_last_name + errmsg)
                    return error_response(404, errmsg)
                source_plates.append(source_plate)

            # the easy case: source and destination plates have same layout and there's only 1 of each
            if transform_template_id == 1:

                order_number = 1
                source_plate = source_plates[0]

                # create the destination plate
                logging.warning("FOUND DEST BC: %s" % destination_barcodes[0])
                plate = create_destination_plate(db_session, operator,
                                                 destination_barcodes[0],
                                                 source_plate.type_id,
                                                 source_plate.storage_location,
                                                 transform_template_id)
                destination_plates.append(plate)
                db_session.flush()

                destination_plate = destination_plates[0]

                for source_plate_well in source_plate.wells:

                    destination_plate_well_id = source_plate_well.well_id

                    try:
                        create_well_transform(
                            db_session, operator, sample_transform,
                            order_number, source_plate, source_plate_well,
                            destination_plate, destination_plate_well_id,
                            source_plate_well.row, source_plate_well.column
                        )
                    except IndexError as err:
                        return error_response(400, err)

                    order_number += 1

            # source(s) and destination(s) are not the same plate type/layout
            else:

                storage_location = source_plates[0].storage_location
                target_plate_type_id = templateData["destination"]["plate_type_id"]

                # create the destination plate(s)
                for destination_barcode in destination_barcodes:
                    plate = create_destination_plate(db_session, operator,
                                                     destination_barcode,
                                                     target_plate_type_id,
                                                     storage_location,
                                                     transform_template_id)
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
                            create_well_transform(
                                db_session, operator, sample_transform,
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


def create_well_transform(db_session, operator, sample_transform, order_number,
                          source_plate, source_plate_well,
                          destination_plate, destination_plate_well_id,
                          row, column):
    """helper function for create_step_record"""

    try:
        existing_well_sample = db_session.query(Sample).filter(
            Sample.plate_id == destination_plate.id,
            Sample.id == source_plate_well.id,
            Sample.well.well_number == destination_plate_well_id
        ).one()
    except:
        pass

    # error if there is already a sample in this dest well
    if existing_well_sample:
        err = ("Plate [%s] already contains "
               "sample %s in well %s") % (
                   destination_plate.external_barcode,
                   source_plate_well.sample_id,
                   source_plate_well.well_id)
        raise IndexError(err)

    source_well_sample = db_session.query(Sample).filter(
        Sample.plate_id == source_plate.id,
        Sample.id == source_plate_well.id,
        Sample.plate_well_code == source_plate_well.plate_well_code
    ).order_by(Sample.date_created.desc()).first()

    if not source_well_sample:
        err = ("Plate [%s] has no sample %s in well %s") % \
            (source_plate.external_barcode,
             source_plate_well.sample_id,
             source_plate_well.well_id)
        raise IndexError(err)

    # create a row representing a well in the destination plate.
    # FIXME this is wrong but unclear if this method is in use?
    destination_well_sample = Sample(plate_id=destination_plate.id,
                                     id=source_plate_well.sample_id,
                                     well_id=destination_plate_well_id,
                                     operator_id=operator.operator_id)
    db_session.add(destination_well_sample)

    # Create a row representing a transform from a well in
    # the "source" plate to a well in the "destination" plate.
    # FIXME change to model just the parent/child relationship
    source_to_dest_well_transform = TransformDetail(
        transform_id=sample_transform.id,  # item_order_number=order_number,
        source_plate_id=source_plate.id,
        source_well_id=source_plate_well.well_id,
        source_sample_id=source_plate_well.sample_id,
        destination_plate_id=destination_plate.id,
        destination_well_id=destination_well_sample.well.well_number,
        destination_sample_id=destination_well_sample.id)
    db_session.add(source_to_dest_well_transform)
    db_session.flush()

    # Old attempt at normalizing TransferDetail:
    # aliquot = Aliquot(transform_id=sample_transform.id,
    #                   source_well_sample_id=source_well_sample.id,
    #                   destination_well_sample_id=destination_well_sample.id)
    # db_session.add(aliquot)
    # db_session.flush()


def plate_details(sample_plate_barcode, fmt, basic_data_only=True):
    import time
    start = time.time()

    try:
        sample_plate = db.session.query(Plate).filter(
            Plate.external_barcode == sample_plate_barcode).one()
    except NoResultFound:
        errmsg = "There is no plate with the barcode: [%s]"
        return error_response(404, errmsg % sample_plate_barcode)

    # if fmt == 'csv':
    #     # FIXME: frontend should call different methods for Download Excel
    #     # (csv) vs. check existence (name check)
    #     basic_data_only = False

    if not sample_plate.plate_type:
        response = {
            "success": False,
            "errorMessage": "Plate with barcode [%s] has no plate type" % (sample_plate_barcode)
        }
        return jsonify(response)

    # ORIGINAL QUERY
    # rows = db.session.query(Plate, TransformDetail).filter(
    #     TransformDetail.destination_plate_id == plate_id,
    #     Plate.id == TransformDetail.source_plate_id).all()

    child_pids = []
    parent_pids = []

    # Query for parent plates
    ParentSample = aliased(Sample)
    ChildSample = aliased(Sample)
    for plate in db.session.query(distinct(ParentSample.plate_id) ) \
            .join(TransformDetail,
                  TransformDetail.parent_sample_id == ParentSample.id ) \
            .filter(ParentSample.plate_id != sample_plate.id ) \
            .join(ChildSample,
                  TransformDetail.child_sample_id == ChildSample.id ) \
            .filter(ChildSample.plate_id == sample_plate.id):
        parent_pids.append(plate)

    parent_plates = []
    if parent_pids:
        parent_plates = db.session.query(Plate).\
            filter(Plate.id.in_(parent_pids)).all()

    # Query for child plates
    for plate in db.session.query(distinct(ChildSample.plate_id) ) \
            .join(TransformDetail,
                  TransformDetail.child_sample_id == ChildSample.id ) \
            .filter(ChildSample.plate_id != sample_plate.id ) \
            .join(ParentSample,
                  TransformDetail.parent_sample_id == ParentSample.id ) \
            .filter(ParentSample.plate_id == sample_plate.id):
        child_pids.append(plate)

    child_plates = []
    if child_pids:
        child_plates = db.session.query(Plate).\
            filter(Plate.id.in_(child_pids)).all()

    wells = []
    this_to_child_task_name = None
    parent_to_this_task_name = None
    for s in sample_plate.current_well_contents(db.session):
        wells.append({"well_id": s.well.well_number,
                      "column_and_row": s.well.well_label,
                      "sample_id": s.id
                      })

    # Look at all the parent plates for this sample
    parent_info = []
    for parent in parent_plates:
        parent_info.append({
            "externalBarcode": parent.external_barcode,
            "dateCreated": str(parent.date_created),
            "dateCreatedFormatted":
                parent.date_created.strftime("%A, %B %d, %Y %I:%M%p")
        })

    # if s.transform:
    #     parent_to_this_task_name = s.transform.transform_type.name

    # Look at all the child plates for this sample
    child_info = []
    for child in child_plates:
        child_info.append({
            "externalBarcode": child.external_barcode,
            "dateCreated": str(child.date_created),
            "dateCreatedFormatted":
                child.date_created.strftime("%A, %B %d, %Y %I:%M%p")
        })

    # if child.transform:
    #     this_to_child_task_name = child.transform.transform_type.name

    report = {
        "success": True,
        "parentPlates": parent_info,
        "parentToThisTaskName": parent_to_this_task_name,
        "childPlates": child_info,
        "thisToChildTaskName": this_to_child_task_name,
        "wells": wells,
        "plateDetails": {
            "dateCreated": str(sample_plate.date_created),
            "dateCreatedFormatted": sample_plate.date_created.strftime("%A, %B %d, %Y %I:%M%p"),
            "createdBy": str(sample_plate.operator.first_and_last_name),
            "type": str(sample_plate.type_id)
        }
    }

    logger.info("Plate info took: " + str(time.time() - start))

    if fmt == "json":
        resp = Response(response=json.dumps(report),
                        status=200, mimetype="application/json")
        return(resp)

    elif fmt == "csv":

        raise NotImplementedError

        si = StringIO.StringIO()
        cw = csv.writer(si)

        cw.writerow(["PLATE REPORT"])
        cw.writerow("")
        cw.writerow("")
        cw.writerow(["","PLATE BARCODE", "CREATION DATE/TIME", "CREATED BY"])
        cw.writerow("")
        cw.writerow(["",sample_plate_barcode, report["plateDetails"]["dateCreatedFormatted"],report["plateDetails"]["createdBy"]])

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
        for attr_name in SAMPLE_VIEW_ATTRS:
            col_header_names.append(attr_name)
        cw.writerow(col_header_names)

        for well in wells:
            cols = ["",
                    well["well_id"],
                    "TBD",
                    # well_to_col_and_row_mapping_fn(well["well_id"]),
                    well["sample_id"]
                    ]
            for attr_name in SAMPLE_VIEW_ATTRS:
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

        sample_plate = db.session.query(Plate).filter_by(external_barcode=barcode).first()

        if not sample_plate:
            response = {
                "success": False,
                "errorMessage": "There is no plate with the barcode: [%s]" % (barcode)
            }
            return jsonify(response)

        samples = sample_plate.current_well_contents(db.session)

        wells = {}
        for sample in samples:
            well = sample.well

            well_data = {
                "well_id": well.well_number,
                "column_and_row": well.well_label,
                "sample_id": sample.id
            }
            wells[well.well_label] = well_data

        plateWellData[barcode] = {
            "wells": wells
        }

    respData = {
        "success": True,
        "plateWellData": plateWellData
    }
    resp = Response(response=json.dumps(respData),
                    status=200, mimetype="application/json")
    return(resp)


def check_plates_are_new():
    data = request.json
    plateBarcodes = data["plateBarcodes"]

    existPlates = []
    for barcode in plateBarcodes:
        try:
            sample_plate = db.session.query(Plate).filter(
                Plate.external_barcode == barcode).one()

            if sample_plate:
                existPlates.append(barcode)
        except NoResultFound:
            pass

    if len(existPlates):
        response = {
            "success": False,
            "errorMessage": "Plates already exist in the database: %s" %
                            (', '.join(existPlates))
        }
        return jsonify(response)

    respData = {
        "success": True
    }
    resp = Response(response=json.dumps(respData),
                    status=200, mimetype="application/json")
    return(resp)

##################
# ### Hamailton operation endpoints
##################

hamiltons = constants.HAMILTONS
carriers = constants.CARRIERS


def get_hamilton_by_barcode(hamilton_barcode):

    if hamilton_barcode in hamiltons:
        respData = hamiltons[hamilton_barcode]
    else:
        errmsg = "There is no Hamilton with the barcode: [%s]"
        return error_response(404, errmsg % hamilton_barcode)

    resp = Response(response=json.dumps(respData),
                    status=200, mimetype="application/json")
    return(resp)


def get_carrier_by_barcode(carrier_barcode, hamilton_barcode):

    if carrier_barcode in carriers:
        respData = carriers[carrier_barcode]
    else:
        errmsg = "There is no carrier with the barcode: [%s]"
        return error_response(404, errmsg % carrier_barcode)

    resp = Response(response=json.dumps(respData),
                    status=200, mimetype="application/json")
    return(resp)


def get_plate_ready_for_step(plate_barcode, transform_type_id):

    if plate_barcode:
        respData = True
    else:
        errmsg = "This plate is not ready for transform type [%s]"
        return error_response(404, errmsg % transform_type_id)

    resp = Response(response=json.dumps(respData),
                    status=200, mimetype="application/json")
    return(resp)


def process_hamilton_sources(transform_type_id):

    transform_type_id = int(transform_type_id)

    respData = {
        "responseCommands": []
    }

    if transform_type_id == constants.TRANS_TYPE_HITPICK_MINIPREP:
        '''
        this code needs to actually analyze the wells in the plates of plateBarcodes
        and build a Hamilton worklist to hitpick into necessary # of destination plates.
        '''

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"}
                ]
            }
        )

    elif transform_type_id == constants.TRANS_TYPE_HITPICK_SHIP_PLATES:
        '''
        this code needs to actually analyze the wells in the plates of plateBarcodes
        and build a shipping worklist to hitpick into necessary # of destination plates.
        '''

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"}
                ]
            }
        )

    elif transform_type_id == constants.TRANS_TYPE_HITPICK_SHIP_TUBES:
        '''
        this code needs to actually analyze the wells in the plates of plateBarcodes
        and build a shipping worklist to hitpick into necessary # of destination tubes.
        '''

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [  # front end just uses length of plates array
                    {"type": "SHIPPING_TUBE_PLATE"},
                    {"type": "SHIPPING_TUBE_PLATE"},
                    {"type": "SHIPPING_TUBE_PLATE"}
                ]
            }
        )

        respData["responseCommands"].append(
            {
                "type": "ADD_TRANSFORM_SPEC_DETAIL",
                "detail": {
                    "key": "shippingTubeBarcodeData",
                    "value": [
                        {"forWellNumber": 1, "COI": "TUBE01", "itemName": "ordered tube item",
                         "partNumber": "12345ABCD", "labelMass": "1 ug"},
                        {"forWellNumber": 2, "COI": "TUBE02", "itemName": "ordered tube item",
                         "partNumber": "6789GHIJ", "labelMass": "1 ug"},
                        {"forWellNumber": 3, "COI": "TUBE03", "itemName": "ordered tube item",
                         "partNumber": "3456MNOP", "labelMass": "1 ug"}
                    ]
                }
            }
        )

    elif transform_type_id == constants.TRANS_TYPE_PCA_PCR_ADD_MMIX:
        '''
        this code needs to actually analyze the wells in the plates of plateBarcodes
        and build a master mix addition worklist AND needs to determine where the 4 destination plates should be placed.
        It will return the SET_DESTINATIONS command as-is below.
        The ADD_TRANSFORM_SPEC_DETAIL should be the array of 4 destination plates with their forPosition and barcode properties set accordingly
        '''

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"}
                ]
            }
        )
        respData["responseCommands"].append(
            {
                "type": "ADD_TRANSFORM_SPEC_DETAIL",
                "detail": {
                    "key": "guidedDestinationPlacementData",
                    "value": [
                        {"forPosition": 1, "barcode": "TUBE01"},
                        {"forPosition": 2, "barcode": "TUBE02"},
                        {"forPosition": 3, "barcode": "TUBE03"},
                        {"forPosition": 4, "barcode": "TUBE04"}
                    ]
                }
            }
        )

    elif transform_type_id == constants.TRANS_TYPE_ECR_PCR_MASTER_MIX_ADDITION:
        '''
        this code needs to actually analyze the wells in the plates of plateBarcodes
        and build a master mix addition worklist AND needs to determine where the 4 destination plates should be placed.
        It will return the SET_DESTINATIONS command as-is below.
        The ADD_TRANSFORM_SPEC_DETAIL should be the array of 4 destination plates with their forPosition and barcode properties set accordingly
        '''

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"}
                ]
            }
        )
        respData["responseCommands"].append(
            {
                "type": "ADD_TRANSFORM_SPEC_DETAIL",
                "detail": {
                    "key": "guidedDestinationPlacementData",
                    "value": [
                        {"forPosition": 1, "barcode": "TUBE01"},
                        {"forPosition": 2, "barcode": "TUBE02"},
                        {"forPosition": 3, "barcode": "TUBE03"},
                        {"forPosition": 4, "barcode": "TUBE04"}
                    ]
                }
            }
        )

    elif transform_type_id == constants.TRANS_TYPE_POST_PCA_NORM:
        '''
        this code needs to actually analyze the wells in the plates of plateBarcodes
        and build nornalization worklist for the source plate.
        '''

    elif transform_type_id == constants.TRANS_TYPE_PCA_PCR_PURIFICATION:

        # REAL code needed here to decide on destinations

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"}
                ]
            }
        )

    elif transform_type_id == constants.TRANS_TYPE_ECR_PCR_PURIFICATION:

        # REAL code needed here to decide on destinations

        respData["responseCommands"].append(
            {
                "type": "SET_DESTINATIONS",
                "plates": [
                    {"type": "SPTT_0006"},
                    {"type": "SPTT_0006"}
                ]
            }
        )

    resp = Response(response=json.dumps(respData),
                    status=200, mimetype="application/json")
    return(resp)


def trash_samples():

    data = request.json
    sampleIds = data["sampleIds"]

    respData = {
        "all_trashed": True
    }


def get_worklist(spec_id):
    response = make_response("****** worklist data for transform spec %s ******" % spec_id)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment;"
    return response


def get_date_time():
    resp = Response(response=json.dumps({"date": str(datetime.datetime.utcnow())}),
                    status=200, mimetype="application/json")
    return(resp)
