"""Add preceding_transfer_type_id column.

Revision ID: 198099a0ee4e
Revises: 3111d557c83a
Create Date: 2015-12-11 14:25:33.802593

"""

# revision identifiers, used by Alembic.
revision = '198099a0ee4e'
down_revision = '3111d557c83a'

from alembic import op
import sqlalchemy as db


def upgrade():
    op.add_column('sample_transfer_type',
                  db.Column('preceding_transfer_type_id',
                            db.Integer(),
                            db.ForeignKey('sample_transfer_type.id')))

    op.execute("update sample_transfer_type"
               " set preceding_transfer_type_id = id + 1"
               " where id + 1 in (select id from sample_transfer_type)")


def downgrade():
    op.execute("alter table sample_transfer_type"
               " drop column if exists "
               " preceding_transfer_type_id")

