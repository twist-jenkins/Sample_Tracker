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

from flask import g, jsonify
from flask_login import current_user

from app import db, constants
from app.utils import scoped_session
from app.models import create_destination_plate
from app.dbmodels import NGS_BARCODE_PLATE  # , NGS_BARCODE_PLATE_TYPE

from twistdb import create_unique_id
from twistdb.sampletrack import (Sample, Plate, PlateWell, Transfer,
                                 PlateType, TransferDetail)

IGNORE_MISSING_SOURCE_PLATE_WELLS = True  # FIXME: this allows silent failures

logger = logging.getLogger(name="Spreadsheet")


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

    #
    # NEXT: Now, do the transfer for each source-plate-well to each destination-plate-well...
    #
    order_number = 1

    for ix, well in enumerate(wells):
        source_plate_barcode = well["source_plate_barcode"]
        source_well_number = well['source_well_number']
        destination_plate_barcode = well["destination_plate_barcode"]
        destination_well_number = well['destination_well_number']
        # destination_sample_id = well.get("destination_sample_id", None)
        destination_plate_type = well['destination_plate_type']

        logging.info("1. Obtain access to the source plate for this line item.")
        try:
            source_plate = db_session.query(Plate).\
                filter(Plate.external_barcode == source_plate_barcode).one()
        except:
            logging.warn(" %s encountered error creating sample transfer. "
                         "There is no source plate with the barcode: [%s]",
                         g.user.first_and_last_name, source_plate_barcode)
            return {
                "success": False,
                "errorMessage": "There is no source plate with the barcode: [%s]" % (source_plate_barcode)
            }

        # storage_location = source_plate.storage_location # FIXME why copy the storage location??

        #
        # 2. Obtain (or create if we haven't yet grabbed it) the sample plate type row for the type of plate
        # specified for the destination of this line item.
        #
        # NOTE I removed the bit about reverse mapping from plate well count
        # because there's no need to do this if you pass in the plate type ID
        # directly as part of the transform spec.
        dest_plate_type = db_session.query(PlateType).\
            get(destination_plate_type)
        if not dest_plate_type:
            logging.info(" %s encountered error creating sample "
                         "transfer. There are no sample plates with "
                         "the type: [%s]",
                         g.user.first_and_last_name,
                         destination_plate_type)
            return {
                "success": False,
                "errorMessage": "There are no sample plates with the type: [%s]" % (destination_plate_type)
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
                try:
                    # Retrieve the target plate for our merge transform
                    destination_plate = db_session.query(Plate).\
                        filter(Plate.external_barcode == destination_plate_barcode).one()
                except:
                    logging.warn(" %s encountered error creating sample transfer. "
                                 "There is no destination plate with the barcode: [%s]",
                                 g.user.first_and_last_name, destination_plate_barcode)
                    return {
                        "success": False,
                        "errorMessage": "There is no destination plate with the barcode: [%s]" %
                                        (destination_plate_barcode)
                    }

            elif in_place_transform_flag:
                # BUGFIX 11/17/2015: for in-place transforms,
                # don't create a new plate!
                # TODO: clarify same-same transfer destination plate.
                destination_plate = source_plate

            else:
                # This is a transform that requires creating a new plate in DB
                try:
                    destination_plate = create_destination_plate(
                        db_session,
                        operator,
                        destination_plate_barcode,
                        dest_plate_type.type_id,
                        "Unknown location",  # FIXME find a better default for this
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

        destination_plate = destination_plates_by_barcode.\
            get(destination_plate_barcode)
        if not destination_plate:
            return {
                "success": False,
                "errorMessage": "Failed to create/find destination plate."
            }

        #
        logging.info('4. Get the "source plate well"')
        #

        source_well_sample = db_session.query(Sample).\
            join(PlateWell).\
            filter(Sample.plate_id == source_plate.id,
                   PlateWell.well_number == source_well_number).first()

        # print "SOURCE PLATE WELL: %s " % str(source_well_sample)
        logging.info("SOURCE WELL SAMPLE: %s (%s, %s) ", source_well_sample,
                     source_plate.id, source_well_number)

        if not source_well_sample and not merge_transform_flag:
            # I think this was trying to confirm that the source_well_number
            # is a legit well number on the destination plate so let's confirm
            # that in a more direct way rather than using mappings
            #
            # error_well_id = source_well_number
            # if dest_plate_size:
            #     if dest_plate_size == "48":
            #         try:
            #             error_well_id = get_col_and_row_for_well_id_48(source_well_number)
            #         except:
            #             error_well_id = source_well_number
            #     elif dest_plate_size == "96":
            #         try:
            #             error_well_id = get_col_and_row_for_well_id_96(source_well_number)
            #         except:
            #             error_well_id = source_well_number
            #     elif dest_plate_size == "384":
            #         try:
            #             error_well_id = get_col_and_row_for_well_id_384(source_well_number)
            #         except:
            #             error_well_id = source_well_number
            name_test = destination_plate.get_well_by_number(source_well_number)
            if not name_test:
                msg = "There is no well [%s] in the source plate with barcode: [%s]" % (source_well_number, source_plate_barcode)
                if IGNORE_MISSING_SOURCE_PLATE_WELLS:
                    logging.warn(msg)
                    continue
                else:
                    logging.error(msg)
                    return {
                        "success": False,
                        "errorMessage": msg
                    }

        logging.info("DESTINATION PLATE, barcode: %s  plate type: [%s]",
                     destination_plate.external_barcode, dest_plate_type.name)

        existing_plate_layout = db_session.query(Sample).join(PlateWell).\
            filter(Sample.plate_id == destination_plate.id,
                   PlateWell.well_number == destination_well_number).first()

        if in_place_transform_flag:
            if not existing_plate_layout:
                return {
                    "success": False,
                    "errorMessage": "This in-place-transform destination plate [%s] contains no sample in well [%s]" %
                                    (destination_plate.external_barcode, source_well_sample.well.well_number)
                }
        elif merge_transform_flag:
            if not existing_plate_layout:
                return {
                    "success": False,
                    "errorMessage": "This merge-transform destination plate [%s] contains no sample in well [%s]" %
                                    (destination_plate.external_barcode, source_well_sample.well.well_number)
                }
        elif existing_plate_layout:
            # still wanted in context of in-place transforms and merge transforms?
            return {
                "success": False,
                "errorMessage": "This destination plate [%s] already contains sample [%s] in well [%s]" %
                                (destination_plate.external_barcode, source_well_sample.id,
                                 source_well_sample.well.well_number)
            }

        logging.info("4. Accession the new sample record for the well")
        copy_metadata = in_place_transform_flag or merge_transform_flag
        destination_sample = sample_handler(db_session,
                                            copy_metadata,
                                            transfer_type_id,
                                            source_well_sample,
                                            destination_plates_by_barcode[destination_plate_barcode],
                                            destination_well_number)
        db_session.flush()

        #
        # 5. Create a row representing a well in the desination plate.
        #
        # if in_place_transform_flag or merge_transform_flag:
        #     destination_well_sample = existing_plate_layout
        #     if destination_well_sample.id != destination_sample_id:
        #         destination_well_sample.id = destination_sample_id  # TODO: is this even necessary orm-wise?
        #     destination_well_sample.operator_id = operator.operator_id  # unfortunately this will wipe out the old operator_id
        # else:
        #     destination_well_sample = Sample(plate_id=destination_plate.id,
        #                                      id=destination_sample_id,
        #                                      well_id=destination_well_number,
        #                                      operator_id=operator.operator_id,
        #                                      row=source_well_sample.row,
        #                                      column=source_well_sample.column)
        #     db_session.add(destination_well_sample)

        # print "DESTINATION PLATE WELL: %s " % (str(destination_well_sample))
        # logging.info("DESTINATION PLATE WELL: %s ", destination_well_sample)
        logging.info("6. Create a row representing a transfer from a well in the 'source' plate to a well")
        source_to_destination_well_transfer = TransferDetail(
            transfer_id=sample_transfer.id,
            source_plate_id=source_well_sample.plate_id,
            source_well_id=source_well_sample.well.well_number,
            source_sample_id=source_well_sample.id,
            destination_plate_id=destination_sample.plate_id,
            destination_well_id=destination_sample.well.well_number,
            destination_sample_id=destination_sample.id)
        db_session.add(source_to_destination_well_transfer)
        db_session.flush()

        # import ipdb; ipdb.set_trace()
        # aliquot = Aliquot(transfer_id=sample_transfer.id,
        #                   source_well_sample_id=source_well_sample.id,
        #                   destination_well_sample_id=destination_sample.id)
        # db_session.add(aliquot)
        db_session.flush()

        order_number += 1

    db_session.commit()

    return {
        "success": True
    }


def sample_handler(db_session, copy_metadata, transfer_type_id,
                   source_well_sample, destination_plate,
                   destination_well_id):

    new_id = create_unique_id(Sample.id_prefix)
    try:
        well = db_session.query(PlateWell).\
            filter(PlateWell.layout == destination_plate.plate_type.layout,
                   PlateWell.well_number == destination_well_id).one()
    except:
        logger.error("Found too many wells for %s?" % destination_well_id)
        return None

    if copy_metadata:
        # Copy all extant metadata
        new_s = quick_copy(db_session, source_well_sample)
        new_s.id = new_id()
        new_s.plate_id = destination_plate.id
        new_s.plate_well_pk = well.pk
    else:
        new_s = Sample(id=new_id(), plate_id=destination_plate.id,
                       plate_well_pk=well.pk,
                       operator_id=current_user.operator_id)
    if source_well_sample:
        new_s.parent_sample_id = source_well_sample.id

    if transfer_type_id in (constants.TRANS_TYPE_QPIX_PICK_COLONIES,
                            constants.TRANS_TYPE_QPIX_TO_384_WELL):
        # We just cloned this so it's clonal
        new_s.is_clonal = True
        # FIXME hardcoding this for Warp2 for now - should derive
        # this from the A/B rebatching metadata somehow (@sucheta!)
        new_s.cloning_process_id = 'CLO_564c1af300bc150fa632c63d'

    db_session.add(new_s)
    return new_s


def safe_sqlalchemy_copy(session, object_handle):
    """Implement a safe copy.copy().

    Based on http://permalink.gmane.org/gmane.comp.python.sqlalchemy.user/39675

    SQLAlchemy-mapped objects travel with an object
    called an InstanceState, which is pegged to that object
    specifically and tracks everything about that object.  It's
    critical within all attribute operations, including gets
    and deferred loading.   This object definitely cannot be
    shared among two instances, and must be handled.

    The copy routine here makes use of session.merge() which
    already essentially implements a "copy" style of operation,
    which produces a new instance with a new InstanceState and copies
    all the data along mapped attributes without using any SQL.

    The mode we are using here has the caveat that the given object
    must be "clean", e.g. that it has no database-loaded state
    that has been updated and not flushed.   This is a good thing,
    as creating a copy of an object including non-flushed, pending
    database state is probably not a good idea; neither represents
    what the actual row looks like, and only one should be flushed.

    """
    copy = session.merge(object_handle, load=False)
    session.expunge(copy)
    return copy


def quick_copy(session, orig_obj):
    """Copy a sample, quick fix"""

    copy = Sample()
    for attrname in ("order_item_id", "type_id", "operator_id",
                     "external_barcode", "name", "description", ):
        setattr(copy, attrname, getattr(orig_obj, attrname))
    return copy

