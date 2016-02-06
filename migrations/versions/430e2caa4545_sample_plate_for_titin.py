"""Sample plate for Titin.

Revision ID: 430e2caa4545
Revises: 41fd137c0b35
Create Date: 2016-01-11 14:27:33.314103

"""

# revision identifiers, used by Alembic.
revision = '430e2caa4545'
down_revision = '41fd137c0b35'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Enum

TITIN_TYPE_ID = 'SPTT_1009'

def insert_plate_type_record():
    #
    # older code to insert a new SAMPLE_PLATE_TYPE row.
    # doesn't work... "AttributeError: Neither 'Column' object nor 'Comparator' object has an attribute '_has_bind_expression' "...
    # using raw sql instead, below.
    #
    sp_migration_table = table(
        'plate_type',
        column('type_id', String),
        column('name', Integer),
        column('description', String),
        column('number_clusters', Integer),
        column('plate_type', String),
        column('status', Enum)
    )
    titin_plate = {
        'type_id': TITIN_TYPE_ID,
        'name': '6144 well, silicon, Titin X.X',
        'description': 'Silicon - Titin 6144 silicon Chip',
        'number_clusters': 6144,
        'plate_type': 'silicon_6144',
        'status': 'active'
    }
    op.bulk_insert(sp_migration_table, [titin_plate])


def upgrade_plate_type():
    # update_sql = ("update sample_transfer_type"
    #               " set name = :name,"
    #               " transfer_template_id = :stti,"
    #               " source_plate_count = :spc,"
    #               " destination_plate_count = :dpc"
    #               " where id = :id")

    insert_sql = ("insert into plate_type"
                  " (type_id, name, description,"
                  " number_clusters, plate_type, status)"
                  " select :type_id, :name, :description,"
                  " :number_clusters, :plate_type, :status"
                  " where not exists"
                  " (select * from plate_type "
                  "  where type_id = :type_id)")

    sql_params = {"type_id": TITIN_TYPE_ID,
                  "name": '6144 well, silicon, Titin X.X',
                  "description": 'Silicon - Titin 6144 silicon Chip',
                  "number_clusters": 6144,
                  "plate_type": 'silicon_6144',
                  "status": 'active'
                  }

    # try update first, then insert.  The WHERE clauses in the SQL
    # for insert and update should allow this without causing failures.
    # op.execute(sa.text(update_sql).bindparams(**args))
    op.execute(sa.text(insert_sql).bindparams(**sql_params))


def upgrade():

    upgrade_plate_type()


def downgrade():
    delete_sql = 'delete from plate_type where plate_type = :pt'
    args = {"pt": TITIN_TYPE_ID}
    op.execute(sa.text(delete_sql).bindparams(**args))
