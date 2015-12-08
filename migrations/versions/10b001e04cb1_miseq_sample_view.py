"""MiSeq sample view

Revision ID: 10b001e04cb1
Revises: 5a4d81becc55
Create Date: 2015-11-18 16:33:37.762888

"""

# revision identifiers, used by Alembic.
revision = '10b001e04cb1'
down_revision = '5a4d81becc55'

from alembic import op
import sqlalchemy as sa


def upgrade():

    miseq_sql = """
        create or replace view miseq_sample_view
        as
        select npsdtl.sample_id,
        npsdtl.parent_sample_id,
        npsdtl.notes,
        i7seq.name as i7_seq_name,
        i7seq.seq as i7_seq,
        npsdtl.i7_sequence_id,
        i5seq.name as i5_seq_name,
        i5seq.seq as i5_seq,
        npsdtl.i5_sequence_id,
        parent.description as parent_description,
        parent.parent_process_id
        from ngs_prepped_sample npsdtl
        join sample npsamp on npsamp.sample_id=npsdtl.sample_id
            and npsamp.type_id = 'ngs_prepped_sample'
        join sample parent on parent.sample_id=npsdtl.parent_sample_id
        join sequence i7seq on i7seq.sequence_id = npsdtl.i7_sequence_id
            and i7seq.type_id=3
        join sequence i5seq on i5seq.sequence_id = npsdtl.i5_sequence_id
            and i5seq.type_id=3;
    """
    op.execute(miseq_sql)


def downgrade():
    op.execute("drop view if exists miseq_sample_view")
