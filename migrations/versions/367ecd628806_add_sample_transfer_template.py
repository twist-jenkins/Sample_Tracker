"""add sample_transfer_template

Revision ID: 367ecd628806
Revises: 284f24a958d6
Create Date: 2015-07-02 09:01:01.382734

"""

# revision identifiers, used by Alembic.
revision = '367ecd628806'
down_revision = '284f24a958d6'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, Text


def insert_rows_simple_table(lookup_table,values_list):
    ins = lookup_table.insert()
    for value in values_list:
        new_row = ins.values(name=value)
        op.execute(new_row)


def upgrade():

    #
    # Create the new "sample_transfer_template" table.
    #
    op.create_table('sample_transfer_template',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    #
    # Create a template type. 
    #
    lookup_table = table('sample_transfer_template',
        column('id', Integer),
        column('name', String)
    )
    insert_rows_simple_table(lookup_table,["One to One Transfer"])

    #
    #
    #
    op.add_column('sample_transfer_type', sa.Column('transfer_template_id', sa.Integer(), default=1))

    op.create_foreign_key(
            "fk_sample_transfer_template", "sample_transfer_type", "sample_transfer_template", 
            ["transfer_template_id"], ["id"])

    #op.drop_constraint('session_app_fkey', 'session', 'foreignkey')

    #
    # Change the fake (madeup) values in the first 3 rows to the real values.
    #
    op.execute("update sample_transfer_type set name='PCA master mix addition', transfer_template_id=1 where id = 1");
    op.execute("update sample_transfer_type set name='post-PCA-PCR purification', transfer_template_id=1  where id = 2");
    op.execute("update sample_transfer_type set name='Cloning', transfer_template_id=1  where id = 3");

    #
    # Now insert all the remaining transfer types.
    #    
    lookup_table = table('sample_transfer_type',
        column('id', Integer),
        column('name', String),
        column('transfer_template_id', Integer)
    )
    data = [
        "Transformation","Plating on Q-pix","Plating on Hamilton","Picking colonies on Q-pix",
        "Glycerol stock","RCA","Pick for miniprep", "Pick for primer removal","Pick for shipment"
    ]
    ins = lookup_table.insert()
    for value in data:
        new_row = ins.values(name=value,transfer_template_id=1)
        op.execute(new_row)

    
    


def downgrade():
    pass
