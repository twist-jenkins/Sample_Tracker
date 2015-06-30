"""add sample ids to sample_transfer_detail

Revision ID: 284f24a958d6
Revises: 2f432d03e68d
Create Date: 2015-06-29 15:09:51.641913

"""

# revision identifiers, used by Alembic.
revision = '284f24a958d6'
down_revision = '2f432d03e68d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('sample_transfer_detail', sa.Column('source_sample_id', sa.String(40)))
    op.add_column('sample_transfer_detail', sa.Column('destination_sample_id', sa.String(40)))


def downgrade():
    pass
