"""modify some columns in template tables

Revision ID: a000f9786c3
Revises: 271e00baa3
Create Date: 2015-09-04 10:44:15.930359

"""

# revision identifiers, used by Alembic.
revision = 'a000f9786c3'
down_revision = '271e00baa3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('sample_transfer_template_details', 'source_plate_well_count')
    op.drop_column('sample_transfer_template_details', 'destination_plate_well_count')
    op.alter_column('sample_transfer_template', 'from_plate_size', new_column_name='source_plate_well_count')
    op.alter_column('sample_transfer_template', 'destination_plate_size', new_column_name='destination_plate_well_count')

def downgrade():
    pass
