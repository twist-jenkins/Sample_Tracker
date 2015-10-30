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

db_metadata = MetaData(bind=db.engine)  # for autoload / schema reflection

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


class Operator(db.Model):

    operator_id = db.Column(db.String(10), primary_key=True)
    jira_username = db.Column(db.String(100))
    email = db.Column(db.String(120))
    user_id = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(80))

    def __repr__(self):
        return '<Operator id: [%s] name: [%s] >' % (self.operator_id,self.email)

    def __init__(self, operator_id, email, first_name, last_name ):
        self.operator_id = operator_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_and_last_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + " " + self.last_name
        return "Unknown"

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True #self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Sample(db.Model):

    sample_id = db.Column(db.String(40), primary_key=True)
    type_id = db.Column(db.String(40), db.ForeignKey('sample_type.type_id'))
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.operator_id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(2048))
    date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)

    #
    # Relationships. ORM magicalness.
    #

    operator = db.relationship("Operator")

    def __init__(self, sample_id, type_id, operator_id, name):
        self.sample_id = create_unique_object_id("SMPL_")
        self.type_id = type_id
        self.operator_id = operator_id
        self.name = name

    def __repr__(self):
        return '<Sample sample_id: [%s] type_id: [%s] operator_id: [%s] name: [%s] >' % (self.sample_id,
            self.type_id,self.operator_id, self.name)


class GeneAssemblySampleView(db.Model):
    try:
        __table__ = db.Table("gene_assembly_sample_view", db_metadata,
                             db.Column("sample_id", db.String(40),
                                       primary_key=True), autoload=True)
    except:
        __table__ = db.Table("gene_assembly_sample", db_metadata,
                             db.Column("sample_id", db.String(40),
                                       primary_key=True), autoload=False)


class SamplePlate(db.Model):

    sample_plate_id = db.Column(db.String(40), primary_key=True)
    type_id = db.Column(db.String(40), db.ForeignKey('sample_plate_type.type_id'))
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.operator_id'))
    storage_location_id = db.Column(db.String(40), db.ForeignKey('storage_location.storage_location_id'))
    date_created = db.Column(db.DateTime) #,default=datetime.datetime.utcnow)
    name = db.Column(db.String(100))
    description = db.Column(db.String(2048))
    external_barcode = db.Column(db.String(100))
    status = db.Column(db.Enum('disposed', 'in_use', 'new',
                               name="enum_sample_plate_status"
                               ), default="new")

    #
    # Relationships. ORM magicalness.
    #

    operator = db.relationship("Operator")
    sample_plate_type = db.relationship("SamplePlateType")
    storage_location = db.relationship("StorageLocation")
    wells = db.relationship("SamplePlateLayout")


    def __init__(self, type_id, operator_id, storage_location_id, name, description, external_barcode):
        self.sample_plate_id = create_unique_object_id("SPLT_")
        self.type_id = type_id
        self.operator_id = operator_id
        self.storage_location_id = storage_location_id
        self.name = name
        self.description = description
        self.status = "new"
        self.external_barcode = external_barcode
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return '<SamplePlate sample_plate_id: [%s] name: [%s] >' % (self.sample_plate_id,self.name)




class SamplePlateLayout(db.Model):

    sample_plate_id = db.Column(db.String(40), db.ForeignKey('sample_plate.sample_plate_id'), primary_key=True)
    well_id = db.Column(db.Integer, primary_key=True)

    #
    # removed the primary key constraint on 7/15/15
    #
    sample_id = db.Column(db.String(40), db.ForeignKey('sample.sample_id')) #, primary_key=True)

    operator_id = db.Column(db.String(10), db.ForeignKey('operator.operator_id'))
    row = db.Column(db.String(10))
    column = db.Column(db.Integer)
    date_created = db.Column(db.DateTime) #,default=datetime.datetime.utcnow)
    notes = db.Column(db.String(512))
    status = db.Column(db.Enum('active', 'deleted', 'failure', 'inactive',
                               name='enum_sample_status'
                               ), default="active")

    #
    # Relationships. ORM magicalness.
    #

    sample = db.relationship("Sample")

    def __init__(self, sample_plate_id, sample_id, well_id, operator_id, row, column, status="active"):
        self.sample_plate_id = sample_plate_id
        self.sample_id = sample_id
        self.well_id = well_id
        self.operator_id = operator_id
        self.row = row
        self.column = column
        self.status = status
        self.date_created = datetime.datetime.now()


        #self.name = name

    def __repr__(self):
        return '<SamplePlateLayout sample_plate_id: [%s]  sample_id: [%s]  well_id: [%s] >' % (self.sample_plate_id,
            self.sample_id, self.well_id )



