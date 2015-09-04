"""add template

Revision ID: 47dcc92e8108
Revises: 1c726e0ec497
Create Date: 2015-09-04 10:30:40.645125

"""

# revision identifiers, used by Alembic.
revision = '47dcc92e8108'
down_revision = '1c726e0ec497'

from alembic import op
import sqlalchemy as sa


from app.database_data.template09_04_2015_10_03_36AM import template
from app.database_data.template_importer import import_template


def upgrade():
    import_template(op,template)



def downgrade():
    pass
