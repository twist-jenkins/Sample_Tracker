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
from twistdb.db import Base

from sqlalchemy import MetaData
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.dialects import postgresql

db_metadata = Base.metadata

NGS_BARCODE_PLATE = "NGS_BARCODE_PLATE_TEST1"
NGS_BARCODE_PLATE_TYPE = 'SPTT_0006'
NGS_BARCODE_SAMPLE_PREFIX = 'BCS_'


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


class SampleView(db.Model):
    try:
        __table__ = db.Table("sample_view", db_metadata,
                             db.Column("sample_id", db.String(40),
                                       primary_key=True), autoload=True)
    except:
        from twistdb.sampletrack import Sample
        __table__ = Sample.__table__


class MiSeqSampleView(db.Model):
    try:
        __table__ = db.Table("miseq_sample_view", db_metadata,
                             db.Column("sample_id", db.String(40),
                                       primary_key=True), autoload=True)
    except:
        from twistdb.sampletrack import Sample
        __table__ = Sample.__table__



def barcode_sequence_to_barcode_sample(barcode_sequence_name):
    return NGS_BARCODE_SAMPLE_PREFIX + barcode_sequence_name.split("_")[1]


