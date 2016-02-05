##############################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: app/routes/spreadsheet.py
#
# These are the handlers for all spreadsheet related
# JSON/REST API routes used by this application.
#
##############################################################################
import logging
from datetime import datetime

from flask import g, jsonify
from sqlalchemy import and_
from sqlalchemy.sql import func

from app import app, db
from app.utils import scoped_session
from app.models import create_destination_plate
from twistdb.public import *
from twistdb.sampletrack import *
from twistdb.ngs import *
from twistdb.sampletrack import Sample
from app.dbmodels import NGS_BARCODE_PLATE, NGS_BARCODE_PLATE_TYPE

from twistdb import create_unique_id

from well_mappings import (get_col_and_row_for_well_id_48,
                           get_well_id_for_col_and_row_48,
                           get_col_and_row_for_well_id_96,
                           get_well_id_for_col_and_row_96,
                           get_col_and_row_for_well_id_384,
                           get_well_id_for_col_and_row_384,
                           get_well_id_for_col_and_row_6144)
from well_count_to_plate_type_name import well_count_to_plate_type_name

IGNORE_MISSING_SOURCE_PLATE_WELLS = True  # FIXME: this allows silent failures


# FIXME: there are a bunch of model instantiations in this thing, and they're
#   all gonna break with the new twistdb models
#   -- kieran


def error_response(status_code, message):
    # TODO: remove duplicate code -- use JSON-API?
    response = jsonify({'success': False, 'message': message})
    response.status_code = status_code
    return response

#
# If the user uploaded a spreadsheet with each row representing a well-to-well transfer, this is where we
# process that spreadsheet data.
#


def create_step_record_adhoc(transfer_type_id,
                             transfer_template_id,
                             wells):

    with scoped_session(db.engine) as db_session:
        result = create_adhoc_sample_movement(db_session,
                                              transfer_type_id,
                                              transfer_template_id,
                                              wells)
        if result["success"]:
            return jsonify({
                "success": True
            })
        else:
            return error_response(400, result["errorMessage"])


