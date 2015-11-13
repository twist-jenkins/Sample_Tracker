"""add transformSpecId to sample_transfer table

Revision ID: e21142f8439
Revises: 3cad6c561c85
Create Date: 2015-11-11 10:25:32.817750

"""

# revision identifiers, used by Alembic.
revision = 'e21142f8439'
down_revision = '3cad6c561c85'

from alembic import op
import sqlalchemy as db


def upgrade():
    op.add_column('sample_transfer',
                  db.Column('sample_transform_spec_id',
                            db.Integer(),
                            db.ForeignKey('sample_transform_spec.spec_id')))

    op.create_foreign_key(
        "fk_sample_transfer_transform_spec",
        "sample_transfer", "sample_transform_spec",
        ["sample_transform_spec_id"], ["spec_id"])


def downgrade():
    op.execute("alter table sample_transfer"
               " drop column if exists "
               " sample_transform_spec_id")
