import csv
import StringIO
import logging
import json
from datetime import datetime

from app import db

from flask import make_response
from flask.ext.restful import abort
from flask_login import current_user

from dbmodels import MiSeqSampleView
from twistdb.sampletrack import Sample
from twistdb.ngs import NGSBarcodePair
from twistdb import create_unique_id

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

    for ix, row in enumerate(rows):
        # make data row
        data = [
            "%s.%d" % (row.sample_id, ix + 1),  # Sample_ID.rownum
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


def sample_map_template(rows):

    sio = StringIO.StringIO()
    book = twist_excel.workbook.TwistExcelWorkbook(sio)

    book.format.gray.set_align('center')
    book.format.gray.set_align('vcenter')
    book.format.gray.set_text_wrap()
    book.format.gray.set_bold()

    book.fields = (
        book.Field("sample_num_on_run", 20, book.format.gray,
                   "Sample Number On Run (For FASTQ Naming)"),
        book.Field("sample_id", 10, book.format.gray,
                   "Sample ID"),
        book.Field("i5_sequence_id", 15, book.format.gray,
                   "I5 Barcode Sequence ID (From Barcode Sequence table)"),
        book.Field("i7_sequence_id", 15, book.format.gray,
                   "I7 Barcode Sequence ID (From Barcode Sequence table)"),
        book.Field("description", 60, book.format.gray,
                   "Expected result description, notes about why on run, "
                   "prep-related notes, which samples are controls, etc"),
        book.Field("var_prep_type", 15, book.format.lime,
                   "Variable: Prep"),
        book.Field("var_parent_type ", 10, book.format.lime,
                   "Variable: Parent type"),
        book.Field("var_flag", 5, book.format.lime,
                   "Variable: Flag"),
    )

    sheet = book.workbook.add_worksheet("NGS Run Map")
    sheet.write('A1', ':table')
    sheet.write('B1', "sample_map")
    sheet.write('A3', 'Maps each sample on run to barcodes and one or more '
                'variables under study. You can add as many categories '
                '(columns) as you like, just match the var_xxx format '
                'in row 6 (row 5 is ignored). Variables that do not start '
                'with "var_" are ignored in row 6 -- do not use spaces.')
    sheet.set_row(4, 72)
    book.write_to(sheet, book.fields)

    row_format = book.format.regular
    for row_ix, row in enumerate(rows):
        position = book.cell_position(row_ix)
        col_vals = [
            row_ix + 1,
            row.parent_sample_id,  # CS_00233
            row.i5_sequence_id,
            row.i7_sequence_id,
            strip_forbidden_chars(row.parent_description),
            "Automated",
            "Colony"
        ]
        sheet.write_row(position, col_vals, row_format)

    return sio


def nps_id_details(db_session, nps_ids):
    """Raises error if some sample is not NPS_"""

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

    return rows


def miseq_csv_response(nps_detail_rows, fname=None):
    """MiSeq CSV"""
    run_id = "MSR_tbd"  # run.run_id
    csvout = miseq_csv_template(nps_detail_rows, run_id)
    logging.info(" %s downloaded the MISEQ REPORT",
                 current_user.first_and_last_name)
    response = make_response(csvout)
    if fname is None:
        datestr = datetime.now().strftime("%Y-%m-%d_%H%M")
        fname = "ngs_miseq_%s.csv" % datestr
    response.headers["Content-Disposition"] = "attachment; filename=%s" % fname
    return response


def sample_map_response(nps_detail_rows, fname=None):
    """Sample Map XLSX"""
    xlsx_out = sample_map_template(nps_detail_rows)
    logging.info(" %s downloaded the SAMPLE MAP REPORT",
                 current_user.first_and_last_name)
    xlsx_out.seek(0)
    mimt = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = make_response(xlsx_out.read())
    response.mimetype = mimt
    if fname is None:
        datestr = datetime.now().strftime("%Y-%m-%d_%H%M")
        fname = "ngs_sample_map_%s.xlsx" % datestr
    response.headers["Content-Disposition"] = "attachment; filename=%s" % fname
    return response


def echo_csv_for_nps(operations, fname=None, transfer_volume=200):
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

    if fname is None:
        datestr = datetime.now().strftime("%Y-%m-%d_%H%M")
        fname = "ngs_barcoding_%s.echo.csv" % datestr

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


def make_ngs_prepped_sample(db_session, source_sample_id,
                            destination_well_id):
    # Grab next pair of barcodes
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

    # Create NPS
    nps_id = create_unique_id("NPS_")()
    description = 'SMT - well %s' % destination_well_id  # TODO: add plate
    nps_sample = Sample(id=nps_id,
                        parent_sample_id=source_sample_id,
                        name=nps_id,
                        description=description,
                        i5_sequence_id=ngs_pair.i5_sequence_id,
                        i7_sequence_id=ngs_pair.i7_sequence_id,
                        operator_id=current_user.operator_id)

    logging.debug('NPS_ID %s for %s assigned [%s, %s]',
                  nps_id, source_sample_id,
                  ngs_pair.i5_sequence_id,
                  ngs_pair.i7_sequence_id)

    db_session.add(nps_sample)
    db_session.flush()

    return nps_id, ngs_pair
