"""add is_one_to_one_transfer column to sample_transfer_template table

Revision ID: 2a4607332a84
Revises: 490846e6ac8d
Create Date: 2015-09-03 17:23:56.431972

"""

# revision identifiers, used by Alembic.
revision = '2a4607332a84'
down_revision = '490846e6ac8d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('sample_transfer_template', sa.Column('is_one_to_one_transfer', sa.String(1), default="N"))


def downgrade():
    op.drop_column('sample_transfer_template', 'is_one_to_one_transfer')
