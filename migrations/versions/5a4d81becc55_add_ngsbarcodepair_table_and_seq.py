"""Add NGSBarcodePair table and seq.

Revision ID: 5a4d81becc55
Revises: 2508b1c64724
Create Date: 2015-11-16 16:45:50.744702

"""

# revision identifiers, used by Alembic.
revision = '5a4d81becc55'
down_revision = '2508b1c64724'

import csv
from datetime import datetime

from alembic import op
import sqlalchemy as db
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, DateTime, Enum

from app.dbmodels import create_unique_object_id
from app.dbmodels import NGS_BARCODE_PLATE, NGS_BARCODE_PLATE_TYPE
from app.plate_to_plate_maps import maps_json


def create_barcode_table():
    #
    # First the barcode database, which becomes a regular table.
    #
    ngs_barcode_pair_table = op.create_table(
        'ngs_barcode_pair',
        db.Column('pk',
                  db.Integer,
                  primary_key=True),
        db.Column('i7_sequence_id',
                  db.String(40),
                  db.ForeignKey('barcode_sequence.sequence_id'),
                  nullable=False),
        db.Column('i5_sequence_id',
                  db.String(40),
                  db.ForeignKey('barcode_sequence.sequence_id'),
                  nullable=False),
        db.Column('reverse_primer_i7_well_row',
                  db.String(10),
                  nullable=False),
        db.Column('reverse_primer_i7_well_column',
                  db.Integer,
                  nullable=False),
        db.Column('forward_primer_i5_well_row',
                  db.String(10),
                  nullable=False),
        db.Column('forward_primer_i5_well_column',
                  db.Integer,
                  nullable=False)
    )
    return ngs_barcode_pair_table


def populate_values(ngs_barcode_pair_table):
    #
    # Populate its values from the file Austin provided.
    #
    csvfilename = 'database/ngs_barcode_database.csv'
    csvfile = open(csvfilename, 'rU')
    if not csvfile:
        raise "Cannot open %s" % csvfilename
    fieldnames = ("pk",
                  "i7_sequence_id",
                  "i5_sequence_id",
                  "reverse_primer_i7_well_row",
                  "reverse_primer_i7_well_column",
                  "forward_primer_i5_well_row",
                  "forward_primer_i5_well_column")
    csvreader = csv.DictReader(csvfile, fieldnames)
    ignore_header = next(csvreader)
    ngs_barcode_pairs = [row for row in csvreader]
    csvfile.close()
    for ix, pair in enumerate(ngs_barcode_pairs):
        assert int(pair["pk"]) == ix
    max_value = ix
    op.bulk_insert(ngs_barcode_pair_table, ngs_barcode_pairs)
    print ("Created table 'ngs_barcode_pair': "
           "%d ngs_barcode_pairs added to DB" % len(ngs_barcode_pairs))
    return ngs_barcode_pairs, max_value


def create_cycle_sequence(max_value):
    #
    # Now create a (postgres-specific) sequence which cycles
    # through the barcodes.  For non-postgres, a modulo operation
    # could be used instead.
    #
    sql = '''
        CREATE SEQUENCE "ngs_barcode_pair_index_seq"
        MINVALUE 0
        INCREMENT BY 1
        MAXVALUE %d
        START WITH 2618
        CYCLE''' % max_value
    print "Created sequence 'ngs_barcode_pair_index_seq': %s" % sql
    op.execute(sql)


def build_plate_wells(ngs_barcode_pairs):
    # Build the barcode plate wells, making sure there is
    # no inconsistent data.
    # Return barcode sequences too.

    json_maps = maps_json()
    plate_map = json_maps["row_column_maps"][NGS_BARCODE_PLATE_TYPE]
    """
                "SPTT_0006": {
                # 384 well plate
                 1: {"row":"A", "column": 1}
                ,2: {"row":"A", "column": 2}
    """
    reverse_map = {(dct["row"], int(dct["column"])): well_id
                   for well_id, dct in plate_map.items()}
    """
                 ("A", 1): 1,
                 ("A", 2): 2
    """
    """
    modulo_index
    i7_sequence_id,  i5_sequence_id
    reverse_primer_i7_well_row, reverse_primer_i7_well_column
    forward_primer_i5_well_row,  forward_primer_i5_well_column
      0 BC_00029  BC_00125  A 1 A 2
      1 BC_00030  BC_00126  C 1 C 2
      2 BC_00031  BC_00127  E 1 E 2
    """
    wells = {}
    barcode_sequences = set()
    for pair in ngs_barcode_pairs:
        for (row_key, col_key, seq_key) in (
            ("reverse_primer_i7_well_row",
             "reverse_primer_i7_well_column",
             "i7_sequence_id"),
            ("forward_primer_i5_well_row",
             "forward_primer_i5_well_column",
             "i5_sequence_id"),
        ):
            rowcol = (pair[row_key], int(pair[col_key]))
            well_id = reverse_map[rowcol]
            barcode_seq = pair[seq_key]
            barcode_sequences.add(barcode_seq)
            if well_id in wells:
                assert wells[well_id] == barcode_seq
            else:
                wells[well_id] = barcode_seq
    return wells, barcode_sequences