def create_adhoc_sample_movement(db_session,
                                 transfer_type_id,
                                 transfer_template_id, wells,
                                 transform_spec_id=None):
    #
    # FIRST. Create a "sample_transfer" row representing this row's transfer.
    #
    operator = g.user
    sample_transfer = Transfer(transfer_type_id=transfer_type_id,
                                     transform_spec_id=transform_spec_id,
                                     operator_id=operator.operator_id)
    db_session.add(sample_transfer)
    db_session.flush()

    destination_plates_by_barcode = {}
    sample_plate_types_by_name = {}

    #
    # NEXT: Now, do the transfer for each source-plate-well to each destination-plate-well...
    #
    order_number = 1

    well_from_col_and_row_methods = {
        "48": get_well_id_for_col_and_row_48,
        "96": get_well_id_for_col_and_row_96,
        "384": get_well_id_for_col_and_row_384,
        "6144": get_well_id_for_col_and_row_6144
    }

    for ix, well in enumerate(wells):
        source_plate_barcode = well["source_plate_barcode"]
        source_col_and_row = well["source_well_name"]
        destination_plate_barcode = well["destination_plate_barcode"]
        destination_col_and_row = well["destination_well_name"]
        destination_well_count = str(well["destination_plate_well_count"])
        destination_sample_id = well.get("destination_sample_id", None)

        #print "WELL: ", well

        #print "DEST WELL COUNT: ", destination_well_count

        #
        # well_count_to_plate_type_name
        #

        #if destination_well_count and destination_well_count.strip() != "":
            #print "USING well count rather than destination plate type name"
            #destination_well_count = "invalid"
        destination_plate_type_name = well_count_to_plate_type_name.get(
            destination_well_count.strip(), None)
        logging.info("Calculated destination_plate_type_name: "
                     "%s from well count: %s",
                     destination_plate_type_name, destination_well_count)

        if not destination_plate_type_name:
            return {
                "success": False,
                "errorMessage": "There is no plate type with %s wells" % (destination_well_count)
            }

        #
        logging.warn("1. Obtain access to the source plate for this line item.")
        #
        source_plate = db_session.query(Plate).filter_by(external_barcode=source_plate_barcode).first()

        if not source_plate:
            logging.info(" %s encountered error creating sample transfer. "
                         "There is no source plate with the barcode: [%s]",
                         g.user.first_and_last_name, source_plate_barcode)
            return {
                "success": False,
                "errorMessage": "There is no source plate with the barcode: [%s]" % (source_plate_barcode)
            }

        #
        # 96 well, plastic
        #
        sample_plate_type = source_plate.sample_plate_type
        plate_size = None
        if sample_plate_type.name == "48 well, plastic":
            plate_size = "48"
        elif sample_plate_type.name == "96 well, plastic":
            plate_size = "96"
        elif sample_plate_type.name == "384 well, plastic":
            plate_size = "384"
        elif sample_plate_type.name == "6144 well, silicon, Titin":
            plate_size = "6144"
        else:
            plate_size = None

        # print "\n\nSOURCE PLATE, barcode: %s  plate type: [%s]" % (#source_plate.external_barcode,sample_plate_type.name)
        logging.info("SOURCE PLATE, barcode: %s  plate type: [%s]",
                     source_plate.external_barcode, sample_plate_type.name)

        source_col_and_row = source_col_and_row.strip()

        # if source_well_id is None or source_well_id.strip() == "":
        if plate_size is None:
            return {
                "success": False,
                "errorMessage": "You must specify a SOURCE well id. Currently this app only has wellid-to-col/row mappings for 96 and 384 size plates and the source plate is this type: [%s]" % (sample_plate_type.name)
            }
        else:
            logging.info("source_col_and_row: %s", source_col_and_row)
            try:
                source_well_id = int(source_col_and_row)
            except ValueError:
                source_well_id = well_from_col_and_row_methods[plate_size](source_col_and_row)
            logging.info("calculated source well id: %s from "
                         "plate size: %s and column/row: %s",
                         source_well_id, plate_size, source_col_and_row)

        # else:
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

        # print "source plate barcode [%s]" % (source_plate_barcode)
        storage_location_id = source_plate.storage_location_id

        #
        # 2. Obtain (or create if we haven't yet grabbed it) the sample plate type row for the type of plate
        # specified for the destination of this line item.
        #
        sample_plate_type = sample_plate_types_by_name.get(destination_plate_type_name)
        if not sample_plate_type:
            sample_plate_type = db_session.query(PlateType).filter_by(name=destination_plate_type_name).first()
            if sample_plate_type:
                sample_plate_types_by_name[destination_plate_type_name] = sample_plate_type
            else:
                logging.info(" %s encountered error creating sample "
                             "transfer. There are no sample plates with "
                             "the type: [%s]",
                             g.user.first_and_last_name,
                             destination_plate_type_name)
                return {
                    "success": False,
                    "errorMessage": "There are no sample plates with the type: [%s]" % (destination_plate_type_name)
                }

        #
        # 3. Obtain (or create if we haven't yet added a row for it in the database) the row for this well-to-well
        # transfer's destination plate.
        # - It may be new, in which case we create a new plate orm object.
        # - We may have created it on a previous loop iteration.
        # - It may already exist in the database, if in_place_transform.
        # - It may already exist in the database, if merge_transform.

        merge_transform_flag = (source_plate_barcode == NGS_BARCODE_PLATE)

        in_place_transform_flag = (destination_plate_barcode == source_plate_barcode)

        destination_plate = destination_plates_by_barcode.get(destination_plate_barcode)

        if not destination_plate:

            if merge_transform_flag:
                # TODO: add lots more kinds of merge transforms.
                destination_plate = db_session.query(Plate).filter_by(external_barcode=destination_plate_barcode).first()

                if not destination_plate:
                    logging.info(" %s encountered error creating sample transfer. "
                                 "There is no destination plate with the barcode: [%s]",
                                 g.user.first_and_last_name, destination_plate_barcode)
                    return {
                        "success": False,
                        "errorMessage": "There is no destination plate with the barcode: [%s]" % (destination_plate_barcode)
                    }

            elif in_place_transform_flag:
                # BUGFIX 11/17/2015: for in-place transforms,
                # don't create a new plate!
                # TODO: clarify same-same transfer destination plate.
                destination_plate = source_plate

            else:
                try:
                    destination_plate = create_destination_plate(
                        db_session,
                        operator,
                        destination_plate_barcode,
                        sample_plate_type.type_id,
                        storage_location_id,
                        transfer_template_id)
                    db_session.flush()
                except IndexError:
                    err_msg = ("Encountered error creating sample "
                               "transfer. Could not create destination plate: [%s]"
                               )
                    logging.info(err_msg, destination_plate_barcode)
                    return {
                        "success": False,
                        "errorMessage": err_msg % destination_plate_barcode
                    }

            destination_plates_by_barcode[destination_plate_barcode] = destination_plate

        #
        logging.warn('4. Get the "source plate well"')
        #

        source_plate_well = db_session.query(PlateLayout).filter(and_(
            PlateLayout.sample_plate_id==source_plate.sample_plate_id,
            PlateLayout.well_id==source_well_id
        )).first()

        # print "SOURCE PLATE WELL: %s " % str(source_plate_well)
        logging.info("SOURCE PLATE WELL: %s (%s, %s) ", source_plate_well,
                     source_plate.sample_plate_id, source_well_id)

        if sample_plate_type.name == "48 well, plastic":
            plate_size = "48"
        elif sample_plate_type.name == "96 well, plastic":
            plate_size = "96"
        elif sample_plate_type.name == "384 well, plastic":
            plate_size = "384"
        else:
            plate_size = None

        if not source_plate_well and not merge_transform_flag:
            error_well_id = source_well_id
            if plate_size:
                if plate_size == "48":
                    try:
                        error_well_id = get_col_and_row_for_well_id_48(source_well_id)
                    except:
                        error_well_id = source_well_id
                elif plate_size == "96":
                    try:
                        error_well_id = get_col_and_row_for_well_id_96(source_well_id)
                    except:
                        error_well_id = source_well_id
                elif plate_size == "384":
                    try:
                        error_well_id = get_col_and_row_for_well_id_384(source_well_id)
                    except:
                        error_well_id = source_well_id

            msg = "There is no well [%s] in the source plate with barcode: [%s]" % (error_well_id, source_plate_barcode)
            if IGNORE_MISSING_SOURCE_PLATE_WELLS:
                logging.warn(msg)
                continue
            else:
                logging.error(msg)
                return {
                    "success": False,
                    "errorMessage": msg
                }



        #print "DESTINATION PLATE TYPE: ",sample_plate_type.name

        print "DESTINATION PLATE, barcode: %s  plate type: [%s]" % (destination_plate.external_barcode,sample_plate_type.name)
        logging.info("DESTINATION PLATE, barcode: %s  plate type: [%s]",destination_plate.external_barcode,sample_plate_type.name)

        #if destination_well_id is None or destination_well_id.strip() == "":
        if plate_size is None:
            return {
                "success":False,
                "errorMessage":"You must specify a DESTINATION well id. Currently this app only has wellid-to-col/row mappings for 96 and 384 size plates and the source plate is this type: [%s]" % (sample_plate_type.name)
            }
        else:
            try:
                destination_well_id = well_from_col_and_row_methods[plate_size](destination_col_and_row)
            except KeyError:
                return {
                    "success":False,
                    "errorMessage":"Destination plate well mapping failed."
                }
            logging.info("calculated DEST well id: %s from plate size: %s and column/row: %s", destination_well_id, plate_size,
                         destination_col_and_row)
            print "calculated DEST well id: %s from plate size: %s and column/row: %s" % (destination_well_id,plate_size, destination_col_and_row)


        #print "DEST WELL ID: ", destination_well_id

        print '@@ querying PlateLayout sample_plate_id: %s, PlateLayout.well_id: %s' \
            % (destination_plate.sample_plate_id, destination_well_id)
        existing_plate_layout = db_session.query(PlateLayout) \
                                                 .filter( PlateLayout.sample_plate_id==destination_plate.sample_plate_id,
                                                          # PlateLayout.sample_id==source_plate_well.sample_id,
                                                          PlateLayout.well_id==destination_well_id ) \
                                                 .first()
        print '@@ got:', existing_plate_layout

        #existing_plate_layout = True

        if in_place_transform_flag:
            if not existing_plate_layout:
                return {
                "success":False,
                "errorMessage":"This in-place-transform destination plate [%s] contains no sample in well [%s]" % (destination_plate.external_barcode,
                    source_plate_well.well_id)
                }
        elif  merge_transform_flag:
            if not existing_plate_layout:
                return {
                "success":False,
                "errorMessage":"This merge-transform destination plate [%s] contains no sample in well [%s]" % (destination_plate.external_barcode,
                    source_plate_well.well_id)
                }
        elif existing_plate_layout:
            # still wanted in context of in-place transforms and merge transforms?
            return {
                "success":False,
                "errorMessage":"This destination plate [%s] already contains sample [%s] in well [%s]" % (destination_plate.external_barcode,
                    source_plate_well.sample_id,source_plate_well.well_id)
            }

        #
        logging.warn("4.  Set destination_sample_id.  Accession cloned_sample if necessary.")
        #
        if not destination_sample_id:
            destination_sample_id = sample_handler(db_session,
                                                   transfer_type_id,
                                                   source_plate_well,
                                                   destination_well_id)

        #
        # 5. Create a row representing a well in the desination plate.
        #

        #
        # FIXED: 7/17/15
        #
        # WRONG! Was depositing in source well id not dest well idn destination_plate_well = PlateLayout(destination_plate.sample_plate_id,
        #    source_plate_well.sample_id,source_plate_well.well_id,operator.operator_id,
        #    source_plate_well.row,source_plate_well.column)
        #db_session.add(destination_plate_well)

        if in_place_transform_flag or merge_transform_flag:
            destination_plate_well = existing_plate_layout
            if destination_plate_well.sample_id != destination_sample_id:
                destination_plate_well.sample_id = destination_sample_id  # TODO: is this even necessary orm-wise?
            destination_plate_well.operator_id = operator.operator_id  # unfortunately this will wipe out the old operator_id
            #if destination_sample_id != source_plate_well.sample_id:
                #source_plate_well.sample_id = destination_sample_id # ???? WRONG! ??
                #db_session.flush()
        else:
            destination_plate_well = PlateLayout( sample_plate_id=destination_plate.sample_plate_id,
                                                        sample_id=destination_sample_id, well_id=destination_well_id,
                                                        operator_id=operator.operator_id, row=source_plate_well.row,
                                                        column=source_plate_well.column)
            db_session.add(destination_plate_well)

        # print "DESTINATION PLATE WELL: %s " % (str(destination_plate_well))
        logging.warn("DESTINATION PLATE WELL: %s ", destination_plate_well)

        #
        logging.warn("6. Create a row representing a transfer from a well in the 'source' plate to a well")
        # in the "desination" plate.
        #
        source_to_destination_well_transfer = TransferDetail( sample_transfer_id=sample_transfer.id,
                                                                    item_order_number=order_number,
                                                                    source_sample_plate_id=source_plate_well.sample_plate_id,
                                                                    source_well_id=source_plate_well.well_id,
                                                                    source_sample_id=source_plate_well.sample_id,
                                                                    destination_sample_plate_id=destination_plate_well.sample_plate_id,
                                                                    destination_well_id=destination_plate_well.well_id,
                                                                    destination_sample_id=destination_plate_well.sample_id)
        db_session.add(source_to_destination_well_transfer)
        db_session.flush()

        order_number += 1

    # db_session.rollback()
    # return {
    #     "success":False,
    #     "errorMessage":"testing!!!"
    # }

    db_session.commit()

    return {
        "success":True
    }

