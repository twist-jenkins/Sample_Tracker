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
import itertools

from flask import g, jsonify
from flask_login import current_user

from app import db, constants
from app.utils import scoped_session
from app.models import create_destination_plate
from app.dbmodels import NGS_BARCODE_PLATE  # , NGS_BARCODE_PLATE_TYPE

from twistdb import create_unique_id
from twistdb.sampletrack import (Sample, Plate, Transform, TransformDetail)

IGNORE_MISSING_SOURCE_PLATE_WELLS = True  # FIXME: this allows silent failures

logger = logging.getLogger(name="Spreadsheet")


def error_response(status_code, message):
    # TODO: remove duplicate code -- use JSON-API?
    response = jsonify({'success': False, 'message': message})
    response.status_code = status_code
    return response

#
# If the user uploaded a spreadsheet with each row representing a well-to-well transform, this is where we
# process that spreadsheet data.
#


def create_step_record_adhoc(transform_type_id,
                             transform_template_id,
                             transform_map):

    with scoped_session(db.engine) as db_session:
        result = create_adhoc_sample_movement(db_session,
                                              transform_type_id,
                                              transform_template_id,
                                              transform_map)
        if result["success"]:
            return jsonify({
                "success": True
            })
        else:
            return error_response(400, result["errorMessage"])


