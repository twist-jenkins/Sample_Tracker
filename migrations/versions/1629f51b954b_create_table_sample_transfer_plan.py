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


def upgrade():

    op.create_table(
        'sample_transfer_plan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transfer_plan', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('sample_transfer_plan')
