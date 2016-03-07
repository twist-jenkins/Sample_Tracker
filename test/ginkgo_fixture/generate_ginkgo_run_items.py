"""Generate synthesis_run_item rows for Ginkgo fixtures.

Parse the writer file used in the WARP2 run, identify each Ginkgo
gene put on the writer from its entry in the work_order.order_item
table and create synthesis_run_item joins and sample records for
the extraction.
"""

import json
import pandas as pd

from twistdb import create_unique_id

SRI_HEADER = ["id","synthesis_run_pk","cluster_design_id",
              "assigned_feature_loc","extraction_sample_id"]
SAMPLE_HEADER = ["id","plate_id","plate_well_code","order_item_id",
                 "cloning_process_id","name","mol_type"]


infile = "Ginkgo_Titin_chip.xlsx"
with open(infile, "r") as gfile:
    ginkgo = pd.read_excel(gfile, sheetname='clusters', skiprows=5)
ginkgo = ginkgo.rename(columns=lambda x: x.replace(':', ''))

oi_file = "work_order/order_item.csv"
with open(oi_file, "r") as ofile:
    oi = pd.read_csv(ofile)

d_file = "work_order/design.csv"
with open(d_file, "r") as dfile:
    d = pd.read_csv(dfile)

cd_file = "work_order/cluster_design.csv"
with open(cd_file, "r") as cdfile:
    cd = pd.read_csv(cdfile)


s_ids = create_unique_id("S_")
sri_ids = create_unique_id("SRI_")
clo = "CLO_564c1af300bc150fa632c63d"  # cloning process, Amp w/ Uni9
plate_id = "PLT_WARP2.1"

s = []
sri = []
for i, row in ginkgo.iterrows():
    if row.cluster_type != 'gene_assembly' or "{" not in row.description:
        continue
    cluster = row.cluster_num
    gname = json.loads(row.description)['customer_item_id']
    oid = oi.ix[oi.customer_line_item_id == gname, 'id'].values[0]
    design = d.ix[d.order_item_id == oid, 'id'].values[0]
    cdesign = cd.ix[cd.design_id == design, 'id'].values[0]

    # Emit row for synthesis_run_item
    sid = "S_WARP2_" + str(cluster).zfill(4)
    sri_row = pd.Series([sri_ids(), 1, cdesign, str(cluster), sid],
                        index=SRI_HEADER)
    sri.append(sri_row)

    plate_well_code = int("66144" + str(cluster).zfill(4))

    s_row = pd.Series([sid, plate_id, plate_well_code, oid, clo, gname, 'DNA'],
                      index=SAMPLE_HEADER)
    s.append(s_row)

pd.DataFrame(sri).to_csv("synthesis/synthesis_run_item.csv", index=False)
pd.DataFrame(s).to_csv("sampletrack/sample.csv", index=False)
