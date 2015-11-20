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
    __tablename__ = "sample"

    # class
    STATUS_ACTIVE = "active"
    STATUS_CONSUMED = "consumed"
    STATUS_READY_TO_SHIP = "ready_to_ship"
    STATUS_SHIPPED = "shipped"
    STATUS_DISPOSED = "disposed"

    sample_id = db.Column(db.String(40), primary_key=True)

    type_id = db.Column(
        db.String(40), db.ForeignKey("sample_type.type_id"),
        index=True, nullable=False)

    # mapper
    __mapper_args__ = {
        "polymorphic_on": type_id,
        "polymorphic_identity": "sample",
        "with_polymorphic": "*"
    }

    # attr
    #operator_id = db.Column(db.String(10), db.ForeignKey('operator.operator_id'))
    #name = db.Column(db.String(100))
    #description = db.Column(db.String(2048))
    #date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)


    # attr
    date_created = db.Column(db.DateTime)
    operator_id = db.Column(
        db.String(10), db.ForeignKey("operator.operator_id"))
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1024))
    # external_barcode = db.Column(db.String(100), nullable=True)
    parent_process_id = db.Column(
        db.String(40), #db.ForeignKey("process.process_id"),
        nullable=True)
    # parent_transfer_process_id = db.Column(
    #     db.String(40), db.ForeignKey("transfer_process.process_id"),
    #     nullable=True)
    status = db.Column(
        db.Enum(
            STATUS_ACTIVE, STATUS_CONSUMED, STATUS_DISPOSED,
            STATUS_READY_TO_SHIP, STATUS_SHIPPED,
            name="enum_sample_status"),
        nullable=False)
    # optional
    # fwd_primer_ps_id = db.Column(
    #     db.String(40),
    #     db.ForeignKey("primer_sequence.sequence_id"), nullable=True)
    # rev_primer_ps_id = db.Column(
    #     db.String(40),
    #     db.ForeignKey("primer_sequence.sequence_id"), nullable=True)
    # reagent_type_set_lot_id = db.Column(
    #     db.String(40),
    #     db.ForeignKey("reagent_type_set_lot.reagent_type_set_lot_id"),
    #     nullable=True)
    # relations
    # fwd_primer = db.relationship(
    #     "PrimerSequence", uselist=False,
    #     backref=db.backref("sample_fwd_primers"),
    #     foreign_keys=fwd_primer_ps_id)
    # rev_primer = db.relationship(
    #     "PrimerSequence", uselist=False,
    #     backref=db.backref("sample_rev_primers"),
    #     foreign_keys=rev_primer_ps_id)
    operator = db.relationship(
        "Operator", uselist=False, backref=db.backref("samples"),
        foreign_keys=operator_id)
    #sample_type = db.relationship(
    #    "SampleType", uselist=False,
    #    backref=db.backref("samples"),
    #    foreign_keys=type_id)
    #parent_process = db.relationship(
    #    "Process", uselist=False,
    #    backref=db.backref("child_samples"),
    #    foreign_keys=parent_process_id)
    # reagent_type_set_lot = db.relationship(
    #     "ReagentTypeSetLot", uselist=False,
    #     backref=db.backref("samples"),
    #     foreign_keys=reagent_type_set_lot_id)

    #
    # Relationships. ORM magicalness.
    #

    operator = db.relationship("Operator")

    def __init__(self, sample_id, date_created, operator_id,
                 name, description, fwd_primer_ps_id, rev_primer_ps_id,
                 parent_process_id, external_barcode, reagent_type_set_lot_id,
                 status, parent_transfer_process_id):
        """Init"""
        self.sample_id = sample_id
        self.date_created = datetime.datetime.strptime(
            date_created, '%Y-%m-%d %H:%M:%S')
        self.operator_id = operator_id
        if reagent_type_set_lot_id:
            self.reagent_type_set_lot_id = reagent_type_set_lot_id
        if status:
            self.status = status
        else:
            self.status = self.STATUS_ACTIVE
        if external_barcode:
            self.external_barcode = external_barcode
        if parent_process_id:
            self.parent_process_id = parent_process_id
        if name:
            self.name = name
        if description:
            self.description = description
        if fwd_primer_ps_id:
            self.fwd_primer_ps_id = fwd_primer_ps_id
        if rev_primer_ps_id:
            self.rev_primer_ps_id = rev_primer_ps_id
        if parent_transfer_process_id:
            self.parent_transfer_process_id = parent_transfer_process_id

    def __repr__(self):
        return '<Sample sample_id: [%s] type_id: [%s] operator_id: [%s] name: [%s] >' % (self.sample_id,
            self.type_id, self.operator_id, self.name)


class GeneAssemblySampleView(db.Model):
    try:
        __table__ = db.Table("sample_view", db_metadata,
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
    sample_transfer_type_id = db.Column(
        db.Integer, db.ForeignKey('sample_transfer_type.id'))
    sample_transform_spec_id = db.Column(
        db.Integer, db.ForeignKey('sample_transform_spec.spec_id'))
    operator_id = db.Column(
        db.String(10), db.ForeignKey('operator.operator_id'))
    date_transfer = db.Column(db.DateTime) #,default=datetime.datetime.utcnow)

    #
    # Relationships. ORM magicalness.
    #

    sample_transfer_type = db.relationship("SampleTransferType")
    sample_transform_spec = db.relationship("SampleTransformSpec")
    operator = db.relationship("Operator")


    def __init__(self, sample_transfer_type_id,
                 sample_transform_spec_id, operator_id):
        self.sample_transfer_type_id = sample_transfer_type_id
        self.sample_transform_spec_id = sample_transform_spec_id
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


class SampleTransformSpec(db.Model):

    #SPEC_ID_SEQ = db.Sequence('sample_transform_spec_seq',
    #                          start=100001)

    spec_id = db.Column(db.Integer(),
                        primary_key=True)
    type_id = db.Column(db.Integer(),
                        db.ForeignKey('sample_transfer_type.id'),
                        nullable=True)
    status = db.Column(db.String(40),
                       nullable=True)
    date_created = db.Column(db.DateTime,
                             default=datetime.datetime.utcnow,
                             nullable=False)
    operator_id = db.Column(db.String(10),
                            db.ForeignKey('operator.operator_id'),
                            nullable=False)
    date_executed = db.Column(db.DateTime,
                              nullable=True)
    data_json = db.Column(postgresql.JSON(),
                          nullable=False)

    def __repr__(self):
        return '<SampleTransfer Spec id: [%s]>' % (self.spec_id, )


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
        # db.ForeignKey("barcode_sequence.sequence_id"),
        nullable=True)
    i7_sequence_id = db.Column(
        db.String(40),
        # db.ForeignKey("barcode_sequence.sequence_id"),
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

