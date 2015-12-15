"""add_hamilton_transform_steps

Revision ID: 29c899083825
Revises: 3111d557c83a
Create Date: 2015-12-15 14:55:15.359919

"""

# revision identifiers, used by Alembic.
revision = '29c899083825'
down_revision = '3111d557c83a'

from alembic import op
import sqlalchemy as sa


def upgradeTransferTemplates():
    update_sql = ("update sample_transfer_template "
                  "set name = :name, "
                  "is_one_to_one_transfer = :ioto, "
                  "source_plate_well_count = :spwc, "
                  "destination_plate_well_count = :dpwc "
                  "where id = :id")

    insert_sql = ("insert into sample_transfer_template  "
                  "(id, name, is_one_to_one_transfer, source_plate_well_count, "
                  " destination_plate_well_count) "
                  "select :id, :name, :ioto, :spwc, :dpwc "
                  "where not exists "
                  "(select * from sample_transfer_template where id = :id)")

    sql_param_names = ("id", "name", "ioto", "spwc", "dpwc")

    desired_values = [
        [32, "Hitpicking for Miniprep", "F", None, None]
    ]

    for row_values in desired_values:
        args = dict(zip(sql_param_names, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql).bindparams(**args))
        op.execute(sa.text(insert_sql).bindparams(**args))

def upgradeTransferTypes():
    update_sql = ("update sample_transfer_type "
              "set name = :name, "
              "sample_transfer_template_id = :stti, "
              "source_plate_count = :spc, "
              "destination_plate_count = :dpc "
              "where id = :id")

    insert_sql = ("insert into sample_transfer_type "
                  "(id, name, sample_transfer_template_id, "
                  " source_plate_count, destination_plate_count) "
                  "select :id, :name, :stti, :spc, :dpc "
                  "where not exists "
                  "(select * from sample_transfer_type where id = :id)")

    sql_param_names = ("id", "name", "stti", "spc", "dpc")

    desired_values = [
        [39, "Hitpicking for Miniprep", 32, 0, 0, 38]
        [48, "Hitpicking for Shipping", 28, 0, 0, 47]
    ]

    for row_values in desired_values:
        args = dict(zip(sql_param_names, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql).bindparams(**args))
        op.execute(sa.text(insert_sql).bindparams(**args))
        
def upgrade():

    upgradeTransferTemplates();
    upgradeTransferTypes();

def downgrade():
    pass