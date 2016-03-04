import StringIO
import csv
from datetime import datetime
import logging

from flask import make_response
from flask_login import current_user
import Bio.Seq
from sqlalchemy.sql import func

from twistdb.sampletrack import Plate, Sample
from twistdb.ngs import NGSRun
from app.routes.transform import WebError

MISEQ_READ_1_CYCLES = 151
MISEQ_READ_2_CYCLES = 151
MISEQ_ADAPTOR_SEQUENCE = "CTGTCTCTTATACACATCT"

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


# def sample_map_template(rows):
#
#     sio = StringIO.StringIO()
#     book = twist_excel.workbook.TwistExcelWorkbook(sio)
#
#     book.format.gray.set_align('center')
#     book.format.gray.set_align('vcenter')
#     book.format.gray.set_text_wrap()
#     book.format.gray.set_bold()
#
#     book.fields = (
#         book.Field("sample_num_on_run", 20, book.format.gray,
#                    "Sample Number On Run (For FASTQ Naming)"),
#         book.Field("sample_id", 10, book.format.gray,
#                    "Sample ID"),
#         book.Field("i5_sequence_id", 15, book.format.gray,
#                    "I5 Barcode Sequence ID (From Barcode Sequence table)"),
#         book.Field("i7_sequence_id", 15, book.format.gray,
#                    "I7 Barcode Sequence ID (From Barcode Sequence table)"),
#         book.Field("description", 60, book.format.gray,
#                    "Expected result description, notes about why on run, "
#                    "prep-related notes, which samples are controls, etc"),
#         book.Field("var_prep_type", 15, book.format.lime,
#                    "Variable: Prep"),
#         book.Field("var_parent_type ", 10, book.format.lime,
#                    "Variable: Parent type"),
#         book.Field("var_flag", 5, book.format.lime,
#                    "Variable: Flag"),
#     )
#
#     sheet = book.workbook.add_worksheet("NGS Run Map")
#     sheet.write('A1', ':table')
#     sheet.write('B1', "sample_map")
#     sheet.write('A3', 'Maps each sample on run to barcodes and one or more '
#                 'variables under study. You can add as many categories '
#                 '(columns) as you like, just match the var_xxx format '
#                 'in row 6 (row 5 is ignored). Variables that do not start '
#                 'with "var_" are ignored in row 6 -- do not use spaces.')
#     sheet.set_row(4, 72)
#     book.write_to(sheet, book.fields)
#
#     row_format = book.format.regular
#     for row_ix, row in enumerate(rows):
#         position = book.cell_position(row_ix)
#         col_vals = [
#             row_ix + 1,
#             row.parent_sample_id,  # CS_00233
#             row.i5_sequence_id,
#             row.i7_sequence_id,
#             strip_forbidden_chars(row.parent_description),
#             "Automated",
#             "Colony"
#         ]
#         sheet.write_row(position, col_vals, row_format)
#
#     return sio


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


# def sample_map_response(nps_detail_rows, fname=None):
#     """Sample Map XLSX"""
#     xlsx_out = sample_map_template(nps_detail_rows)
#     logging.info(" %s downloaded the SAMPLE MAP REPORT",
#                  current_user.first_and_last_name)
#     xlsx_out.seek(0)
#     mimt = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     response = make_response(xlsx_out.read())
#     response.mimetype = mimt
#     if fname is None:
#         datestr = datetime.now().strftime("%Y-%m-%d_%H%M")
#         fname = "ngs_sample_map_%s.xlsx" % datestr
#     response.headers["Content-Disposition"] = "attachment; filename=%s" % fname
#     return response


def preview_ngs_load(session, request):
    rows, cmds = [{}], []
    # TO DO   based on source barcode, present the target sequencer

    details = request.json['details']

    # DEV Only remove when code exists to set sequencer
    sequencer = "MiSeq"

    cmds.append({
        "type": "PRESENT_DATA",
        "item": {
            "type": "text",
            "title": "Target Sequencer",
            "data": "<strong>" + sequencer + "</strong>"
        }
    })

    reqData = {
        "sequencerBarcode": None,
        "inputCartridgeBarcode": None,
        "flowCellBarcode": None
    }

    if "requestedData" in details:
        data = details["requestedData"]
        if "sequencerBarcode" in data:
            reqData["sequencerBarcode"] = data["sequencerBarcode"]
        if "inputCartridgeBarcode" in data:
            reqData["inputCartridgeBarcode"] = data["inputCartridgeBarcode"]
        if "flowCellBarcode" in data:
            reqData["flowCellBarcode"] = data["flowCellBarcode"]

    cmds.extend([
        {"type": "REQUEST_DATA",
         "item": {'type': "barcode.INSTRUMENT",
                  "title": "Sequencer Barcode",
                  "forProperty": "sequencerBarcode",
                  # "value": reqData["sequencerBarcode"]
                  }
         },
        {"type": "REQUEST_DATA",
         "item": {"type": "barcode.CARTRIDGE",
                  "title": "Input Cartridge Barcode",
                  "forProperty": "inputCartridgeBarcode",
                  # "value": reqData["inputCartridgeBarcode"]
                  }
         },
        {"type": "REQUEST_DATA",
         "item": {"type": "barcode.FLOWCELL",
                  "title": "Flowcell Barcode",
                  "forProperty": "flowCellBarcode",
                  # "value": reqData["flowCellBarcode"]
                  }
         },
    ])
    return rows, cmds


