"""add template

Revision ID: bb22974c735
Revises: 53225805e104
Create Date: 2015-09-04 10:04:14.124413

"""

# revision identifiers, used by Alembic.
revision = 'bb22974c735'
down_revision = '53225805e104'

from alembic import op
import sqlalchemy as sa

from app.database_data.template09_04_2015_10_03_36AM import template
from app.database_data.template_importer import import_template


def upgrade():
    import_template(op,template)



def downgrade():
    pass
