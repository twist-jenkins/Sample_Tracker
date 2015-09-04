"""add template

Revision ID: 1c726e0ec497
Revises: 16469135dc6
Create Date: 2015-09-04 10:18:34.106157

"""

# revision identifiers, used by Alembic.
revision = '1c726e0ec497'
down_revision = '16469135dc6'

from alembic import op
import sqlalchemy as sa


from app.database_data.template09_04_2015_10_03_36AM import template
from app.database_data.template_importer import import_template


def upgrade():
    import_template(op,template)



def downgrade():
    pass
