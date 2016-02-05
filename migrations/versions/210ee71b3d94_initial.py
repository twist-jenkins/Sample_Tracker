"""initial

Revision ID: 210ee71b3d94
Revises: None
Create Date: 2015-06-26 15:39:42.709699

"""

# revision identifiers, used by Alembic.
revision = '210ee71b3d94'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    '''
    op.create_table('sample_transfer_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('sample_transfer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transfer_type_id', sa.Integer(), nullable=False),
    sa.Column('operator_id', sa.String(length=10), nullable=False),
    sa.Column('date_transfer', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['transfer_type_id'], ['sample_transfer_type.id'], ),
    sa.ForeignKeyConstraint(['operator_id'], ['operator.operator_id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('sample_transfer_detail',
    sa.Column('sample_transfer_id', sa.Integer(), nullable=False),
    sa.Column('item_order_number', sa.Integer(), nullable=False),
    sa.Column('source_sample_plate_id', sa.String(length=40), nullable=False),
    sa.Column('source_well_id', sa.Integer(), nullable=False),
    sa.Column('destination_sample_plate_id', sa.String(length=40), nullable=False),
    sa.Column('destination_well_id', sa.Integer(), nullable=False),

    sa.ForeignKeyConstraint(['sample_transfer_id'], ['sample_transfer.id'], ),
    sa.ForeignKeyConstraint(['source_sample_plate_id'], ['sample_plate.sample_plate_id'], ),
    #sa.ForeignKeyConstraint(['source_well_id'], ['sample_plate_layout.well_id'], ),
    sa.ForeignKeyConstraint(['destination_sample_plate_id'], ['sample_plate.sample_plate_id'], ),
    #sa.ForeignKeyConstraint(['destination_well_id'], ['sample_plate_layout.well_id'], ),

    sa.PrimaryKeyConstraint('sample_transfer_id', 'item_order_number')
    )
    '''


def downgrade():
    
    op.drop_table('sample_transfer_type')
    op.drop_table('sample_transfer')
    op.drop_table('sample_transfer_detail')