"""
rows_alpha character varying(100),
    cols_num integer
"""

class SamplePlateType(db.Model):

    type_id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(2048))
    number_clusters = db.Column(db.Integer)
    sample_plate_type = db.Column(
        db.Enum('custom_plastic_16', 'custom_plastic_30', 'nw_ct_0004_96',
                'nw_ct_0006_108', 'nw_ct_0008_96', 'nw_ct_0012_108',
                'plastic_1', 'plastic_12', 'plastic_1536', 'plastic_24',
                'plastic_3456', 'plastic_384', 'plastic_48',
                'plastic_6', 'plastic_96', 'plastic_9600',
                name="enum_sample_plate_type"))
    status = db.Column(db.Enum('active','retired',
                               name="enum_sample_plate_type_status"),
                       default="active")
    rows_alpha = db.Column(db.String(100))
    cols_num = db.Column(db.Integer)

    def __init__(self, name, sample_plate_type,rows_alpha,cols_num):
        self.type_id = create_unique_object_id("SPT_")
        self.name = name
        self.sample_plate_type = sample_plate_type
        self.rows_alpha = rows_alpha
        self.cols_num = cols_num


    def __repr__(self):
        return '<SamplePlateType id: [%s] name: [%s] >' % (self.type_id,self.name)



class SampleTransfer(db.Model):

    #
    # Table columns.
    #

    id = db.Column(db.Integer, primary_key=True)
    sample_transfer_type_id = db.Column(db.Integer, db.ForeignKey('sample_transfer_type.id'))
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.operator_id'))
    date_transfer = db.Column(db.DateTime) #,default=datetime.datetime.utcnow)

    #
    # Relationships. ORM magicalness.
    #

    sample_transfer_type = db.relationship("SampleTransferType")
    operator = db.relationship("Operator")


    def __init__(self, sample_transfer_type_id, operator_id):
        self.sample_transfer_type_id = sample_transfer_type_id
        self.operator_id = operator_id
        self.date_transfer = datetime.datetime.now()

    def __repr__(self):
        return '<SampleTransfer operator: [%s] transfer type: [%s] datetime: [%s] >' % (self.operator.first_and_last_name,
            self.sample_transfer_type.name,self.date_transfer)


class SampleTransferDetail(db.Model):

    #
    # Table columns.
    #

    sample_transfer_id = db.Column(db.Integer, db.ForeignKey('sample_transfer.id'), primary_key=True)
    item_order_number = db.Column(db.Integer, primary_key=True)
    source_sample_plate_id = db.Column(db.String(40), db.ForeignKey('sample_plate.sample_plate_id'))
    source_well_id = db.Column(db.Integer)#, db.ForeignKey('sample_plate_layout.well_id'))
    source_sample_id = db.Column(db.String(40))#, db.ForeignKey('sample_plate_layout.sample_id'))

    destination_sample_plate_id = db.Column(db.String(40), db.ForeignKey('sample_plate.sample_plate_id'))
    destination_well_id = db.Column(db.Integer)#, db.ForeignKey('sample_plate_layout.well_id'))
    destination_sample_id = db.Column(db.String(40))#, db.ForeignKey('sample_plate_layout.sample_id'))

    #
    # Relationships. ORM magicalness.
    #

    sample_transfer = db.relationship("SampleTransfer")
    source_plate = db.relationship("SamplePlate",foreign_keys='SampleTransferDetail.source_sample_plate_id')
    destination_plate = db.relationship("SamplePlate",foreign_keys='SampleTransferDetail.destination_sample_plate_id')


    def __init__(self, sample_transfer_id, item_order_number, source_sample_plate_id, source_well_id,
        source_sample_id, destination_sample_plate_id, destination_well_id, destination_sample_id ):
        self.sample_transfer_id = sample_transfer_id
        self.item_order_number = item_order_number
        self.source_sample_plate_id = source_sample_plate_id
        self.source_well_id = source_well_id
        self.source_sample_id = source_sample_id
        self.destination_sample_plate_id = destination_sample_plate_id
        self.destination_well_id = destination_well_id
        self.destination_sample_id = destination_sample_id


