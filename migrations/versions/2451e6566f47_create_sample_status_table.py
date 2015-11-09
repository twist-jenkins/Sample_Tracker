"""create sample status table

Revision ID: 2451e6566f47
Revises: 558be9081c47
Create Date: 2015-11-05 16:19:52.122421

"""

# revision identifiers, used by Alembic.
revision = '2451e6566f47'
down_revision = '558be9081c47'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():

    op.create_table(
        'sample_status_code',
        sa.Column('status_type', sa.String(40), nullable=False),
        sa.Column('description', sa.String(512), nullable=True),
        sa.Column('date_added', sa.TIMESTAMP, nullable=False),
        sa.PrimaryKeyConstraint('status_type')
    )

    op.create_table(
        'sample_status',
        sa.Column('sample_id', sa.String(40), sa.ForeignKey('sample.sample_id'), nullable=False),
        sa.Column('status_type', sa.String(40), sa.ForeignKey('sample_status_code.status_type'), nullable=False),
        sa.Column('status_date', sa.TIMESTAMP, nullable=False),
        sa.Column('operator_id', sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint('sample_id')
    )

def downgrade():
    op.drop_table('sample_status')
    op.drop_table('sample_status_code')
