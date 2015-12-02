import csv
import StringIO
import logging
import json
from datetime import datetime

from flask import make_response
from flask.ext.restful import abort
from flask_login import current_user

from dbmodels import MiSeqSampleView

""" some of the templates and logic is from twistbio.util.miseq.py.
That code will continue to be used by R&D.
Pasting the relevant bits here instead of importing twist_core."""

FORBIDDEN_CHARS_MISEQ = list("""?()[]/\=+<>:;"',*^|&""")
FORBIDDEN_CHARS_NEXTSEQ = list("""?()[]/\=+<>:;"',*^|&.@""")
FORBIDDEN_CHARS = FORBIDDEN_CHARS_NEXTSEQ

# note that this is for resequencing workflow only now
SAMPLE_SHEET_TEMPLATE = """[Header]
IEMFileVersion,4
Investigator Name,%s %s
Experiment Name,%s
Date,%s
Workflow,%s
Application,%s
Assay,%s
Description,%s
Chemistry,%s

[Reads]
%d
%d

[Settings]
FilterPCRDuplicates,1
ReverseComplement,0
VariantFilterQualityCutoff,30
QualityScoreTrim,%d
Adapter,%s

[Data]
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,I5_Index_ID,index2,GenomeFolder,Sample_Project,Description
%s
"""


def strip_forbidden_chars(in_str, replace_with_char=" ", max_len=1000):
    """Return clean string"""
    if not in_str:
        return ""
    clean_chars = []
    for c in in_str:
        if c in FORBIDDEN_CHARS:
            clean_chars.append(replace_with_char)
        else:
            clean_chars.append(c)
    if len(clean_chars) > max_len:
        return ''.join(clean_chars)[0:max_len] + "..."
    return ''.join(clean_chars)


def miseq_csv_template(rows, run_id):

    si = StringIO.StringIO()
    cw = csv.writer(si)

    #run_date_created = run.date_created.strftime("%d/%m/%Y")
    run_date_created = datetime.now().strftime("%d/%m/%Y")
    run_description = "Run description TBD"  # run.description
    genome_str = ""  # blank out genome for generate fastq workfow

    cw.writerow(["[Header]"])
    cw.writerow(["IEMFileVersion", "4"])
    cw.writerow(["Investigator Name",
                current_user.first_and_last_name])
    cw.writerow(["Experiment Name", run_id])
    cw.writerow(["Date", run_date_created])
    cw.writerow(["Workflow", "GenerateFASTQ"])  # run.miseq_workflow
    cw.writerow(["Application", "GenerateFASTQ"])  # run.miseq_workflow
    cw.writerow(["Assay", "Nextera XT"])  # run.miseq_assay
    cw.writerow(["Description", strip_forbidden_chars(run_description)])
    cw.writerow(["Chemistry", "Amplicon"])  # run.miseq_chemistry
    cw.writerow([""])
    cw.writerow(["[Reads]"])
    cw.writerow(["151"])  # run.read_1_cycles
    cw.writerow(["151"])  # run.read_2_cycles
    cw.writerow([""])
    cw.writerow(["[Settings]"])
    cw.writerow(["FilterPCRDuplicates", 1])
    cw.writerow(["ReverseComplement", 0])
    cw.writerow(["VariantFilterQualityCutoff", 30])
    cw.writerow(["QualityScoreTrim", 30])
    cw.writerow(["Adapter", "CTGTCTCTTATACACATCT"])
    cw.writerow([""])
    cw.writerow(["[Data]"])

    cw.writerow(['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well',
                 'I7_Index_ID', 'index', 'I5_Index_ID', 'index2',
                 'GenomeFolder', 'Sample_Project', 'Description'])

    for row in rows:
        # make data row
        data = [
            row.sample_id,  # Sample_ID
            row.parent_sample_id,  # Sample_Name
            "",  # Sample_Plate
            row.notes,  # Sample_Well
            row.i7_seq_name,  # I7_Index_ID
            row.i7_seq,  # index
            row.i5_seq_name,  # I5_Index_ID
            row.i5_seq,  # index2
            genome_str,  # GenomeFolder
            "",  # Sample_Project
            strip_forbidden_chars(row.parent_description)  # Description
        ]
        cw.writerow(data)

    csvout = si.getvalue().strip('\r\n')

    return csvout