def insert_barcode_sample_records(barcode_sequences):
    #
    # Now populate samples (of some type TBD) for the barcode sequences
    # so we can put them into a plate layout.
    #

    unq_srtd_barcode_seqs = sorted(list(set(barcode_sequences)))
    sample_migration_table = table(
        'sample',
        column('sample_id', String),
        column('date_created', DateTime),
        column('operator_id', String),
        column('type_id', Integer),
        column('name', String),
        column('description', String),
        column('status', String)
    )
    rows = [{'sample_id': barcode_sequence_to_barcode_sample(seq_name),
             'date_created': datetime.now(),
             'operator_id': 'AH',
             'type_id': 'blended_sample',
             'name': seq_name,
             'description': 'Barcode sample for %s' % seq_name,
             'status': 'active'
             }
            for seq_name in unq_srtd_barcode_seqs
            ]
    op.bulk_insert(sample_migration_table, rows)


def insert_barcode_plate_record():
    #
    # Now insert a parentless NGS_BARCODE_PLATE_TEST1.
    #
    bc_plate_id = create_unique_object_id('SPLT_')
    sp_migration_table = table(
        'sample_plate',
        column('sample_plate_id', String),
        column('type_id', Integer),
        column('operator_id', String),
        column('storage_location_id', String),
        column('date_created', DateTime),
        column('description', String),
        column('external_barcode', String),
        column('name', String),
        column('status', Enum('disposed', 'in_use', 'new'))
    )
    barcode_plate = {
        'sample_plate_id': bc_plate_id,
        'type_id': NGS_BARCODE_PLATE_TYPE,
        'operator_id': 'AH',
        'storage_location_id': 'LOC_0064',  # FAKE STORAGE LOCATION
        'date_created': datetime.now(),
        'description': 'Barcoding Plate Test 1',
        'external_barcode': NGS_BARCODE_PLATE,
        'name': 'NGS Barcode Plate Test 1',
        'status': 'in_use'
    }
    op.bulk_insert(sp_migration_table, [barcode_plate])
    return bc_plate_id


def insert_barcode_well_records(bc_plate_id, wells):
    #
    # Now populate that plate NGS_BARCODE_PLATE_TEST1 with samples.
    #

    json_maps = maps_json()
    plate_map = json_maps["row_column_maps"][NGS_BARCODE_PLATE_TYPE]

    splt_migration_table = table(
        'sample_plate_layout',
        column('sample_plate_id', String),
        column('sample_id', String),
        column('well_id', Integer),
        column('row', Integer),
        column('column', Integer),
        column('date_created', DateTime),
        column('operator_id', String),
        column('status', Enum('active',))
    )
    rows = [{'sample_plate_id': bc_plate_id,
             'sample_id': barcode_sequence_to_barcode_sample(wells[well_id]),
             'well_id': well_id,
             'row': row_col_dict["row"],
             'column': row_col_dict["column"],
             'date_created': datetime.now(),
             'operator_id': 'AH',
             'status': 'active'
             }
            for (well_id, row_col_dict) in plate_map.items()
            if well_id in wells]
    op.bulk_insert(splt_migration_table, rows)

    '''
    for well_id, row_col_dict in plate_map:
        if well_id in wells:
            # i7_wells[i7_seq_id] = reverse_map[i7_rowcol]
            barcode_id = 'BC_233'
            barcode_well = {
                'sample_plate_id': bc_plate_id,
                'sample_id': barcode_id,
                'well_id': well_id,
                'row': row_col_dict["row"],
                'column': row_col_dict["column"],
                'date_created': datetime.now(),
                'operator_id': 'AH',
                'status': 'active'
            }
    '''


def upgrade():
    ngs_barcode_pair_table = create_barcode_table()
    ngs_barcode_pairs, max_value = populate_values(ngs_barcode_pair_table)
    create_cycle_sequence(max_value)
    wells, barcode_sequences = build_plate_wells(ngs_barcode_pairs)
    insert_barcode_sample_records(barcode_sequences)
    bc_plate_id = insert_barcode_plate_record()
    insert_barcode_well_records(bc_plate_id, wells)


def downgrade():
    delete_sql = 'delete from sample_plate where external_barcode = :bc'
    args = {"bc": NGS_BARCODE_PLATE}
    op.execute(db.text(delete_sql).bindparams(**args))
    op.execute('drop table if exists ngs_barcode_pair')
    op.execute('drop sequence if exists ngs_barcode_pair_index_seq')
