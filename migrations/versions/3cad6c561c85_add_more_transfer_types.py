"""Add more transfer types

Revision ID: 3cad6c561c85
Revises: 3638291961f0
Create Date: 2015-11-11 05:21:25.541706

"""

# revision identifiers, used by Alembic.
revision = '3cad6c561c85'
down_revision = '3638291961f0'

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
        [25, "Rebatching for Transformation", "F", None, None]
        ,[26, "Fragment Analyzer", "F", None, None]
        ,[27, "NGS QC Pass", "F", None, None]
        ,[28, "Shipping", "F", None, None]
        ,[29, "Reformatting for Purification", "F", None, None]
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
        [45, "Rebatching for Transformation", 25, 1, 1]
        ,[46, "Fragment Analyzer", 26, 1, 1]
        ,[47, "NGS QC Pass", 27, 1, 1]
        ,[48, "Shipping", 28, 1, 1]
        ,[49, "Reformatting for Purification", 29, 1, 1]
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
