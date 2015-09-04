"""init one to one sample transfer template

Revision ID: 53225805e104
Revises: 2a4607332a84
Create Date: 2015-09-04 08:33:11.990882

"""

# revision identifiers, used by Alembic.
revision = '53225805e104'
down_revision = '2a4607332a84'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("UPDATE sample_transfer_template SET is_one_to_one_transfer='Y' WHERE name='One to One Transfer' ")


def downgrade():
    pass
