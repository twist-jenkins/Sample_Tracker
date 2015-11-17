"""Add NGSBarcodePair table and seq.

Revision ID: 5a4d81becc55
Revises: 2508b1c64724
Create Date: 2015-11-16 16:45:50.744702

"""

# revision identifiers, used by Alembic.
revision = '5a4d81becc55'
down_revision = '2508b1c64724'

import csv
import json

from alembic import op
import sqlalchemy as db


def upgrade():
    ngs_barcode_pair_table = op.create_table(
        'ngs_barcode_pair',
        db.Column('id',
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

    csvfilename = 'database/ngs_barcode_database.csv'
    csvfile = open(csvfilename, 'rU')
    if not csvfile:
        raise "Cannot open %s" % csvfilename
    fieldnames = ("modulo_index",  # id
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
        assert int(pair["modulo_index"]) == ix
    max_value = ix
    op.bulk_insert(ngs_barcode_pair_table, ngs_barcode_pairs)
    print ("Created table 'ngs_barcode_pair': "
           "%d ngs_barcode_pairs added to DB" % len(ngs_barcode_pairs))

    sql = '''
        CREATE SEQUENCE "ngs_barcode_pair_index_seq"
        MINVALUE 0
        INCREMENT BY 1
        MAXVALUE %d
        START WITH 2618
        CYCLE''' % max_value
    print "Created sequence 'ngs_barcode_pair_index_seq': %s" % sql
    op.execute(sql)

def downgrade():
    op.execute('drop table if exists ngs_barcode_pair')
    op.execute('drop sequence if exists ngs_barcode_pair_index_seq')
