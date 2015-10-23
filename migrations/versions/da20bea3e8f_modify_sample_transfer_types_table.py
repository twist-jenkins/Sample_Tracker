"""modify sample_transfer_types table

Revision ID: da20bea3e8f
Revises: 38166f229d6b
Create Date: 2015-10-08 00:17:40.345523

"""

# revision identifiers, used by Alembic.
revision = 'da20bea3e8f'
down_revision = '38166f229d6b'

from alembic import op
import sqlalchemy as sa

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
    [1, "Aliquoting for Quantification (384 plate)", 1, 1, 1],
    [2, "Cloning (Insert hitpicking)", 1, 1, 1],
    [3, "Cloning (Thermocyling)", 2, 1, 0],
    [4, "Cloning (Vector hitpicking)", 2, 1, 0],
    [5, "Denaturation / Reannealing", 1, 1, 1],
    [6, "Error correction (ECR)", 1, 1, 1],
    [7, "PCA", 2, 1, 0],
    [8, "PCR", 2, 1, 0],
    [9, "Purification (384 plate)", 1, 1, 1],
    [10, "Transfer to EDC plate", 1, 1, 1],
    [11, "Aliquoting for Frag analysis", 13, 1, 4],
    [12, "Transformation", 13, 1, 4],
    [13, "Plating on Hamilton", 14, 1, 2],
    [14, "Picking: Manual to 96 plates", 16, 1, 4],
    [15, "Picking: Qpix to 96 plates", 21, 1, 4],
    [16, "Picking: Qpix to 384 plates", 22, 1, 1],
    [17, "Glycerol stock: from 96 plate", 18, 4, 1],
    [18, "Glycerol stock: from 384 plate", 1, 1, 1],
    [19, "Aliquoting for RCA: from 96 plate", 18, 4, 1],
    [20, "Aliquoting for RCA: from 384 plate", 1, 1, 1],
    [21, "RCA: Stamp for denaturation", 1, 1, 1],
    [22, "RCA: Stamp into templiphi plate", 1, 1, 1],
    [23, "RCA: dilution step 1 (1:3)", 2, 1, 0],
    [24, "RCA: dilution step 2 (1:75)", 1, 1, 1],
    [25, "NGS prep: tagmentation", 2, 1, 0],
    [26, "NGS prep: barcode hitpicking", 2, 1, 0],
    [27, "NGS prep: PCR", 2, 1, 0],
    [28, "Hitpicking for primer removal: from RCA", 19, 0, 0],
    [29, "Hitpicking for primer removal: from Glycerol stock", 19, 0, 0],
    [30, "PR: Phusion U MM addition", 2, 1, 0],
    [31, "PR: PCR", 2, 1, 0],
    [32, "PR: Pre-USER purification", 1, 1, 1],
    [33, "PR: USER addition", 2, 1, 0],
    [34, "PR: USER incubation", 2, 1, 0],
    [35, "PR: Kappa polishing", 2, 1, 0],
    [36, "Purification: 96 plate", 1, 1, 1],
    [37, "Aliquoting for Frag analysis", 1, 1, 1],
    [38, "Aliquoting for Quantification: 96 plate", 1, 1, 1],
    [39, "Hitpicking for miniprep: from glycerol stock", 19, 0, 0],
    [40, "Miniprep", 1, 1, 1],
    [41, "Miniprep transfer to 96-PCR plate", 1, 1, 1],
    [42, "Hitpick for shipping", 20, 1, 0]
    [43, "Plate Merge", 23, 1, 1]
]


def upgrade():

    op.add_column('sample_transfer_type',
                  sa.Column('source_plate_count',
                            sa.Integer, default=1))
    op.add_column('sample_transfer_type',
                  sa.Column('destination_plate_count',
                            sa.Integer, default=1))

    for row_values in desired_values:
        args = dict(zip(sql_param_names, row_values))

        # try update first, then insert.  The WHERE clauses in the SQL
        # for insert and update should allow this without causing failures.
        op.execute(sa.text(update_sql).bindparams(**args))
        op.execute(sa.text(insert_sql).bindparams(**args))


def downgrade():

    op.drop_column('sample_transfer_type', 'source_plate_count')
    op.drop_column('sample_transfer_type', 'destination_plate_count')