def create_adhoc_sample_movement(db_session,
                                 transform_type_id,
                                 transform_template_id, transform_map,
                                 transform_spec_id=None):
    #
    # FIRST. Create a "sample_transform" row representing this row's transform.
    #
    operator = g.user
    sample_transform = Transform(transform_type_id=transform_type_id,
                                 transform_spec_id=transform_spec_id,
                                 operator_id=operator.operator_id)
    db_session.add(sample_transform)
    db_session.flush()

    import time
    start = time.time()

    #import pdb
    #pdb.set_trace()
    # Cache all requested source plates
    source_plates = {}
    logging.info("Caching source plates.")
    srcs = set([d['source_plate_barcode'] for d in transform_map])
    for src in srcs:
        try:
            source_plate = db_session.query(Plate).\
                filter(Plate.external_barcode == src).one()
            source_plates[src] = source_plate
        except:
            logging.warn(" %s encountered error creating sample transform. "
                         "There is no source plate with the barcode: [%s]",
                         g.user.first_and_last_name, src)
            return {
                "success": False,
                "errorMessage": "There is no source plate with the barcode: [%s]" % (src)
            }

    # We always operate on a plate's current contents so we pull that
    # in a single query so that we have it on-hand and can then single out
    # samples for transfer.
    src_samples = {}
    logging.info("Caching source samples.")
    for barcode, plate in source_plates.iteritems():
        s = plate.current_well_contents(db_session)
        src_samples[barcode] = {}
        for sample in s:
            src_samples[barcode][sample.well.well_number] = sample

    # Create and cache all destination plates as needed
    dest_plates = {}
    logging.info("Caching dest plates.")
    dests = set([(d['destination_plate_barcode'],
                  d['destination_plate_type']) for d in transform_map])

    # TODO: remove merge_transform_flag
    # merge_transform_flag = (NGS_BARCODE_PLATE in srcs)
    in_place_transform_flag = (srcs == set([d[0] for d in dests]))

    # if merge_transform_flag:
    #     # TODO: add lots more kinds of merge transforms.
    #     try:
    #         # Retrieve the target plate for our merge transform
    #         dbarcodes = [d[0] for d in dests]
    #         dplates = db_session.query(Plate).\
    #             filter(Plate.external_barcode.in_(dbarcodes)).all()
    #         for plate in dplates:
    #             dest_plates[plate.external_barcode] = plate
    #     except:
    #         logging.warn("%s encountered error creating sample transform. "
    #                      "One or more destination plate with barcodes do not # exist (in merge transform): %s",
    #                      g.user.first_and_last_name, dests)
    #         return {
    #             "success": False,
    #             "errorMessage": "Missing at least one destination plate with # the barcode: %s" %
    #                             (dests)
    #         }
    # el
    if in_place_transform_flag:
        # BUGFIX 11/17/2015: for in-place transforms,
        # don't create a new plate!
        # TODO: clarify same-same transform destination plate.
        dest_plates = source_plates
    else:
        # This is a transform that requires creating a new plate in DB
        try:
            for barcode, dtype in dests:
                destination_plate = create_destination_plate(
                    db_session,
                    operator,
                    barcode,
                    dtype,
                    "Unknown location",  # FIXME find a better default for this
                    transform_template_id)
                dest_plates[barcode] = destination_plate
            db_session.flush()
        except IndexError:
            err_msg = ("Encountered error creating sample "
                       "transform. Could not create destination plate: [%s]"
                       )
            logging.info(err_msg, ",".join([d[0] for d in dests]))
            return {
                "success": False,
                "errorMessage": err_msg % ",".join([d[0] for d in dests])
            }

    # Create a map of samples already on the destination plates, if any
    dest_samples = {}
    logging.info("Caching dest samples (if any).")
    for barcode, plate in dest_plates.iteritems():
        s = plate.current_well_contents(db_session)
        dest_samples[barcode] = {}
        for sample in s:
            dest_samples[barcode][sample.well.well_number] = sample

    # Also cache a map of well number to well instance for all destination wells
    well_cache = {}
    for barcode, plate in dest_plates.iteritems():
        if plate.type_id not in well_cache.keys():
            well_cache[plate.type_id] = {}
        well_ids = [d['destination_well_number']
                    if d['destination_plate_barcode'] == barcode
                    else None for d in transform_map]
        well_ids = [x for x in well_ids if x is not None]  # There must be a better way!
        for id in well_ids:
            well_cache[plate.type_id][id] = plate.get_well_by_number(id)

    # Split mixing operations (pooling, NGS barcoding, primer addition, etc)
    # out from non-mixing steps
    #mixing_factor = defaultdict(int)
    #for oper in transform_map:
    #    mixing_factor[(oper["source_plate_barcode"],
    #                   oper['source_well_number'])] += 1
    #mixing_operations = [oper for oper in transform_map
    #                     if mixing_factor[(oper["source_plate_barcode"],
    #                                       oper['source_well_number'])] > 1

    keyfunc = lambda oper: (oper['destination_plate_barcode'],
                            oper['destination_well_number'])
    transforms_by_dest = sorted(transform_map, key=keyfunc)

    new_rows = []
    logging.info("Creating new samples.")
    for dest_key, operation_group in itertools.groupby(transforms_by_dest,
                                                       keyfunc):

        # This loop is now oriented towards many-samples-to-one-sample
        # merge transforms.  len(source_samples) shows the type of transform:
        #
        #     len(source_samples) == 0: create fresh sample, no parents
        #     len(source_samples) == 1: copy sample, one parent
        #     len(source_samples) > 1: merge sample, multiple parents

        # check destination

        destination_plate_barcode, destination_well_number = dest_key

        try:
            dplate = dest_plates[destination_plate_barcode]
        except KeyError:
            msg = "Failed to create/find destination plate [%s]."
            msg %= destination_plate_barcode
            logging.error("Invalid xfer: %s", msg)
            return {"success": False,
                    "errorMessage": msg}

        try:
            dest_s = dest_samples[destination_plate_barcode][destination_well_number]
        except KeyError:
            dest_s = None

        # check source(s)

        source_samples = []
        for oper in operation_group:
            try:
                source_plate_barcode = oper["source_plate_barcode"]
                source_well_number = oper['source_well_number']
            except KeyError:
                msg = "Failed to create/find source plate/well [%s/%s]."
                msg %= (source_plate_barcode, source_well_number)
                logging.error("Invalid xfer: %s", msg)
                return {"success": False,
                        "errorMessage": msg}

            try:
                src_s = src_samples[source_plate_barcode][source_well_number]
            except KeyError:
                msg = "Failed to create sample for plate/well [%s/%s]."
                msg %= (source_plate_barcode, source_well_number)
                logging.error("Invalid xfer: %s", msg)
                return {"success": False,
                        "errorMessage": msg}

            source_samples.append(src_s)

        copy_metadata = in_place_transform_flag  # or merge_transform_flag
        s = sample_handler(db_session, copy_metadata, sample_transform,
                           well_cache, [src_s], dplate,
                           destination_well_number, dest_s)
        new_rows.append(s)


    if False: # for oper in transform_map:
        try:
            source_plate_barcode = oper["source_plate_barcode"]
            source_well_number = oper['source_well_number']
            destination_plate_barcode = oper["destination_plate_barcode"]
            destination_well_number = oper['destination_well_number']
        except KeyError:
            logging.error("Malformed operation [%s]:", oper)
            raise

        # try:
        #     splate = source_plates[source_plate_barcode]
        # except:
        #     logging.warn(" %s encountered error creating sample transform. "
        #                  "There is no source plate with the barcode: [%s]",
        #                  g.user.first_and_last_name, source_plate_barcode)
        #     return {
        #         "success": False,
        #         "errorMessage": "There is no source plate with the barcode: [%s]" % (source_plate_barcode)
        #     }

        try:
            dplate = dest_plates[destination_plate_barcode]
        except:
            return {
                "success": False,
                "errorMessage": "Failed to create/find destination plate [%s]." %
                                destination_plate_barcode
            }

        try:
            src_s = src_samples[source_plate_barcode][source_well_number]
        except:
            return {
                "success": False,
                "errorMessage": "Failed to create sample for plate/well [%s/%s]." %
                                (source_plate_barcode, source_well_number)
            }

        try:
            dest_s = dest_samples[destination_plate_barcode][destination_well_number]
        except:
            dest_s = None

        # NOTE I'm not sure when we would need this or even in what code path
        # it would execute given the try block above?
        #
        # if not src_s and not merge_transform_flag:
        #
        #     name_test = dplate.get_well_by_number(source_well_number)
        #     if not name_test:
        #         msg = "There is no well [%s] in the source plate with barcode: [%s]" % (source_well_number, source_plate_barcode)
        #         if IGNORE_MISSING_SOURCE_PLATE_WELLS:
        #             logging.warn(msg)
        #             continue
        #         else:
        #             logging.error(msg)
        #             return {
        #                 "success": False,
        #                 "errorMessage": msg
        #             }

        # existing_plate_layout = db_session.query(Sample).\
        #     join(PlateWell, Sample.well).\
        #     filter(Sample.plate_id == destination_plate.id,
        #            PlateWell.well_number == destination_well_number).first()

        # NOTE I don't think we need to carefully check these; if the destination
        # well has a sample in it, then this is by definition a merge transform
        # and we should note the source and current destination sample as parents
        # of the new destination sample.
        #
        # if in_place_transform_flag:
        #     if not existing_plate_layout:
        #         return {
        #             "success": False,
        #             "errorMessage": "This in-place-transform destination plate [%s] contains no sample in well [%s]" %
        #                             (destination_plate.external_barcode, source_well_sample.well.well_number)
        #         }
        # elif merge_transform_flag:
        #     if not existing_plate_layout:
        #         return {
        #             "success": False,
        #             "errorMessage": "This merge-transform destination plate [%s] contains no sample in well [%s]" %
        #                             (destination_plate.external_barcode, source_well_sample.well.well_number)
        #         }
        # elif existing_plate_layout:
        #     # still wanted in context of in-place transforms and merge transforms?
        #     return {
        #         "success": False,
        #         "errorMessage": "This destination plate [%s] already contains sample [%s] in well [%s]" %
        #                         (destination_plate.external_barcode, source_well_sample.id,
        #                          source_well_sample.well.well_number)
        #     }

        assert src_s is not None

        copy_metadata = in_place_transform_flag or merge_transform_flag
        s = sample_handler(db_session, copy_metadata, sample_transform,
                           well_cache, [src_s], dplate,
                           destination_well_number, dest_s)
        new_rows.append(s)

    logging.info("Bulk inserting samples and relationships.")

    db_session.bulk_save_objects(new_rows)
    db_session.commit()

    logger.info("Adhoc movement took: " + str(time.time() - start))

    return {
        "success": True
    }


