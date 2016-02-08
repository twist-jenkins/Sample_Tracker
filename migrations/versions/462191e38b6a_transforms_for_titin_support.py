"""Transforms for Titin support.

Revision ID: 462191e38b6a
Revises: 430e2caa4545
Create Date: 2016-01-11 14:28:38.583640

"""

# revision identifiers, used by Alembic.
revision = '462191e38b6a'
down_revision = '430e2caa4545'

from alembic import op
import sqlalchemy as sa


def upgradeTransferTemplates():
    update_sql = ("update sample_transfer_template"
                  " set name = :name,"
                  " is_one_to_one_transfer = :ioto,"
                  " source_plate_well_count = :spwc,"
                  " destination_plate_well_count = :dpwc"
                  " where id = :id")

    insert_sql = ("insert into sample_transfer_template"
                  " (id, name, is_one_to_one_transfer, source_plate_well_count,"
                  " destination_plate_well_count)"
                  " select :id, :name, :ioto, :spwc, :dpwc"
                  " where not exists"
                  " (select * from sample_transfer_template where id = :id)")

    sql_param_names = ("id", "name", "ioto", "spwc", "dpwc")

    desired_values = [
        [34, "Extraction - Titin", "F", None, None]
    ]

    for row_values in desired_values:
        args = dict(zip(sql_param_names, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql).bindparams(**args))
        op.execute(sa.text(insert_sql).bindparams(**args))


def upgradeTransferTypes():
    update_sql = ("update sample_transfer_type"
                  " set name = :name,"
                  " transfer_template_id = :stti,"
                  " source_plate_count = :spc,"
                  " destination_plate_count = :dpc"
                  " where id = :id")

    insert_sql = ("insert into sample_transfer_type"
                  " (id, name, transfer_template_id,"
                  " source_plate_count, destination_plate_count)"
                  " select :id, :name, :stti, :spc, :dpc"
                  " where not exists"
                  " (select * from sample_transfer_type where id = :id)")

    sql_param_names = ("id", "name", "stti", "spc", "dpc")

    desired_values = [
        [52, "Extraction - Titin", 34, 1, 16, None]
    ]

    for row_values in desired_values:
        args = dict(zip(sql_param_names, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql).bindparams(**args))
        op.execute(sa.text(insert_sql).bindparams(**args))


def upgrade():

    upgradeTransferTemplates()
    upgradeTransferTypes()


def downgrade():
    pass