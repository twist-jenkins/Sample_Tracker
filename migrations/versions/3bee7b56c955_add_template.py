"""add template

Revision ID: 3bee7b56c955
Revises: a000f9786c3
Create Date: 2015-09-04 11:03:04.238707

"""

# revision identifiers, used by Alembic.
revision = '3bee7b56c955'
down_revision = 'a000f9786c3'

from alembic import op
import sqlalchemy as sa


from app.database_data.template09_04_2015_10_03_36AM import template
from app.database_data.template_importer import import_template


def upgrade():
    import_template(op,template)



def downgrade():
    pass