def sample_handler(db_session, transfer_type_id,
                        source_plate_well, destination_well_id):
    if transfer_type_id in (15, 16):  # QPix To 96/384 plates
        return make_cloned_sample(db_session,
                                  source_plate_well.sample_id,
                                  destination_well_id)
    else:
        return source_plate_well.sample_id  # no new sample


def make_cloned_sample(db_session, source_sample_id, destination_well_id):
    operator = g.user
    source_id = create_unique_id("tmp_src_")()
    colony_name = "%d-%s" % (12, destination_well_id)

    # Create CS
    cs_id = create_unique_id("CS_")()

    cloned_sample =       Sample(sample_id=cs_id,
                                 parent_sample_id=source_sample_id,
                                 source_id=source_id,
                                 colony_name=colony_name,
                                 operator_id=operator.operator_id)

    # Add CLO
    clo = None

    # TODO: determine how to fetch the desired production cloning
    # process for this sample / cluster_design / order item.
    # For now, just look up the sample, and use a hardcoded
    # cloning process of Twist31 / Amp / 'CLO_564c1af300bc150fa632c63d'

    name = 'cs_' + source_id  # FIXME: determine some more meaningful name
    qry = (
        db.session.query(Sample)
        .filter_by(sample_id=source_sample_id)
    )
    result = qry.first()
    if not result:
        # The alpha code looked up the "cloning plan" from a database view
        # ga_view = result
        # clo = ga_view.cloning_process_id_plan

        clo = 'CLO_564c1af300bc150fa632c63d'  # FIXME: hardcoded Amp for warp 1
        # name = 'CS for ' + str(source_sample_id)  # for warp 1, just keep same name

    cloned_sample.parent_process_id = clo
    logging.info('CS_ID %s for %s assigned cloning_process_id [%s]',
                 cs_id, source_sample_id, clo)
    cloned_sample.name = name

    db_session.add(cloned_sample)
    db_session.flush()

    return cs_id


