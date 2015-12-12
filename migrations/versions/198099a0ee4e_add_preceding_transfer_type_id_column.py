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
                  db.Column('prior_transfer_type_id',
                            db.Integer(),
                            db.ForeignKey('sample_transfer_type.id')))

    op.execute("update sample_transfer_type"
               " set prior_transfer_type_id = id - 1"
               " where id - 1 in (select id from sample_transfer_type)")

    prior_sql = """
      create view sampletrack.plate_prior_step_view as
      select
          subq.sample_plate_id,
          sp.external_barcode,
          sp.type_id,
          sp.status,
          subq.sample_transfer_type_id,
          subq.date_transfer,
          subq.name,
          subq.sample_transfer_template_id,
          subq.prior_transfer_type_id
       from (
          Select distinct
              det.destination_sample_plate_id as sample_plate_id,
              det.sample_transfer_id,
              st.sample_transfer_type_id,
              st.date_transfer,
              stt.name,
              stt.sample_transfer_template_id,
              stt.prior_transfer_type_id,
              Row_Number() Over ( Partition By det.destination_sample_plate_id
                                  Order By date_transfer ) As rnk
          From  sample_transfer_detail det
          join sample_transfer st on st.id = det.sample_transfer_id
          join sample_transfer_type stt on stt.id = st.sample_transfer_type_id

      ) as subq
      join sample_plate sp on sp.sample_plate_id = subq.sample_plate_id
      where subq.rnk = 1; -- most recent step
    """
    op.execute(prior_sql)


def downgrade():
    op.execute("drop view if exists plate_prior_step_view")

    op.execute("alter table sample_transfer_type"
               " drop column if exists "
               " prior_transfer_type_id")