def store_ngs_run(sess, spec):

    print "@" * 500
    import pprint
    pprint.pprint(spec.data_json)
    # parse metadata
    details = spec.data_json['details']
    assert "requestedData" in details
    data = details["requestedData"]
    sequencer_bc = data["sequencerBarcode"]
    input_cartridge_bc = data["inputCartridgeBarcode"]
    flowcell_bc = data["flowCellBarcode"]
    for barcode in (sequencer_bc, input_cartridge_bc, flowcell_bc):
        assert barcode is not None

    # parse sample
    sources = spec.data_json["sources"]
    assert len(sources) == 1
    assert "details" in sources[0]
    source_plate_bc = sources[0]["details"]["id"]
    assert source_plate_bc is not None
    msr_platetube = (sess.query(Plate)
                     .filter_by(external_barcode=source_plate_bc)
                     ).one()
    msr_samples = msr_platetube.current_well_contents(sess)
    lms = len(msr_samples)
    if lms != 1:
        return "Incorrect number of source samples: [%s], expected 1" % lms
    msr_sample = msr_samples[0]

    # create msr
    create_msr(sess, msr_sample, input_cartridge_bc, flowcell_bc,
               sequencer_bc)

    return False


def create_msr(cur_session, msr_sample, cartridge_id,
               flowcell_id, instrument_stub):
    """Adapted from twist_lims/lims_app/util/temp_google.py handle_create_ngs_run """
    ##############
    # make ngs run
    ##############

    # replace with sequence or object id
    print "Replace ngs run max with db sequence or object id"
    max_run = cur_session.query(func.max(NGSRun.pk)).one()
    next_run_id = max_run[0] + 1

    # get max run id (replace)
    # instrument_run_number = int(form_params['instrument_run_number'])
    # get max analysis id
    '''
    max_analysis = cur_session.query(
        func.max(tdd.NGSSequencingAnalysis.analysis_id)).one()
    next_analysis_id = "NSA_%05d" % (int(max_analysis[0].split("_")[1]) + 1)
    '''

    # split adpator sequence from assay
    # miseq_adaptor_seq, miseq_assay = form_params['miseq_adapter'].split("_", 1)

    # create ngs run
    ngs_run = NGSRun()
    ngs_run.pk = next_run_id
    ngs_run.sample_id = msr_sample.id
    ngs_run.cartridge_id = cartridge_id
    ngs_run.flowcell_id = flowcell_id
    ngs_run.instrument_run_number = '1234' # instrument_run_number
    ngs_run.instrument_pk = '1' # instrument_pk
    ngs_run.read_1_cycles = MISEQ_READ_1_CYCLES
    ngs_run.read_2_cycles = MISEQ_READ_2_CYCLES
    ngs_run.miseq_adapter = MISEQ_ADAPTOR_SEQUENCE

    cur_session.add(ngs_run)

'''
def create_nrsj(cur_session, ngs_run, ngs_prepped_samples):
    """Adapted from twist_lims/temp_google.py handle_create_ngs_run line 2977"""
    for ix, ngs_prepped_sample in enumerate(ngs_prepped_samples):
        sample_num_on_run = ix + 1
        # now create sample join (redundant info with plate layout -- refactor)
        nrsj = NGSRunSampleJoin(
            ngs_run.run_id,
            ngs_prepped_sample.id,
            sample_num_on_run,
            "-%s" % sample_num_on_run,  # dummy value
            "-1",  # rec['plate_column_id']
        )
        nrsj.ngs_run = ngs_run
        nrsj.sample = ngs_prepped_sample
        # add to db
        cur_session.add(nrsj)
'''


def miseq_csv_template(samples, run_id, i7_rc=True):

    si = StringIO.StringIO()
    cw = csv.writer(si)

    #run_date_created = run.date_created.strftime("%d/%m/%Y")
    run_date_created = datetime.now().strftime("%d/%m/%Y")
    run_description = "Run description TBD -- NOTE i7 barcode sequence is RC as of 1-29-2016 1438"

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
    cw.writerow([str(MISEQ_READ_1_CYCLES)])
    cw.writerow([str(MISEQ_READ_2_CYCLES)])
    cw.writerow([""])
    cw.writerow(["[Settings]"])
    cw.writerow(["FilterPCRDuplicates", 1])
    cw.writerow(["ReverseComplement", 0])
    cw.writerow(["VariantFilterQualityCutoff", 30])
    cw.writerow(["QualityScoreTrim", 30])
    cw.writerow(["Adapter", MISEQ_ADAPTOR_SEQUENCE])
    cw.writerow([""])
    cw.writerow(["[Data]"])

    cw.writerow(['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well',
                 'I7_Index_ID', 'index', 'I5_Index_ID', 'index2',
                 'GenomeFolder', 'Sample_Project', 'Description'])

    for ix, sample in enumerate(samples):
        # make data row
        i7_seq = sample.i7_barcode.sequence
        if i7_rc:
            i7_seq = Bio.Seq.Seq(i7_seq).reverse_complement()
        data = [
            "%s.%d" % (sample.id, ix + 1),  # Sample_ID.rownum
            sample.order_item_id,  # Sample_Name
            sample.plate.external_barcode,  # Sample_Plate
            sample.plate_well_code,  # Sample_Well
            sample.i7_sequence_id,  # I7_Index_ID
            i7_seq,  # index1
            sample.i5_sequence_id,  # I5_Index_ID
            sample.i5_barcode.sequence,  # index2
            genome_str,  # GenomeFolder
            sample.work_order_id,  # Sample_Project
            strip_forbidden_chars("Parent Sample " + ", ".join([p.id for p in sample.parents]))  # Description
        ]
        cw.writerow(data)

    csvout = si.getvalue().strip('\r\n')

    return csvout

