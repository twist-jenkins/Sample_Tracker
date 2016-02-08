"""create well status table

Revision ID: 3638291961f0
Revises: 2451e6566f47
Create Date: 2015-11-05 16:20:04.726506

"""

# revision identifiers, used by Alembic.
revision = '3638291961f0'
down_revision = '2451e6566f47'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():

    op.create_table(
        'well_status_code',
        sa.Column('status_type', sa.String(40), nullable=False),
        sa.Column('description', sa.String(512), nullable=True),
        sa.Column('date_created', sa.TIMESTAMP, nullable=False),
        sa.PrimaryKeyConstraint('status_type')
    )

    op.create_table(
        'well_status',
        sa.Column('plate_id', sa.String(40), sa.ForeignKey('sample_plate.id'), nullable=False),
        sa.Column('well_id', sa.INTEGER, nullable=False),
        sa.Column('status_type', sa.String(40), sa.ForeignKey('well_status_code.status_type'), nullable=False),
        sa.Column('status_date', sa.TIMESTAMP, nullable=False),
        sa.Column('operator_id', sa.String(100), nullable=False)
    )

def downgrade():
    op.drop_table('well_status')
    op.drop_table('well_status_code')
