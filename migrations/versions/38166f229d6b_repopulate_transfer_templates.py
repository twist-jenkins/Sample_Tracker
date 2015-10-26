"""Repopulate transfer templates

Revision ID: 38166f229d6b
Revises: 16ac291fa1b9
Create Date: 2015-10-12 21:02:01.150025

"""

# revision identifiers, used by Alembic.
revision = '38166f229d6b'
down_revision = '16ac291fa1b9'

from alembic import op
import sqlalchemy as sa

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
    [1, "Same to same transfer", "T", None, None],
    [2, "Same plate", "T", None, None],
    [12, "384 to 48", "F", 384, 48],
    [13, "384 to 96 ", "F", 384, 96],
    [14, "96 to 48", "F", 96, 48],
    [16, "48 to 96 VARIABLE", "F", 48, 96],
    [17, "48 to 384 VARIABLE", "F", 48, 384],
    [18, "96 to 384", "F", 96, 384],
    [19, "384 to 96 VARIABLE", "F", 384, 96],
    [20, "96 to VARIABLE", "F", 96, None],
    [21, "Qpix to 96 well plates", "F", None, None],
    [22, "Qpix to 384 well plates", "F", None, None],
    [23, "Plate Merge", "F", None, None],
    [24, "Generic Transfer", "F", None, None]
]


def upgrade():
    op.add_column('sample_transfer_template',
                  sa.Column('source_plate_well_count',
                            sa.Integer))
    op.add_column('sample_transfer_template',
                  sa.Column('destination_plate_well_count',
                            sa.Integer))

    for row_values in desired_values:
        args = dict(zip(sql_param_names, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql).bindparams(**args))
        op.execute(sa.text(insert_sql).bindparams(**args))


def downgrade():
    op.drop_column('sample_transfer_template', 'source_plate_well_count')
    op.drop_column('sample_transfer_template', 'destination_plate_well_count')