def make_ngs_prepped_sample(db_session, source_plate_well,
                            destination_well_id):
    operator = g.user

    # Create NPS
    nps_id = create_unique_id("NPS_")()
    i5_sequence_id, i7_sequence_id = "i5a", "i7b"
    insert_size_expected = 1000
    parent_process_id = None
    external_barcode = None
    reagent_type_set_lot_id = None
    status = None
    parent_transfer_process_id = None
    # FIXME: we should just leave notes & description blank, no?
    nps_sample = NGSPreppedSample( sample_id=nps_id, parent_sample_id=source_plate_well.sample_id,
                                   description="temp nps description", i5_sequence_id=i5_sequence_id,
                                   i7_sequence_id=i7_sequence_id, notes="temp nps notes",
                                   insert_size_expected=insert_size_expected, date_created=datetime.utcnow(),
                                   operator_id=operator.operator_id, parent_process_id=parent_process_id,
                                   external_barcode=external_barcode,
                                   reagent_type_set_lot_id=reagent_type_set_lot_id,
                                   parent_transfer_process_id=parent_transfer_process_id)

    logging.info('NPS_ID %s for %s assigned [%s, %s]',
                 nps_id, source_plate_well.sample_id,
                 i5_sequence_id, i7_sequence_id)

    db_session.add(nps_sample)
    db_session.flush()

    return nps_id
