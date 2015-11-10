"""Create table sample_transform_spec

Revision ID: 1629f51b954b
Revises: da20bea3e8f
Create Date: 2015-10-15 17:25:27.408367

"""

# revision identifiers, used by Alembic.
revision = '1629f51b954b'
down_revision = 'da20bea3e8f'

import datetime

from alembic import op
import sqlalchemy as db
from sqlalchemy.dialects import postgresql


def upgrade():

    op.create_table(
        'sample_transform_spec',
        db.Column('spec_id',
                  db.Integer(),
                  primary_key=True),
        db.Column('type_id',
                  db.Integer(),
                  db.ForeignKey('sample_transfer_type.id'),
                  nullable=True),
        db.Column('status',
                  db.String(40),
                  nullable=True),
        db.Column('date_created',
                  db.DateTime,
                  default=datetime.datetime.utcnow,
                  nullable=False),
        db.Column('date_executed',
                  db.DateTime,
                  nullable=True),
        db.Column('operator_id',
                  db.String(10),
                  db.ForeignKey('operator.operator_id'),
                  nullable=False),
        db.Column('data_json', postgresql.JSON(),
                  nullable=False)
    )

    op.execute('''
DO
$$BEGIN
EXECUTE format('ALTER SEQUENCE %s START 100001'
, pg_get_serial_sequence('sample_transform_spec', 'spec_id'));
END$$;
               ''')
    ## also add FK from sample_transfer

def downgrade():
    # op.drop_table('sample_transfer_plan')
    op.drop_table('sample_transform_spec')