class SampleTransferTemplate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_one_to_one_transfer = db.Column(db.String(1),default="N", nullable=True)
    from_plate_size = db.Column(db.Integer,default=1,nullable=False)
    destination_plate_size = db.Column(db.Integer,default=1,nullable=False)

    __table_args__ = (db.CheckConstraint(is_one_to_one_transfer.in_(['Y','N'])), )

    sample_transfer_types = db.relationship('SampleTransferType')

    sample_transfer_template_details = db.relationship('SampleTransferTemplateDetails')

    def __init__(self, name ):
        self.name = name

    def __repr__(self):
        return '<SampleTransferTemplate id: [%d] name: [%s] >' % (self.id,self.name)


class SampleTransferTemplateDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sample_transfer_template_id = db.Column(db.Integer, db.ForeignKey('sample_transfer_template.id'))
    source_plate_number = db.Column(db.Integer, default=1, nullable=False)
    #source_plate_well_count = db.Column(db.Integer, nullable=False)
    source_plate_well_id = db.Column(db.Integer, nullable=False)
    source_plate_well_id_string = db.Column(db.String(10),default="",nullable=True)

    destination_plate_number = db.Column(db.Integer, default=1, nullable=False)
    #destination_plate_well_count = db.Column(db.Integer, nullable=False)
    destination_plate_well_id = db.Column(db.Integer, nullable=False)
    destination_plate_well_id_string = db.Column(db.String(10),default="",nullable=True)

    sample_transfer_template = db.relationship('SampleTransferTemplate')


class SampleTransferType(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    source_plate_count = db.Column(db.Integer)
    destination_plate_count = db.Column(db.Integer)
    sample_transfer_template_id = db.Column(db.Integer, db.ForeignKey('sample_transfer_template.id'))

    sample_transfers = db.relationship('SampleTransfer')
    sample_transfer_template = db.relationship('SampleTransferTemplate')

    #def __init__(self, name ):
    #    self.name = name

    #def __repr__(self):
    #    return '<SampleTransferType id: [%d] name: [%s] template: [%s] source_plate_count: [%s] destination_plate_count: [%s]>' % (self.id,self.name,self.sample_transfer_template.name, self.source_plate_count, self.destination_plate_count)



class SampleType(db.Model):

    type_id = db.Column(db.String(40), primary_key=True)
    id_prefix = db.Column(db.String(40))
    name = db.Column(db.String(100))
    description = db.Column(db.Text())

    def __init__(self, type_id, id_prefix, name ):
        self.type_id = type_id
        self.id_prefix = id_prefix
        self.name = name

    def __repr__(self):
        return '<SampleType id: [%d] name: [%s] >' % (self.id,self.name)



class StorageLocation(db.Model):

    storage_location_id = db.Column(db.String(40), primary_key=True)
    parent_storage_location_id = db.Column(db.String(40), db.ForeignKey('storage_location.storage_location_id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(2048))
    location_type = db.Column(
        db.Enum('disposal', 'plate_storage', 'storage', 'work_station',
                name="enum_storage_location_type"),
        default="plate_storage")
    status = db.Column(
        db.Enum('active', 'inactive', name="enum_storage_status"),
        default="active")

    def __init__(self, name ):
        self.storage_location_id = create_unique_object_id("LOC_")
        self.name = name



class SampleTransferPlan(db.Model):

    plan_id = db.Column(db.String(40), primary_key=True)
    plan = db.Column(postgresql.JSON(), nullable=False)

    def __init__(self, plan_id, plan):
        self.plan_id = plan_id
        self.plan = plan

    def __repr__(self):
        return '<SampleTransfer Plan id: [%s]>' % (self.plan_id, )


