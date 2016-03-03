from twistdb.sampletrack import Plate, Sample
from app.routes.transform import WebError

MISEQ_READ_1_CYCLES = 151
MISEQ_READ_2_CYCLES = 151
MISEQ_ADAPTOR_SEQUENCE = "CTGTCTCTTATACACATCT"

def preview_ngs_load(session, request):
    rows, cmds = [{}], []
    # TO DO   based on source barcode, present the target sequencer

    details = request.json['details']

    # DEV Only remove when code exists to set sequencer
    sequencer = "MiSeq";

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
         }},
        {"type": "REQUEST_DATA",
         "item": {
             "type": "barcode.CARTRIDGE",
             "title": "Input Cartridge Barcode",
             "forProperty": "inputCartridgeBarcode",
             # "value": reqData["inputCartridgeBarcode"]
         }},
        {"type": "REQUEST_DATA",
         "item": {
             "type": "barcode.FLOWCELL",
             "title": "Flowcell Barcode",
             "forProperty": "flowCellBarcode",
             # "value": reqData["flowCellBarcode"]
         }}, ])
    return rows, cmds


def store_ngs_run(sess, request):

    print "@" * 500

    # parse metadata
    assert "requestedData" in request.details
    data = request.details["requestedData"]
    sequencer_bc = data["sequencerBarcode"]
    input_cartridge_bc = data["inputCartridgeBarcode"]
    flowcell_bc = data["flowCellBarcode"]
    for barcode in (sequencer_bc, input_cartridge_bc, flowcell_bc):
        assert barcode is not None

    # parse sample
    sources = request.details["sources"]
    assert len(sources) == 1
    assert "details" in sources[0]
    source_plate_bc = sources[0]["details"]["id"]
    assert source_plate_bc is not None
    msr_platetube = (sess.query(Plate)
                     .filter_by(external_barcode=source_plate_bc)
                     ).one()
    msr_samples = msr_platetube.current_well_contents(sess)
    assert len(msr_samples) == 1
    msr_sample = msr_samples[0]

    # create msr
    create_msr(sess, msr_sample, input_cartridge_bc, flowcell_bc,
               sequencer_bc)


def create_msr(cur_session, msr_sample, cartridge_id='car_tbd',
               flowcell_id='fc_tbd', instrument_stub='inr_tbd'
               instrument_run_number='irn_tbd', instrument_pk=1):
    """Adapted from twist_lims/lims_app/util/temp_google.py handle_create_ngs_run """
    ##############
    # make ngs run
    ##############

    # replace with sequence or object id
    print "Replace ngs run max with db sequence or object id"
    max_run = cur_session.query(func.max(NGSRun.id)).one()
    next_run_id = "MSR_%05d" % (int(max_run[0].split("_")[1]) + 1)

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
    ngs_run.id = next_run_id
    ngs_run.sample_id = msr_sample.id
    ngs_run.cartridge_id = cartridge_id
    ngs_run.instrument_run_number = instrument_run_number
    ngs_run.instrument_pk = instrument_pk
    ngs_run.read_1_cycles = MISEQ_READ_1_CYCLES
    ngs_run.read_2_cycles = MISEQ_READ_2_CYCLES
    ngs_run.miseq_adaptor = MISEQ_ADAPTOR_SEQUENCE

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

