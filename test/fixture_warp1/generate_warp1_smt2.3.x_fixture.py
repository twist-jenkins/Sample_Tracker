"""Generate a fixture that creates the WARP1.x plate but in smt2.3.x schema.

The WARP 1.x plates are only in the warp1smt database but in a much older
version of twistdb's schema.
"""

import logging
import datetime
import pandas as pd

from twistdb import create_unique_id

logging.basicConfig(level=logging.INFO)

WOR_HEADER = ["id","_human_id","date_received","twist_sales_order_id","sf_customer_id","customer_priority","internal_rank","description","notes"]
OIG_HEADER = ["id","_human_id","order_id","name","customer_priority","planning_rank","description"]
OI_HEADER = ["id","_human_id","item_type","order_id","item_group_id","item_category","part_number_pk","delivery_format_id","order_definition","line_item_number","received_datetime","due_datetime","priority","sfdc_item_id","customer_line_item_id","customer_line_item_description","notes"]
DNA_HEADER = ["id","difficulty_pk","difficulty_label","difficulty_score","sequence","resistance_marker_pk","cloning_process_id","primer_pair_id"]
CDESIGN_HEADER = ["id","design_id","batching_group_pk","design_rank","category_num","category_pk","details","longest_oligo_length","overlap_perc_gc","cloning_process_id","primer_pair_pk","requested_feature_loc","requested_dest_well","requested_extraction"]
DESIGN_HEADER = ["id","order_item_id","design_rank","design","longest_oligo_length","overlap_perc_gc"]
SRN_HEADER = ["pk","name","chip_id","added_datetime","control_set_id","status_pk","operator_id"]
SRI_HEADER = ["id","synthesis_run_pk","cluster_design_id",
              "assigned_feature_loc","extraction_sample_id"]
PLATE_HEADER = ["id","type_id","operator_id","date_created","storage_location","description","name","external_barcode","status"]
SAMPLE_HEADER = ["id","plate_id","plate_well_code","order_item_id",
                 "cloning_process_id","name","mol_type"]


# This is actually CSV but we have to call it something else otherwise
# the seed_data() method will try to load it ...
infile = "WARP1_clusters.txt"
with open(infile, "r") as gfile:
    cluster_map = pd.read_csv(gfile)

infile = "WARP1_genes.txt"
with open(infile, "r") as gfile:
    gene_map = pd.read_csv(gfile)

# Setup ID generators
wo_ids = create_unique_id("WOR_")
oig_ids = create_unique_id("OIG_")
oi_ids = create_unique_id("OI_")
des_ids = create_unique_id("DES_")
cld_ids = create_unique_id("CLD_")
s_ids = create_unique_id("S_")
sri_ids = create_unique_id("SRI_")

# cloning process, Amp w/ Uni9
primer_pair_id = 1
clo = "CLO_564c1af300bc150fa632c63d"

# Remove empty clusters
cluster_map = cluster_map[~pd.isnull(cluster_map.name)]

# Create work_order
order_id = wo_ids()
group_id = oig_ids()

wo = pd.Series([order_id,10001,datetime.datetime.now(),None,None,100,100,
                'WARP1 test plate', None], index=WOR_HEADER)
pd.DataFrame(wo).transpose().to_csv("work_order/work_order.csv", index=False)

oig = pd.Series([group_id,10001,order_id,'WARP1 test group',100,100,
                'WARP1 test group'], index=OIG_HEADER)
pd.DataFrame(oig).transpose().to_csv("work_order/order_item_group.csv", index=False)

# Create order items
oi_list = []
dna_list = []
design_list = []
cdesign_list = []

name_to_oi = {}
human_id = 1000001
line_item_num = 0
logging.info("Generating work_order rows.")
for i, row in gene_map.iterrows():
    human_id += 1
    oid = oi_ids()
    line_item_num += 1
    name_to_oi[row.Name] = oid
    this_oi = pd.Series([oid, human_id, 'dna_molecule',
                         order_id, group_id, 'production',
                         2, 1, None, line_item_num, datetime.datetime.now(),
                         datetime.datetime.now() + datetime.timedelta(days=5),
                         100, None, row.Name, row.Name, None], index=OI_HEADER)
    oi_list.append(this_oi)

    # And then the DNA molecule
    this_dna = pd.Series([oid, 2, 'Standard',
                          1, row.Sequence, 1, clo, primer_pair_id],
                         index=DNA_HEADER)
    dna_list.append(this_dna)

    # Create design row
    did = des_ids()
    this_design = pd.Series([did, oid, 1, '{"design": "fake!"}', None, None], index=DESIGN_HEADER)
    design_list.append(this_design)

    # Create cluster_design row
    cid = cld_ids()
    this_cluster = pd.Series([cid, did, 1, 1, 1, 1, '{"design": "fake!"}', None, None,
                              clo, primer_pair_id, None,
                              None, None], index=CDESIGN_HEADER)
    cdesign_list.append(this_cluster)


order_items = pd.DataFrame(oi_list)
order_items.to_csv("work_order/order_item.csv", index=False)

dna_items = pd.DataFrame(dna_list)
dna_items.to_csv("work_order/dna_molecule.csv", index=False)

designs = pd.DataFrame(design_list)
designs.to_csv("work_order/design.csv", index=False)

cdesigns = pd.DataFrame(cdesign_list)
cdesigns.to_csv("work_order/cluster_design.csv", index=False)

# Create synthesis_runs - we need to make three per Etoro
srn_rows = []
sri_rows = []
plate_rows = []
sample_rows = []
srns = ['SRN_000767', 'SRN_000790', 'SRN_000819']
for srn in srns:
    logging.info("Creating synthesis run %s" % srn)
    pk_value = int(srn.replace("SRN_000",""))
    srn_item = pd.Series([pk_value, srn, None, datetime.datetime.now(),
                         None, 1, 'jdiggans'], index=SRN_HEADER)
    srn_rows.append(srn_item)

    # Create the plate resulting from this run
    pname = "PLT_" + srn
    plate_item = pd.Series([pname, "SPTT_1009", 'jdiggans',
                            datetime.datetime.now(), None,
                            'Titin "plate" for ' + srn, None,
                            pname, 'new'], index=PLATE_HEADER)
    plate_rows.append(plate_item)

    # And then create the SRN run items for each run
    for i, cluster in cluster_map.iterrows():
        sri_id = sri_ids()
        oid = name_to_oi[cluster['name']]
        design = designs.ix[designs.order_item_id == oid]
        cdesign = cdesigns.ix[cdesigns.design_id == design.id.values[0]]

        sri_item = pd.Series([sri_id, pk_value, cdesign.id,
                              cluster.cluster, cluster.extraction],
                             index=SRI_HEADER)
        sri_rows.append(sri_item)

        # And the sample row
        sample_id = s_ids()
        well_code = '66144' + str(cluster.cluster).zfill(4)
        s_item = pd.Series([sample_id, pname, well_code, oid, None, None, 'DNA'],
                           index=SAMPLE_HEADER)
        sample_rows.append(s_item)

logging.info("Writing results")

srns = pd.DataFrame(srn_rows)
srns.to_csv("synthesis/synthesis_runs.csv", index=False)

sris = pd.DataFrame(sri_rows)
sris.to_csv("synthesis/synthesis_run_items.csv", index=False)

plates = pd.DataFrame(plate_rows)
plates.to_csv("sampletrack/plate.csv", index=False)

samples = pd.DataFrame(sample_rows)
samples.to_csv("sampletrack/sample.csv", index=False)
