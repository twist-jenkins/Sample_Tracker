"""Add Resistance Marker to sample view.

Revision ID: 2508b1c64724
Revises: e21142f8439
Create Date: 2015-11-11 15:59:57.903424

"""

# revision identifiers, used by Alembic.
revision = '2508b1c64724'
down_revision = 'e21142f8439'

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.execute('drop view sample_view;')
    op.execute('drop view gene_assembly_sample_view;')
    op.execute('drop view cloned_sample_view;')

    ga_sql = """
        create view gene_assembly_sample_view
        as
        --GeneAssemblySample with details
        -- Gene assembly samples are made up of other sequences
        -- (and they have a sequence assembly identifier (SAN ID))
        select
        SAMP.sample_id as sample_id,
        SAMP.type_id as sample_type,
        SAMP.date_created as sample_date_created,
        CLP.cloning_process_id AS cloning_process_id_plan,
        VS.resistance_marker AS resistance_marker_plan,
        NULL::text AS cloning_process_id_actual,
        SAMP.name as sample_name,
        SAMP.operator_id as sample_operator_id,
        OP.first_name || ' ' || OP.last_name as sample_operator_first_and_last_name,
        SAMP.description as sample_description,
        -- SAMP.external_barcode as sample_external_barcode,
        SAMP.parent_process_id as sample_parent_process_id,
        SAMP.status as sample_status,
        -- SAMP.fwd_primer_ps_id as sample_fwd_primer_ps_id,
        -- SAMP.rev_primer_ps_id as sample_rev_primer_ps_id,
        -- GA.parent_sample_id as ga_parent_sample_id,
        COR.order_id as cor_order_id,
        COR.order_date as cor_order_date,
        COR.customer_id as cor_customer_id,
        CID.institution_id as cid_institution_id,
        COI.order_item_id as coi_order_item_id,
        COI.line_item_number as coi_line_item_number,
        COI.order_configuration_id as coi_order_configuration_id,
        COI.received_datetime as coi_received_datetime,
        COI.due_datetime as coi_due_datetime,
        COI.priority as coi_priority,
        COI.order_item_status_id as coi_order_item_status_id,
        COI.order_item_type_id as coi_order_item_type_id,
        COI.order_item_delivery_format_id as coi_order_item_delivery_format_id,
        COI.customer_sequence_num as coi_customer_sequence_num,
        COI.customer_line_item_id as coi_customer_line_item_id,
        COI.customer_line_item_description as coi_customer_line_item_description,
        COI.description as coi_description,
        COI.notes as coi_notes,
        -- COI.status_notes as coi_status_notes,
        GA.sagi_id as ga_sagi_id,
        SAGI.sag_id as sagi_sag_id,
        SAGI.date_created as sagi_date_created,
        SAGG.date_created as sagg_date_created,
        SAGG.fivep_ps_id as sagg_fivep_ps_id,
        SAGG.threep_ps_id as sagg_threep_ps_id,
        SAGG.fivep_as_id as sagg_fivep_as_id,
        SAGG.fivep_as_dir as sagg_fivep_as_dir,
        SAGG.threep_as_id as sagg_threep_as_id,
        SAGG.threep_as_dir as sagg_threep_as_dir,
        GS.sequence_id as gs_sequence_id,
        SEQ.seq as gs_seq,
        SEQ.name as gs_name,
        SEQ.description as gs_description
        from gene_assembly_sample GA
        inner join sample SAMP on SAMP.sample_id = GA.sample_id
        inner join sag_instance SAGI on SAGI.sagi_id = GA.sagi_id
        inner join sag_node_gene SAGG on SAGG.sag_id = SAGI.sag_id
        inner join gene_sequence GS on GS.sequence_id = SAGG.sequence_id
        inner join sequence SEQ on SEQ.sequence_id = GS.sequence_id
        inner join synthesis_cluster_sample_join SCSJ on SCSJ.sample_id = GA.sample_id
        inner join synthesis_cluster CLST on CLST.cluster_id = SCSJ.cluster_id -- and CLST.sagi_id = SAGI.sagi_id
        left outer join cloning_plan CLP on clp.cluster_id = CLST.cluster_id
        left outer join cloning_process CLO on clo.process_id = CLP.cloning_process_id
        left outer join vector_sequence VS on vs.sequence_id = CLO.vector_sequence_id
        left outer join order_item COI on COI.order_item_id = CLST.order_item_id
        left outer join "order" COR on COR.order_configuration_id = COI.order_configuration_id
        left outer join customer CID on CID.customer_id = COR.customer_id
        left outer join operator OP on OP.operator_id = SAMP.operator_id
        where SAMP.type_id='gene_assembly';
        """
    op.execute(ga_sql)

    cs_sql = """
        create view cloned_sample_view
        as
        -- ClonedSample with details
        select
        CSSAMP.sample_id as sample_id,
        CSSAMP.type_id as sample_type,
        CSSAMP.date_created as sample_date_created,
        CLP.cloning_process_id AS cloning_process_id_plan,
        VS.resistance_marker AS resistance_marker_plan,
        CSSAMP.parent_process_id AS cloning_process_id_actual,
        CSSAMP.name as sample_name,
        CSSAMP.operator_id as sample_operator_id,
        OP.first_name || ' ' || OP.last_name as sample_operator_first_and_last_name,
        CSSAMP.description as sample_description,
        -- SAMP.external_barcode as sample_external_barcode,
        CSSAMP.parent_process_id as sample_parent_process_id,
        CSSAMP.status as sample_status,
        -- SAMP.fwd_primer_ps_id as sample_fwd_primer_ps_id,
        -- SAMP.rev_primer_ps_id as sample_rev_primer_ps_id,
        -- GA.parent_sample_id as ga_parent_sample_id,
        COR.order_id as cor_order_id,
        COR.order_date as cor_order_date,
        COR.customer_id as cor_customer_id,
        CID.institution_id as cid_institution_id,
        COI.order_item_id as coi_order_item_id,
        COI.line_item_number as coi_line_item_number,
        COI.order_configuration_id as coi_order_configuration_id,
        COI.received_datetime as coi_received_datetime,
        COI.due_datetime as coi_due_datetime,
        COI.priority as coi_priority,
        COI.order_item_status_id as coi_order_item_status_id,
        COI.order_item_type_id as coi_order_item_type_id,
        COI.order_item_delivery_format_id as coi_order_item_delivery_format_id,
        COI.customer_sequence_num as coi_customer_sequence_num,
        COI.customer_line_item_id as coi_customer_line_item_id,
        COI.customer_line_item_description as coi_customer_line_item_description,
        COI.description as coi_description,
        COI.notes as coi_notes,
        -- COI.status_notes as coi_status_notes,
        GA.sagi_id as ga_sagi_id,
        SAGI.sag_id as sagi_sag_id,
        SAGI.date_created as sagi_date_created,
        SAGG.date_created as sagg_date_created,
        SAGG.fivep_ps_id as sagg_fivep_ps_id,
        SAGG.threep_ps_id as sagg_threep_ps_id,
        SAGG.fivep_as_id as sagg_fivep_as_id,
        SAGG.fivep_as_dir as sagg_fivep_as_dir,
        SAGG.threep_as_id as sagg_threep_as_id,
        SAGG.threep_as_dir as sagg_threep_as_dir,
        GS.sequence_id as gs_sequence_id,
        SEQ.seq as gs_seq,
        SEQ.name as gs_name,
        SEQ.description as gs_description
        from cloned_sample CS
        inner join sample CSSAMP on CSSAMP.sample_id = CS.sample_id
        inner join sample GASAMP on GASAMP.sample_id = CS.parent_sample_id
        inner join gene_assembly_sample GA on GA.sample_id = GASAMP.sample_id
        inner join sag_instance SAGI on SAGI.sagi_id = GA.sagi_id
        inner join sag_node_gene SAGG on SAGG.sag_id = SAGI.sag_id
        inner join gene_sequence GS on GS.sequence_id = SAGG.sequence_id
        inner join sequence SEQ on SEQ.sequence_id = GS.sequence_id
        inner join synthesis_cluster_sample_join SCSJ on SCSJ.sample_id = GA.sample_id
        inner join synthesis_cluster CLST on CLST.cluster_id = SCSJ.cluster_id -- and CLST.sagi_id = SAGI.sagi_id
        left outer join cloning_plan CLP on CLP.cluster_id = CLST.cluster_id
        left outer join cloning_process CLO on clo.process_id = CLP.cloning_process_id
        left outer join vector_sequence VS on vs.sequence_id = CLO.vector_sequence_id
        left outer join order_item COI on COI.order_item_id = CLST.order_item_id
        left outer join "order" COR on COR.order_configuration_id = COI.order_configuration_id
        left outer join customer CID on CID.customer_id = COR.customer_id
        left outer join operator OP on OP.operator_id = CSSAMP.operator_id
        where CSSAMP.type_id='cloned_sample';
        """
    op.execute(cs_sql)

    sv_sql = """
        create or replace view sample_view
        as
        select * from cloned_sample_view
        union all
        select * from gene_assembly_sample_view;
    """
    op.execute(sv_sql)


def downgrade():
    pass
