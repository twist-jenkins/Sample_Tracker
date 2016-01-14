"""modify transfer types add ordering column

Revision ID: 28c1281bad7b
Revises: 2afc419979cf
Create Date: 2016-01-12 15:20:27.863549

"""

# revision identifiers, used by Alembic.
revision = '28c1281bad7b'
down_revision = '2afc419979cf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('sample_transfer_type', sa.Column('menu_ordering', sa.INTEGER))


def downgrade():
    op.drop_column('sample_transfer_type', 'menu_ordering')
