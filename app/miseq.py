import csv
import StringIO
import logging
from datetime import datetime
import collections

from app import db

from flask import make_response
from flask.ext.restful import abort
from flask_login import current_user

from dbmodels import MiSeqSampleView
from twistdb.sampletrack import Sample, TransformDetail
from twistdb.ngs import NGSBarcodePair, NGSRun, NGSSequencingAnalysis
from twistdb import create_unique_id
from app.steps import ngs_run


def nps_id_details(db_session, sample_ids):
    """Raises error if some sample is not barcoded.  """

    n_total = len(sample_ids)
    if n_total == 0:
        err = "No samples -- cannot create miseq file."
        logging.error(err)
        abort(400, message=err)

    qry = (
        db_session.query(Sample)
        .filter(Sample.id.in_(sample_ids))
        .order_by(Sample.id)
    )
    samples = qry.all()

    if not samples:
        err = "NPS Sample query failed -- cannot create miseq file."
        logging.error(err)
        abort(400, message=err)

    # verify barcodes
    n_missing_i7 = sum([1 for el in samples
                        if el.i5_barcode and not el.i7_barcode])
    n_missing_i5 = sum([1 for el in samples
                        if el.i7_barcode and not el.i5_barcode])
    n_missing_both = sum([1 for el in samples
                          if not el.i5_barcode and not el.i7_barcode])
    n_missing_either = sum([1 for el in samples
                            if not el.i5_barcode or not el.i7_barcode])
    if n_missing_either != 0:
        err = "%d of %d samples are not properly barcoded ("
        err %= (n_missing_either, n_total)
        if n_missing_i5:
            err += "%d samples have i7 but no i5... " % n_missing_i5
        if n_missing_i7:
            err += "%d samples have i5 but no i7... " % n_missing_i7
        if n_missing_both:
            err += "%d samples have neither i5 nor i7... " % n_missing_both
        logging.error(err)
        abort(400, message=err + ").  Miseq requires all samples to be barcoded.")

    # verify no duplicate pairs
    pairs = collections.defaultdict(int)
    for s in samples:
        pairs[(s.i5_barcode, s.i7_barcode)] += 1
    errors = ["Barcode pair (%s, %s) used %dx" % (p[0], p[1], pairs[p])
              for p in pairs if pairs[p] > 1]
    if errors:
        logging.error(errors)
        abort(400, message=", ".join(errors))

    return samples


def echo_csv( operations, transfer_volume ):
    """
    generates string containing CSV in Echo format
    see echo_csv_for_nps()
    """
    # FIXME shouldn't this be somewhere else if it's general echo worklist generation??
    si = StringIO.StringIO()
    cw = csv.writer(si)

    cw.writerow(['Source Plate Barcode', 'Source Well',
                 'Destination Plate Barcode', 'Destination Well',
                 'Transfer Volume'])

    for oper in operations:
        # make data row
        data = [
            oper["source_plate_barcode"],
            oper["source_well_name"],
            oper["destination_plate_barcode"],
            oper["destination_well_name"],
            transfer_volume
        ]
        cw.writerow(data)

    return si.getvalue().strip('\r\n')


def echo_csv_rebatch( operations):
    """
    generates string containing CSV in Echo format
    see echo_csv_for_nps()
    """
    # FIXME shouldn't this be somewhere else if it's general echo worklist generation??
    si = StringIO.StringIO()
    cw = csv.writer(si)

    cw.writerow(['Source Plate Barcode', 'Source Well',
                 'Destination Plate Barcode', 'Destination Well',
                 'Transfer Volume'])

    for oper in operations:
        # make data row
        data = [
            oper["source_plate_barcode"],
            oper["source_well_name"],
            oper["destination_plate_barcode"],
            oper["destination_well_name"],
            oper["transfer_volume"],
            oper["marker"]

        ]
        cw.writerow(data)

    return si.getvalue().strip('\r\n')

def echo_csv_for_nps(operations, fname=None, transfer_volume=200):
    """ assumes each oper looks like {
            "source_plate_barcode": "NGS_BARCODE_PLATE_TEST2",
            "source_well_name": "A1",
            "source_sample_id":"BCS_00234",
            "source_plate_well_count": 384,
            "destination_plate_barcode":"SRN 000577 SM-37",
            "destination_well_name":"K13",
            "destination_plate_well_count":384
            "destination_sample_id": "NPS_89111c1a0327a61016dc4d017"
        }
    """
    logging.info(" %s downloaded an ECHO WORKLIST",
                 current_user.first_and_last_name)

    csvout = echo_csv( operations, transfer_volume )
    response = make_response(csvout)

    if fname is None:
        datestr = datetime.now().strftime("%Y-%m-%d_%H%M")
        fname = "ngs_barcoding_%s.echo.csv" % datestr

    assert fname[-4:] == '.csv'
    response.headers["Content-Disposition"] = "attachment; filename=%s" % fname
    return response


def next_ngs_pair(db_session):
    """Note, this method used to create an NPS (NGSPreppedSample), but now
    simply picks the next pair of NGS barcodes"""

    ngs_pair = None
    tries_remaining = 1000
    while not ngs_pair and tries_remaining > 0:
        tries_remaining -= 1
        next_index_sql = db.Sequence('ngs_barcode_pair_index_seq', schema='ngs')
        if not next_index_sql:
            raise KeyError("sequence ngs_barcode_pair_index_seq is missing")
        ngs_barcode_pair_index = db_session.execute(next_index_sql)
        print '@@ fetching ngs_barcode_pair_index:', ngs_barcode_pair_index
        ngs_pair = db_session.query(NGSBarcodePair).get(ngs_barcode_pair_index)
        print '@@ got:', ngs_pair, 'from', NGSBarcodePair, db_session.query(NGSBarcodePair).count()

    if not ngs_pair:
        raise KeyError("ngs_barcode_pair_index %s not found"
                       % ngs_barcode_pair_index)

    return ngs_pair