def miseq_csv_for_nps(db_session, nps_ids):

    n_total = len(nps_ids)
    if n_total == 0:
        err = "No samples -- cannot create miseq file."
        logging.error(err)
        abort(400, message=err)

    n_non_nps = sum([1 for el in nps_ids if el[0:4] != 'NPS_'])
    if n_non_nps != 0:
        err = "%d of %d samples are not NPS_ samples"
        err %= (n_non_nps, n_total)
        logging.error(err)
        abort(400, message=err + ".  Miseq requires all samples to be NPS_.")

    qry = (
        db_session.query(MiSeqSampleView)
        .filter(MiSeqSampleView.sample_id.in_(nps_ids))
        .order_by(MiSeqSampleView.sample_id)
    )
    rows = qry.all()

    if not rows:
        err = "MiSeqSampleView query failed -- cannot create miseq file."
        logging.error(err)
        abort(400, message=err)

    run_id = "MSR_tbd"  # run.run_id
    csvout = miseq_csv_template(rows, run_id)

    logging.info(" %s downloaded the MISEQ REPORT",
                 current_user.first_and_last_name)

    # We need to modify the response, so the first thing we
    # need to do is create a response out of the CSV string
    response = make_response(csvout)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=MiSeq_" + run_id + "_Report.csv"
    return response


def echo_csv_for_nps(operations, fname, transfer_volume=100):
    """ assumes each oper looks like {
            "source_plate_barcode": "NGS_BARCODE_PLATE_TEST1",
            "source_well_name": "A1",
            "source_sample_id":"BCS_00234",
            "source_plate_well_count": 384,
            "destination_plate_barcode":"SRN 000577 SM-37",
            "destination_well_name":"K13",
            "destination_plate_well_count":384
            "destination_sample_id": "NPS_89111c1a0327a61016dc4d017"
        }
    """
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

    csvout = si.getvalue().strip('\r\n')
    logging.info(" %s downloaded an ECHO WORKLIST",
                 current_user.first_and_last_name)

    response = make_response(csvout)
    assert fname[-4:] == '.csv'
    response.headers["Content-Disposition"] = "attachment; filename=%s" % fname
    return response

'''
def create_msr(cur_session, form_params):
    """Lifted from twist_lims/lims_app/util/temp_google.py handle_create_ngs_run """
    ##############
    # make ngs run
    ##############
    # replace with sequence or object id
    print "Replace ngs run max with db sequence or object id"
    max_run = cur_session.query(func.max(tdd.NGSRun.run_id)).one()
    next_run_id = "MSR_%05d" % (int(max_run[0].split("_")[1]) + 1)
    # get max run id (replace)
    instrument_run_number = int(form_params['instrument_run_number'])
    # get max analysis id
    max_analysis = cur_session.query(
        func.max(tdd.NGSSequencingAnalysis.analysis_id)).one()
    next_analysis_id = "NSA_%05d" % (int(max_analysis[0].split("_")[1]) + 1)
    # split adpator sequence from assay
    miseq_adaptor_seq, miseq_assay = form_params['miseq_adapter'].split("_", 1)
    # create ngs run
    ngs_run = tdd.NGSRun(
        next_run_id,
        form_params['run_date'],
        cur_operator.operator_id,
        cur_instrument.instrument_id,
        form_params['cartridge_id'],
        form_params['flowcell_id'],
        # max_run_num + 1,
        instrument_run_number,
        form_params['run_status'],
        # strip nbsp; from copy and paste confluence
        form_params['run_description'].replace(u'\xa0', ' '),
        form_params['run_notes'],
        form_params['miseq_workflow'],
        form_params['miseq_chemistry'],
        form_params['read1_cycles'],
        form_params['read2_cycles'],
        miseq_adaptor_seq,
        miseq_assay,
        form_params['miseq_quality_score_trim'],
        )
    ngs_run.instrument = cur_instrument
    # need to store miseq kit lots (associate RTS)
    cur_session.add(ngs_run)


def create_nrsj(cur_session, ngs_run, ngs_prepped_samples):
    """Adapted from twist_lims/temp_google.py handle_create_ngs_run line 2977"""
    for ix, ngs_prepped_sample in enumerate(ngs_prepped_samples):
        sample_num_on_run = ix + 1
        # now create sample join (redundant info with plate layout -- refactor)
        nrsj = NGSRunSampleJoin(
            ngs_run.run_id,
            ngs_prepped_sample.sample_id,
            sample_num_on_run,
            "-%s" % sample_num_on_run,  # dummy value
            "-1",  # rec['plate_column_id']
        )
        nrsj.ngs_run = ngs_run
        nrsj.sample = ngs_prepped_sample
        # add to db
        cur_session.add(nrsj)
'''



