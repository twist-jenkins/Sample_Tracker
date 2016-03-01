"""Generate synthesis_run_item rows for the WARP3 fixtures.

Here we have to take into account that the WARP3 genes have a mix of
Uni9 and 10 genes. We also want a random mix of Amp and Kan markers
so that we can test out the rebatching by antibiotic code.
"""

import random
import pandas as pd

from twistdb import create_unique_id

SRI_HEADER = ["id","synthesis_run_id","cluster_design_id",
              "assigned_feature_loc","extraction_sample_id"]
SAMPLE_HEADER = ["id","plate_id","plate_well_code","order_item_id",
                 "cloning_process_id","name","mol_type"]


# This is actually CSV but we have to call it something else otherwise
# the seed_data() method will try to load it ...
infile = "WARP3_cluster_map.txt"
with open(infile, "r") as gfile:
    cluster_map = pd.read_csv(gfile)

oi_file = "order_item.txt"
with open(oi_file, "r") as ofile:
    oi = pd.read_csv(ofile)

dna_file = "dna_molecule.txt"
with open(dna_file, "r") as dnafile:
    dna = pd.read_csv(dnafile)

d_file = "work_order/design.csv"
with open(d_file, "r") as dfile:
    d = pd.read_csv(dfile)

cd_file = "work_order/cluster_design.csv"
with open(cd_file, "r") as cdfile:
    cd = pd.read_csv(cdfile)

s_ids = create_unique_id("S_")
sri_ids = create_unique_id("SRI_")

# Create a dict of CLO IDs for each of Uni9 and Uni10 for AMP/KAN
clo_ids = {
    'Uni9': {
        1: 'CLO_564c1af300bc150fa632c63d',
        2: 'CLO_564c1af300bc150fa632c63e'
    },
    'Uni10': {
        1: 'CLO_56d5260f00bc152a1e9ec797',
        2: 'CLO_56d5260f00bc152a1e9ec798'
    }
}

s = []
sri = []
for i, row in cluster_map.iterrows():
    plate_id = row['plate_name']

    oi_row = oi.ix[oi.id == row['woi']]
    oid = oi.ix[oi.id == row['woi'], 'id'].values[0]

    # Choose 75% to be NHA2 (PK 2), 25% to be NHA1 (PK 1)
    oi.ix[oi.id == row['woi'], 'part_number_pk'] = random.choice([1,2,2,2])

    # if oid == 'WOI_56d00e21f40d163883076224':
    #     import ipdb; ipdb.set_trace()
    design = d.ix[d.order_item_id == oid, 'id'].values[0]
    cdesign = cd.ix[cd.design_id == design, 'id'].values[0]

    # Find the row for DNA molecule and randomly choose a resistance marker
    if (oi.ix[oi.id == row['woi'], 'part_number_pk'] == 2).bool():
        dna.ix[dna.id == oid, 'resistance_marker_pk'] = random.choice([1,2])  # randomly amp or kan

        # Then pick a CLO based on resistance marker PK and Uni
        clo = clo_ids[row['Uni']][
            dna.ix[dna.id == oid, 'resistance_marker_pk'].values[0]]

        dna.ix[dna.id == oid, 'cloning_process_id'] = clo

    # Emit row for synthesis_run_item
    sid = "S_" + plate_id + "_" + str(row['cluster']).zfill(4)
    sri_row = pd.Series([sri_ids(), 1, cdesign, str(row['cluster']), sid],
                        index=SRI_HEADER)
    sri.append(sri_row)

    plate_well_code = int("66144" + str(row['cluster']).zfill(4))

    # clo_key = random.choice(clo_ids[row['Uni']].keys())
    # clo = clo_ids[row['Uni']][clo_key]

    gname = "%s/%s cluster %d" % (row['srn'], plate_id, row['cluster'])
    s_row = pd.Series([sid, plate_id, plate_well_code, oid, '', gname, 'DNA'],
                      index=SAMPLE_HEADER)
    s.append(s_row)

pd.DataFrame(oi).to_csv("work_order/order_item.csv", index=False)
pd.DataFrame(dna).to_csv("work_order/dna_molecule.csv", index=False)

pd.DataFrame(sri).to_csv("synthesis/synthesis_run_item.csv", index=False)
pd.DataFrame(s).to_csv("sampletrack/sample.csv", index=False)
