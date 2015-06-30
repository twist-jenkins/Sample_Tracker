"""load seed values

Revision ID: 2f432d03e68d
Revises: 210ee71b3d94
Create Date: 2015-06-26 16:16:43.574327

"""

# revision identifiers, used by Alembic.
revision = '2f432d03e68d'
down_revision = '210ee71b3d94'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, Text


def insert_rows_simple_table(lookup_table,values_list):
    ins = lookup_table.insert()
    for value in values_list:
        new_row = ins.values(name=value)
        op.execute(new_row)


def load_sample_transfer_type():
    lookup_table = table('sample_transfer_type',
        column('id', Integer),
        column('name', String)
    )
    insert_rows_simple_table(lookup_table,["Add PCR Master Mix", "Transfer Aliquot", "Move Specimen"])

def delete_all_from_sample_transfer_type():
    lookup_table = table('sample_transfer_type',
        column('id', Integer),
        column('name', String)
    )
    op.execute(lookup_table.delete())


def upgrade():
    load_sample_transfer_type()


def downgrade():
    delete_all_from_sample_transfer_type()
