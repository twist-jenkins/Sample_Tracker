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

    # Cache all requested plates, raising an error if any are not found
    plate_cache = {}
    srcs = set([d['source_plate_barcode'] for d in transform_map])
    logging.info("Caching source plates: %s" % list(srcs))
    for src_barcode in srcs:
        try:
            source_plate = db_session.query(Plate).\
                filter(Plate.external_barcode == src_barcode).one()
            plate_cache[src_barcode] = source_plate
        except:
            logging.warn(" %s encountered error creating sample transform. "
                         "There is no source plate with the barcode: [%s]",
                         g.user.first_and_last_name, src_barcode)
            return {
                "success": False,
                "errorMessage": "There is no source plate with the barcode: [%s]" % (src_barcode)
            }

    # Cache all destination plates, creating any that are not found

    dests = set([(d['destination_plate_barcode'],
                  d['destination_plate_type']) for d in transform_map])
    logging.info("Caching dest plates: %s" % list(dests))
    for dest_barcode, dtype in dests:
        try:
            dest_plate = db_session.query(Plate).\
                filter(Plate.external_barcode == dest_barcode).one()
            plate_cache[dest_barcode] = dest_plate
        except:
            logging.info("There is no dest plate [%s], creating it",
                         dest_barcode)
            # This is a transform that requires creating a new plate in DB
            try:
                destination_plate = create_destination_plate(
                    db_session,
                    operator,
                    dest_barcode,
                    dtype,
                    "Unknown location",  # FIXME find a better default for this
                    transform_template_id)
                plate_cache[dest_barcode] = destination_plate
                db_session.flush()
            except IndexError:
                err_msg = ("Encountered error creating sample "
                           "transform. Could not create destination plate: [%s]"
                           )
                logging.error(err_msg)
                return {
                    "success": False,
                    "errorMessage": err_msg
                }

    # We always operate on a plate's current contents so we pull that
    # in a single query so that we have it on-hand and can then single out
    # samples for transfer.
    sample_cache = {}
    logging.info("Caching plate samples.")
    for barcode, plate in plate_cache.iteritems():
        s = plate.current_well_contents(db_session)
        for sample in s:
            sample_cache[(barcode, sample.well.well_number)] = sample

    # Lookup well_number by well_name, if necessary
    for oper in transform_map:
        if "source_well_number" not in oper:
            s_bc = oper["source_plate_barcode"]
            s_label = str(oper["source_well_name"])
            s_type = plate_cache[s_bc].plate_type
            s_number = s_type.layout.get_well_by_label(s_label).well_number
            oper["source_well_number"] = s_number
            # TODO: oper["source_well_sample"]

    # Also cache a map of well number to well instance for all destination wells
    well_cache = {}
    for dest_barcode in [d[0] for d in dests]:
        plate = plate_cache[dest_barcode]
        # if plate.type_id not in well_cache.keys():
        #    well_cache[plate.type_id] = {}
        well_ids = [d['destination_well_number']
                    if d['destination_plate_barcode'] == dest_barcode
                    else None for d in transform_map]
        well_ids = [x for x in well_ids if x is not None]  # There must be a better way!
        for id in well_ids:
            well_cache[(dest_barcode, id)] = plate.get_well_by_number(id)

    dest_grouping_func = lambda oper: (oper['destination_plate_barcode'],
                                       oper['destination_well_number'])
    transforms_by_dest = sorted(transform_map, key=dest_grouping_func)

    new_rows = []
    logging.info("Iterating over operations...")
    for dest_key, operation_group in itertools.groupby(transforms_by_dest,
                                                       dest_grouping_func):

        # This loop is now oriented towards many-samples-to-one-sample
        # merge transforms.  len(source_samples) shows the type of transform:
        #
        #     len(source_samples) == 0: create fresh sample, no parents
        #     len(source_samples) == 1: copy sample, one parent
        #     len(source_samples) > 1: merge sample, multiple parents
        #
        # Handles mixing operations (pooling, NGS barcoding,
        # primer addition, etc) as well as non-mixing steps

        # check destination

        destination_plate_barcode, destination_well_number = dest_key
        logging.warn("**************** %s", dest_key)

        try:
            dplate = plate_cache[destination_plate_barcode]
        except KeyError:
            msg = "Failed to lookup destination plate from cache [%s]."
            msg %= destination_plate_barcode
            logging.error("Invalid xfer: %s", msg)
            return {"success": False, "errorMessage": msg}

        try:
            dest_s = sample_cache[(destination_plate_barcode,
                                   destination_well_number)]
        except KeyError:
            # raise KeyError(destination_plate_barcode, destination_well_number)
            dest_s = None

        # check source(s)

        source_samples = [sample_cache[(oper["source_plate_barcode"],
                                        oper["source_well_number"])]
                          for oper in operation_group]

        s = sample_handler(db_session, sample_transform,
                           well_cache, source_samples, dplate,
                           destination_well_number, dest_s)
        new_rows.append(s)

    logging.info("Bulk inserting samples and relationships.")

    db_session.bulk_save_objects(new_rows)
    db_session.commit()

    logger.info("Adhoc movement took: " + str(time.time() - start))

    return {
        "success": True
    }