def sample_handler(db_session, copy_metadata, transform, well_cache,
                   source_well_samples, destination_plate,
                   destination_well_id, destination_sample=None):

    logging.warn("sample_handler: src=[%s] dest=[%s]",
                 source_well_samples, destination_sample)

    new_id = create_unique_id(Sample.id_prefix)
    try:
        well = well_cache[destination_plate.type_id][destination_well_id]
    except:
        err = "Found too many wells for dest well_id [%s] type [%s]" \
            % (destination_well_id, destination_plate.plate_type)
        logger.error(err)
        raise KeyError(err)

    if copy_metadata:
        assert len(source_well_samples) == 1
        # Copy all extant metadata
        new_s = quick_copy(db_session, source_well_samples[0])
        new_s.id = new_id()
        new_s.plate_id = destination_plate.id
        new_s.plate_well_code = well.well_code
    else:
        new_s = Sample(id=new_id(), plate_id=destination_plate.id,
                       plate_well_code=well.well_code,
                       operator_id=current_user.operator_id)
    new_s.transform_id = transform.id

    if transform.transform_type_id in (constants.TRANS_TYPE_QPIX_PICK_COLONIES,
                                       constants.TRANS_TYPE_QPIX_TO_384_WELL):
        # We just cloned this so it's clonal
        new_s.is_clonal = True
        # FIXME hardcoding this for Warp2 for now - should derive
        # this from the A/B rebatching metadata somehow (@sucheta!)
        new_s.cloning_process_id = 'CLO_564c1af300bc150fa632c63d'

    # new_objs = [new_s]

    # Link up the source samples as parent
    for source_well_sample in source_well_samples:
        source_to_dest_well_transform = TransformDetail(
            transform=transform,
            parent_sample_id=source_well_sample.id,
            child_sample_id=new_s.id
        )
    # new_objs.append(source_to_dest_well_transform)
    # NOTE that we don't have to explicitly return the TransformDetail instances
    # created because they are linked to the new_s Sample instance by virtue
    # of setting new_s.id as the child ID. I tried to actually return these
    # instances directly and commit them in the bulk commit and that ended up
    # double-adding rows for each TransformDetail, one with the transform ID
    # properly populated and one without. Strange!
    #
    # I also verified that even though nothing is technically *done* with the
    # instance variables source_to_dest_well_transform and
    # dest_well_parent_transform that it *is* necessary to create them like
    # this to properly populated the TransformDetail table. SQLAlchemy magic.

    if destination_sample:
        # This is also a parent since we are merging samples
        dest_well_parent_transform = TransformDetail(
            transform=transform,
            parent_sample_id=destination_sample.id,
            child_sample_id=new_s.id
        )
        # new_objs.append(dest_well_parent_transform)

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


from sqlalchemy.orm import make_transient


def transient_copy(session, inst):
    session.expunge(inst)
    make_transient(inst)
    inst.id = None
    session.add(inst)
    session.flush()
    return inst


def quick_copy(session, orig_obj):
    """Copy a sample, quick fix"""

    copy = Sample()
    for attrname in ("order_item_id", "type_id", "operator_id",
                     "external_barcode", "name", "description",
                     "work_order_id", "synthesis_run_pk", "cluster_num",
                     "primer_pk", "cloning_process_id",
                     "mol_type", "is_circular", "is_clonal",
                     "is_assembly", "is_external", "external_id",
                     "host_cell_pk", "growth_medium", "i5_sequence_id",
                     "i7_sequence_id"):
        setattr(copy, attrname, getattr(orig_obj, attrname))
    return copy
