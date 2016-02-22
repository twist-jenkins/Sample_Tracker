from collections import defaultdict
import datetime
import math
import csv
from cStringIO import StringIO



def create_source( db, vector_barcode ):
    """
    """
    from twistdb.sampletrack import Plate, TransformSpec
    from app.miseq import echo_csv
    from app.constants import TRANS_TYPE_PCA_PREPLANNING as PCA_PREPLANNING

    rows, cmds = [], []

    N_days_ago = datetime.datetime.now() - datetime.timedelta( days=SEARCH_LAST_N_DAYS )
    specjs = []
    for spec in db.query(TransformSpec) \
                  .filter( TransformSpec.date_created >= N_days_ago ):
        srcs = spec.data_json['sources']

        if ( len(srcs) == 1
             and srcs[0]['details']['id'] == bulk_barcode
             and spec.data_json['details']['transfer_type_id'] == PCA_PREPLANNING ):

            specjs.append( spec.data_json )

    return rows, cmds