def sample_handler(db_session, transform, well_cache,
                   source_well_samples, destination_plate,
                   destination_well_id, destination_sample=None):
    """Accessions a new sample into the designated well,
    using the source sample(s) as parents and/or reagents.
    Note: destination_sample, if present, will become a parent
    of the new sample that this routine will accession."""

    logging.debug("sample_handler: src=[%s] dest=[%s]",
                  source_well_samples, destination_sample)

    new_id = create_unique_id(Sample.id_prefix)

    # Copy all extant metadata except transform, parents, children, is_clonal
    if len(source_well_samples) == 0:
        raise ValueError("source sample is required")
    elif len(source_well_samples) > 1:
        logging.debug("Merging %d samples into %s",
                      len(source_well_samples), destination_sample)
        new_s = merged_sample(db_session, source_well_samples)
    else:
        assert len(source_well_samples) == 1
        new_s = copied_sample(db_session, source_well_samples[0])

    # Set attributes unique to this sample
    new_s.id = new_id()
    new_s.plate_id = destination_plate.id
    new_s.transform_id = transform.id
    well = well_cache[(destination_plate.external_barcode,
                       destination_well_id)]
    new_s.plate_well_code = well.well_code

    # Handle transform-specific sample logic
    if transform.transform_type_id in (constants.TRANS_TYPE_QPIX_PICK_COLONIES,
                                       constants.TRANS_TYPE_QPIX_TO_384_WELL):
        # We just cloned this so it's clonal
        new_s.is_clonal = True
        # FIXME hardcoding this for Warp2 for now - should derive
        # this from the A/B rebatching metadata somehow (@sucheta!)
        new_s.cloning_process_id = 'CLO_564c1af300bc150fa632c63d'

    # Link up the source sample(s) and any "destination" sample as parent(s)
    for source_well_sample in source_well_samples:
        source_to_dest_well_transform = TransformDetail(
            transform=transform,
            parent_sample_id=source_well_sample.id,
            child_sample_id=new_s.id
        )

    if destination_sample:
        dest_well_parent_transform = TransformDetail(
            transform=transform,
            parent_sample_id=destination_sample.id,
            child_sample_id=new_s.id
        )

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


def copied_sample(session, orig_obj):
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


def merged_sample(session, parent_samples):
    """Merge a set of samples."""

    copy = Sample()
    attrs_to_ignore = ("is_clonal", )
    for attrname in ("order_item_id", "type_id", "operator_id",
                     "external_barcode", "name", "description",
                     "work_order_id", "synthesis_run_pk", "cluster_num",
                     "primer_pk", "cloning_process_id",
                     "mol_type", "is_circular",
                     "is_assembly", "is_external", "external_id",
                     "host_cell_pk", "growth_medium", "i5_sequence_id",
                     "i7_sequence_id"):
        source_vals = set([getattr(par, attrname) for par in parent_samples])
        if len(source_vals) == 1:
            setattr(copy, attrname, source_vals[0])
    return copy
