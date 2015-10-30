"""Create table sample_transfer_plan

Revision ID: 1629f51b954b
Revises: da20bea3e8f
Create Date: 2015-10-15 17:25:27.408367

"""

# revision identifiers, used by Alembic.
revision = '1629f51b954b'
down_revision = 'da20bea3e8f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():

    op.create_table(
        'sample_transfer_plan',
        sa.Column('plan_id', sa.String(40), nullable=False),
        sa.Column('plan', postgresql.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('plan_id')
    )


def downgrade():
    op.drop_table('sample_transfer_plan')
