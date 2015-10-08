"""modify sample_transfer_types table

Revision ID: da20bea3e8f
Revises: 20f6697c416
Create Date: 2015-10-08 00:17:40.345523

"""

# revision identifiers, used by Alembic.
revision = 'da20bea3e8f'
down_revision = '16ac291fa1b9'

from alembic import op
import sqlalchemy as sa

update_template = ("update sample_transfer_type "
                   "set name = :name, "
                   "sample_transfer_template_id = :stti, "
                   "source_plate_count = :spc, "
                   "destination_plate_count = :dpc, "
                   "inverted = :inv "
                   "where id = :id")

update_template_arg_names = ("id", "name", "stti", "spc", "dpc", "inv")

desired_values = [
    [1, "Aliquoting for Quantification (384 plate)", 1, 1, 1, False],
    [2, "Cloning (Insert hitpicking)", 1, 1, 1, False],
    [3, "Cloning (Thermocyling)", 1, 1, 0, False],
    [4, "Cloning (Vector hitpicking)", 1, 1, 0, False],
    [5, "Denaturation / Reannealing", 1, 1, 1, False],
    [6, "Error correction (ECR)", 1, 1, 1, False],
    [7, "PCA", 1, 1, 0, False],
    [8, "PCR", 1, 1, 0, False],
    [9, "Purification (384 plate)", 1, 1, 1, False],
    [10, "Transfer to EDC plate", 1, 1, 1, False],
    [11, "Aliquoting for Frag analysis", 13, 1, 4, False],
    [12, "Transformation", 13, 1, 4, False],
    [13, "Plating on Hamilton", 14, 1, 2, False],
    [14, "Picking: Manual to 96 plate x4", 16, 1, 4, False],
    [15, "Picking: Qpix to 96 plate x4", 16, 1, 4, False],
    [16, "Picking: Qpix to 384 plate", 17, 1, 1, False],
    [17, "Glycerol stock: from 96 plate", 17, 4, 1, True],
]


def upgrade():

    op.add_column('sample_transfer_type',
                  sa.Column('source_plate_count',
                            sa.Integer, default=1))
    op.add_column('sample_transfer_type',
                  sa.Column('destination_plate_count',
                            sa.Integer, default=1))
    op.add_column('sample_transfer_type',
                  sa.Column('inverted',
                            sa.Boolean, default=False))

    for row_values in desired_values:
        args = dict(zip(update_template_arg_names, row_values))
        op.execute(sa.text(update_template).bindparams(**args))


def downgrade():

    op.drop_column('sample_transfer_type', 'source_plate_count')
    op.drop_column('sample_transfer_type', 'destination_plate_count')
    op.drop_column('sample_transfer_type', 'inverted')

