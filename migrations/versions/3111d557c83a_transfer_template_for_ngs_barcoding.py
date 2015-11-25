"""Transfer template for ngs barcoding

Revision ID: 3111d557c83a
Revises: 10b001e04cb1
Create Date: 2015-11-23 21:45:57.435695

"""

# revision identifiers, used by Alembic.
revision = '3111d557c83a'
down_revision = '10b001e04cb1'

from alembic import op
import sqlalchemy as sa


update_sql_t_type = ("update sample_transfer_type "
              "set name = :name, "
              "sample_transfer_template_id = :stti, "
              "source_plate_count = :spc, "
              "destination_plate_count = :dpc "
              "where id = :id")

insert_sql_t_type = ("insert into sample_transfer_type "
              "(id, name, sample_transfer_template_id, "
              " source_plate_count, destination_plate_count) "
              "select :id, :name, :stti, :spc, :dpc "
              "where not exists "
              "(select * from sample_transfer_type where id = :id)")

sql_param_names_t_type = ("id", "name", "stti", "spc", "dpc")

desired_values_t_type = [
    [26, "NGS prep: barcode hitpicking", 30, 1, 0]
]


update_sql_t_template = ("update sample_transfer_template "
              "set name = :name, "
              "is_one_to_one_transfer = :ioto, "
              "source_plate_well_count = :spwc, "
              "destination_plate_well_count = :dpwc "
              "where id = :id")

insert_sql_t_template = ("insert into sample_transfer_template  "
              "(id, name, is_one_to_one_transfer, source_plate_well_count, "
              " destination_plate_well_count) "
              "select :id, :name, :ioto, :spwc, :dpwc "
              "where not exists "
              "(select * from sample_transfer_template where id = :id)")

sql_param_names_t_template = ("id", "name", "ioto", "spwc", "dpwc")

desired_values_t_template = [
    [30, "NGS Barcoding", "F", None, None]
]

def upgrade():

    for row_values in desired_values_t_template:
        args = dict(zip(sql_param_names_t_template, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql_t_template).bindparams(**args))
        op.execute(sa.text(insert_sql_t_template).bindparams(**args))

    for row_values in desired_values_t_type:
        args = dict(zip(sql_param_names_t_type, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql_t_type).bindparams(**args))
        op.execute(sa.text(insert_sql_t_type).bindparams(**args))



def downgrade():
    pass
