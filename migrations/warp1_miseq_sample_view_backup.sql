
select * from sampletrack.miseq_sample_view;


create view miseq_sample_view as
select npsdtl.sample_id,
        npsdtl.parent_sample_id,
        npsdtl.notes,
        i7seq.name as i7_seq_name,
        i7seq.sequence as i7_seq,
        npsdtl.i7_sequence_id,
        i5seq.name as i5_seq_name,
        i5seq.sequence as i5_seq,
        npsdtl.i5_sequence_id,
        parent.description as parent_description
        from backend.ngs_prepped_sample npsdtl
        join backend.sample npsamp on npsamp.sample_id=npsdtl.sample_id
            and npsamp.type_id = 'ngs_prepped_sample'
        join backend.sample parent on parent.sample_id=npsdtl.parent_sample_id
        join backend.barcode_sequence i7seq on i7seq.id = npsdtl.i7_sequence_id
        join backend.barcode_sequence i5seq on i5seq.id = npsdtl.i5_sequence_id;


------ NEXT PROJECT: reenable constraints

--- constraints as of Wedn morning:
ALTER TABLE "tag"."sample_tag_join" ADD CONSTRAINT "sample_tag_join_tag_id_fkey" FOREIGN KEY (tag_id) REFERENCES tag.tag(tag_id);
ALTER TABLE "public"."wafer" ADD CONSTRAINT "wafer_wafer_type_id_fkey" FOREIGN KEY (wafer_type_id) REFERENCES wafer_type(wafer_type_id);
ALTER TABLE "public"."synthesis_cluster" ADD CONSTRAINT "synthesis_cluster_run_id_fkey" FOREIGN KEY (run_id) REFERENCES synthesis_run(run_id);
ALTER TABLE "ngs"."ngs_run" ADD CONSTRAINT "ngs_run_instrument_pk_fkey" FOREIGN KEY (instrument_pk) REFERENCES instrument(pk);

-- constraints from a fresh develop



