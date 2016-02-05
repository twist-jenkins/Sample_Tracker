----- NEXT PROJECT: new sample plates warp 1.2,3,4

create table public.backup_sample_plate as select * from sampletrack.sample_plate;

create table public.backup_sample_plate_layout as select * from sampletrack.sample_plate_layout;

create table public.backup_sample as select * from backend.sample;

create table public.backup_gene_assembly_sample as select * from backend.gene_assembly_sample;


select * from sampletrack.sample_plate;




INSERT INTO sampletrack.sample_plate ("plate_id","type_id","operator_id","storage_location","date_created","name","description","external_barcode","status") VALUES (E'SPLT_WARP1.2',E'SPTT_1009',E'CL',E'LOC_0064',E'26-JAN-16 11:01:00',E'PLATE_WARP1.2',E'PLATEDESC_WARP1.2',E'SRN-WARP1.2',E'new');

INSERT INTO sampletrack.sample_plate ("plate_id","type_id","operator_id","storage_location","date_created","name","description","external_barcode","status") VALUES (E'SPLT_WARP1.3',E'SPTT_1009',E'CL',E'LOC_0064',E'26-JAN-16 11:04:00',E'PLATE_WARP1.3',E'PLATEDESC_WARP1.3',E'SRN-WARP1.3',E'new');

INSERT INTO sampletrack.sample_plate ("plate_id","type_id","operator_id","storage_location","date_created","name","description","external_barcode","status") VALUES (E'SPLT_WARP1.4',E'SPTT_1009',E'CL',E'LOC_0064',E'28-JAN-16 15:25:00',E'PLATE_WARP1.4',E'PLATEDESC_WARP1.4',E'SRN-WARP1.4',E'new');

-- done

select * from backend.sample where sample_id like 'GA_WARP1_TEST1%';

INSERT INTO backend.sample("sample_id","type_id","order_item_id","date_created","name","description","external_barcode","operator_id")
select E'GA_WARP1.2_' || right(sample_id, 4),
E'gene_assembly',NULL,E'28-JAN-16 15:52:00',
E'SRN-WARP1.2 CLUST ' || right(sample_id, 4),
E'SRN-WARP1.2 CLUST ' || right(sample_id, 4),
NULL,NULL
from backend.sample where sample_id like 'GA_WARP1_TEST1%';

INSERT INTO backend.sample("sample_id","type_id","order_item_id","date_created","name","description","external_barcode","operator_id")
select E'GA_WARP1.3_' || right(sample_id, 4),
E'gene_assembly',NULL,E'28-JAN-16 15:53:00',
E'SRN-WARP1.3 CLUST ' || right(sample_id, 4),
E'SRN-WARP1.3 CLUST ' || right(sample_id, 4),
NULL,NULL
from backend.sample where sample_id like 'GA_WARP1_TEST1%';

INSERT INTO backend.sample("sample_id","type_id","order_item_id","date_created","name","description","external_barcode","operator_id")
select E'GA_WARP1.4_' || right(sample_id, 4),
E'gene_assembly',NULL,E'28-JAN-16 15:54:00',
E'SRN-WARP1.4 CLUST ' || right(sample_id, 4),
E'SRN-WARP1.4 CLUST ' || right(sample_id, 4),
NULL,NULL
from backend.sample where sample_id like 'GA_WARP1_TEST1%';

-- done

insert into backend.gene_assembly_sample(sample_id)
select
E'GA_WARP1.2_' || right(sample_id, 4)
from backend.sample where sample_id like 'GA_WARP1_TEST1%';

insert into backend.gene_assembly_sample(sample_id)
select
E'GA_WARP1.3_' || right(sample_id, 4)
from backend.sample where sample_id like 'GA_WARP1_TEST1%';

insert into backend.gene_assembly_sample(sample_id)
select
E'GA_WARP1.4_' || right(sample_id, 4)
from backend.sample where sample_id like 'GA_WARP1_TEST1%';

-- done

insert into sampletrack.sample_plate_layout
("plate_id","well_id","sample_id","operator_id","row","column","date_created","notes","status")
select 'SPLT_WARP1.2', well_id,
E'GA_WARP1.2_' || right(sample_id, 4),
operator_id, row, "column",  E'26-JAN-16 13:51:01', NULL, status
from sampletrack.sample_plate_layout
where plate_id = 'SPLT_WARP1_TEST1';

insert into sampletrack.sample_plate_layout
("plate_id","well_id","sample_id","operator_id","row","column","date_created","notes","status")
select 'SPLT_WARP1.3', well_id,
E'GA_WARP1.3_' || right(sample_id, 4),
operator_id, row, "column",  E'26-JAN-16 13:53:01', NULL, status
from sampletrack.sample_plate_layout
where plate_id = 'SPLT_WARP1_TEST1';

insert into sampletrack.sample_plate_layout
("plate_id","well_id","sample_id","operator_id","row","column","date_created","notes","status")
select 'SPLT_WARP1.4', well_id,
E'GA_WARP1.4_' || right(sample_id, 4),
operator_id, row, "column",  E'26-JAN-16 13:54:01', NULL, status
from sampletrack.sample_plate_layout
where plate_id = 'SPLT_WARP1_TEST1';

-- done
