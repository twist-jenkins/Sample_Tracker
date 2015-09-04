"""add sample_transfer_template_details table

Revision ID: 490846e6ac8d
Revises: 367ecd628806
Create Date: 2015-09-03 17:06:15.882757

"""

# revision identifiers, used by Alembic.
revision = '490846e6ac8d'
down_revision = '367ecd628806'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('sample_transfer_template_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_transfer_template_id', sa.Integer(), nullable=False),

    sa.Column('source_plate_number', sa.Integer(), nullable=False),
    sa.Column('source_plate_well_count', sa.Integer(), nullable=False),
    sa.Column('source_plate_well_id', sa.Integer(), nullable=False),
    sa.Column('source_plate_well_id_string', sa.String(length=10), default="", nullable=False),

    sa.Column('destination_plate_number', sa.Integer(), nullable=False),
    sa.Column('destination_plate_well_count', sa.Integer(), nullable=False),
    sa.Column('destination_plate_well_id', sa.Integer(), nullable=False),
    sa.Column('destination_plate_well_id_string', sa.String(length=10), default="", nullable=False),

    sa.ForeignKeyConstraint(['sample_transfer_template_id'], ['sample_transfer_template.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('sample_transfer_template_details')
