######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: dbmodels.py
#
# The database models used by SQLAlchemy.
#
######################################################################################

import bson
import json
import datetime

from app import app
from app import db

from sqlalchemy import MetaData
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.dialects import postgresql

from twistdb.sampletrack import *
from twistdb.public import *
from twistdb.db import Base

db_metadata = Base.metadata

#db_metadata = MetaData(bind=db.engine)  # for autoload / schema reflection


def create_unique_object_id(prefix=""):
    return prefix + str(bson.ObjectId())


class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value, use_decimal=True)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return json.loads(value, use_decimal=True)





class ClonedSample(Sample):
    """Cloned sample, simplified version of twist_core db_model.ClonedSample.
    This version is also polymorphic."""
    __tablename__ = "cloned_sample"

    sample_id = db.Column(
        db.String(40), db.ForeignKey("sample.sample_id"), primary_key=True)

    __mapper_args__ = {
       "polymorphic_identity": "cloned_sample",
       'inherit_condition': (sample_id == Sample.sample_id)
    }

    # columns
    parent_sample_id = db.Column(
        db.String(40), db.ForeignKey("sample.sample_id"), nullable=False)
    source_id = db.Column(db.String(40), nullable=False)
    colony_name = db.Column(db.String(40), nullable=False)
    plate_name = db.Column(db.String(40), nullable=True)
    plate_id = db.Column(db.String(40), nullable=True)
    well_id = db.Column(db.String(40), nullable=True)

    # relationships
    parent_sample = db.relationship(
        "Sample", uselist=False, backref=db.backref("sample_clones"),
        foreign_keys=parent_sample_id)

    def __init__(self, sample_id, parent_sample_id, source_id, colony_name,
                 plate_id, well_id, description, operator_id):
        """Init"""

        if not colony_name:
            raise ValueError("Colony name required for cloned sample")
        if self.sample_id == parent_sample_id:
            raise ValueError(
                "Sample ID == Parent Sample ID: %s" % sample_id)
        # set default name
        name = self._make_name(parent_sample_id, source_id, colony_name)
        # create description if not provided
        if not description:
            description = "Cloned sample: %s, Source: %s, Colony: %s" % (
                parent_sample_id, source_id, colony_name)

        # super
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # operator_id = operator_id
        parent_process_id = None
        external_barcode = None
        reagent_type_set_lot_id = None
        status = self.STATUS_ACTIVE
        parent_transfer_process_id = None
        fwd_primer_ps_id = None
        rev_primer_ps_id = None
        Sample.__init__(
            self, sample_id, date_created, operator_id, name,
            description, fwd_primer_ps_id, rev_primer_ps_id,
            parent_process_id, external_barcode,
            reagent_type_set_lot_id, status, parent_transfer_process_id)

        if plate_id and well_id:
            self.plate_id = plate_id
            self.well_id = well_id

        # redundant but using for unique constraint within orm
        self.colony_name = colony_name
        self.parent_sample_id = parent_sample_id
        self.source_id = source_id

    def _make_name(self, parent_sample_id, source_id, colony_name):
        """Helper to make short name"""
        pid = parent_sample_id
        if len(parent_sample_id) > 10:
            pid = "%s_%s.%s" % (
                parent_sample_id.split("_")[0],
                parent_sample_id[-6:-3].upper(),
                parent_sample_id[-3:].upper())
        return "%s-%s.%s" % (pid, source_id, colony_name)

    def parent(self):
        """Return parent"""
        return self.parent_sample


class NGSPreppedSample(Sample):
    """NGS prepped sample -- Simpler version based on twist_core"""
    __tablename__ = "ngs_prepped_sample"
    # type info
    sample_id = db.Column(
        db.String(40), db.ForeignKey("sample.sample_id"),
        primary_key=True, index=True)
    __mapper_args__ = {
        "polymorphic_identity": "ngs_prepped_sample",
        "inherit_condition": (sample_id == Sample.sample_id)}
    parent_sample_id = db.Column(
        db.String(40), db.ForeignKey("sample.sample_id"),
        nullable=False)
    i5_sequence_id = db.Column(
        db.String(40),
        db.ForeignKey("barcode_sequence.sequence_id"),
        nullable=True)
    i7_sequence_id = db.Column(
        db.String(40),
        db.ForeignKey("barcode_sequence.sequence_id"),
        nullable=True)
    insert_size_expected = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(1024))
    # relations
    parent_sample = db.relationship(
        "Sample", uselist=False,
        backref=db.backref("ngs_prepped_samples"),
        foreign_keys=parent_sample_id)
    # i5_barcode = db.relationship(
    #     "BarcodeSequence", uselist=False,
    #     backref=db.backref("i5_ngs_run_sample_joins"),
    #     foreign_keys=i5_sequence_id)
    # i7_barcode = db.relationship(
    #     "BarcodeSequence", uselist=False,
    #     backref=db.backref("i7_ngs_run_sample_joins"),
    #     foreign_keys=i7_sequence_id)

    def __init__(self, sample_id, parent_sample_id, description,
                 i5_sequence_id, i7_sequence_id, notes, insert_size_expected,
                 date_created, operator_id, parent_process_id,
                 external_barcode, reagent_type_set_lot_id, status,
                 parent_transfer_process_id):
        """Init"""
        name = "%s.%s" % (sample_id, parent_sample_id)
        Sample.__init__(
            self, sample_id, date_created, operator_id, name,
            description, None, None, parent_process_id, external_barcode,
            reagent_type_set_lot_id, status, parent_transfer_process_id)
        if self.sample_id == parent_sample_id:
            raise ValueError(
                "Sample ID == Parent Sample ID: %s" % sample_id)
        self.parent_sample_id = parent_sample_id
        if i5_sequence_id:
            self.i5_sequence_id = i5_sequence_id
        if i7_sequence_id:
            self.i7_sequence_id = i7_sequence_id
        self.insert_size_expected = insert_size_expected
        if notes:
            self.notes = notes

