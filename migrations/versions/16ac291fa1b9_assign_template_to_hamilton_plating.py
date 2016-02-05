"""assign template to hamilton plating

Revision ID: 16ac291fa1b9
Revises: 23f42852f68d
Create Date: 2015-09-04 16:26:53.949976

"""

# revision identifiers, used by Alembic.
revision = '16ac291fa1b9'
down_revision = '23f42852f68d'

from alembic import op
import sqlalchemy as sa


def upgrade():

    connection = op.get_bind()

    transfer_template_id = None 

    select = "select id from sample_transfer_template where name = '384 to 48'"
    results = connection.execute(select)
    for result in results:
        transfer_template_id = int(result[0])

    sql = " UPDATE sample_transfer_type set transfer_template_id = %d "
    sql += " WHERE name='Plating on Hamilton' "
    op.execute(sql % (transfer_template_id))

def downgrade():
    pass
