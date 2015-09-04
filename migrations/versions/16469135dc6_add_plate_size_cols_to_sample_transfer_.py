"""add plate_size cols to sample_transfer_template

Revision ID: 16469135dc6
Revises: bb22974c735
Create Date: 2015-09-04 10:14:48.651343

"""

# revision identifiers, used by Alembic.
revision = '16469135dc6'
down_revision = 'bb22974c735'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('sample_transfer_template', sa.Column('from_plate_size', sa.Integer, default=1,nullable=True))
    op.add_column('sample_transfer_template', sa.Column('destination_plate_size', sa.Integer, default=1,nullable=True))


def downgrade():
    op.drop_column('sample_transfer_template', 'from_plate_size')
    op.drop_column('sample_transfer_template', 'destination_plate_size')
