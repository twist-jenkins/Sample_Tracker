"""add 384 to 48 transfer template

Revision ID: 7b4ae4459f8
Revises: 3bee7b56c955
Create Date: 2015-09-04 16:00:31.054440

"""

# revision identifiers, used by Alembic.
revision = '7b4ae4459f8'
down_revision = '3bee7b56c955'

from alembic import op
import sqlalchemy as sa


from app.database_data.template09_04_2015_16_17_15PM import template
from app.database_data.template_importer import import_template


def upgrade():
    import_template(op,template)



def downgrade():
    pass
