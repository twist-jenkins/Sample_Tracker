"""Hamilton worklist generation."""

from twistdb.sampletrack import Plate, PlateWell

INITIAL_VOL = 27  # uL, assuming pre-frag analysis
FINAL_DNA_CONC = 15  # ng/uL

MAX_TRANSFER_VOL = 48  # uL per Leslie, 50-2 since initial vol increased by 2 to 27
VOL_FORMAT = "{0:.2f}"

WORKLIST_HEADERS_POST_PCA = "Well ID,Volume\n"

MIN_PLATES = 1
MAX_PLATES = 25
MAX_PLATE_ROWS = 8
MAX_PLATE_WELLS = 95
CARRIER_MAX_PLATES = 5
PLATE_LETTERS = list('ABCDEFGH')

def yield_dest_well(plate_count):
    """Generator function which yields the next destination well given the total number of plates (e.g. for plate, well in yield_dest_well(3): ...)"""
    row = col = plate = 1
    letter = 0

    for i in xrange(plate_count * MAX_PLATE_WELLS):
        if i != 1 and i % MAX_PLATE_WELLS == 1:
            plate += 1
            row = col = 1
        elif i != 0 and i % MAX_PLATE_ROWS == 0:
            row = 1
            col += 1
        if row == 1:
            letter = 0

        well = '%s%s' % (PLATE_LETTERS[letter], col)
        yield {'plate': plate, 'well': well}

        letter += 1
        row += 1
    yield None

def post_pca_normalization_worklist(db, plate_id):
    """Generate bulk water to well_id for dilution post-PCA product."""

    worklist = WORKLIST_HEADERS_POST_PCA + plate_id + ",\n"
    try:
        plate = db.query(Plate).filter(Plate.external_barcode == plate_id).one()
    except:
        return {
            "success": False,
            "errorMessage": "Couldn't find plate %s" % plate_id
        }

    sdict = {}
    for sample in plate.current_well_contents(db):
        sdict[sample.well.well_label] = sample

    # The Hamilton transfers liquid most efficiently by column. Also, the spacing
    # is such that in a 384-well plate, the head has to skip a column each time
    # and then come back for the first column. See MES-1056 for details.

    # We double the 1:N row count so that later we can move through by
    # 2s so that we wrap back around to the even rows.
    row_skip_order = range(1, plate.plate_type.layout.row_count + 1) + \
        range(2, plate.plate_type.layout.row_count + 1)

    for curr_col in xrange(plate.plate_type.layout.col_count):
        for curr_row in row_skip_order[::2]:  # skip a column each time
            wlabel = chr(curr_row - 1 + ord('A')) + str(curr_col + 1)
            sample = sdict[wlabel]

            row = sample.well.well_label + ","

            if not sample.conc_ng_ul:
                return {
                    "success": False,
                    "errorMessage": "Sample %s has no concentration data!" % sample.id
                }

            # Convert the concentration data to a normalization volume
            # using the formula on:
            # https://twistbioscience.atlassian.net/wiki/display/IN/Plate+Reader+-++Requirements+for+integration+with+Sample+Tracker?focusedCommentId=69534577#PlateReader-RequirementsforintegrationwithSampleTracker-Calculation
            norm_vol = ((sample.conc_ng_ul * float(INITIAL_VOL)) /
                        float(FINAL_DNA_CONC)) - INITIAL_VOL

            # Limit the total amount of liquid we transfer for normalization
            if norm_vol > MAX_TRANSFER_VOL:
                norm_vol = MAX_TRANSFER_VOL
            elif norm_vol < 0:
                norm_vol = 0

            row += VOL_FORMAT.format(norm_vol) + "\n"
            worklist += row

    return worklist

def miniprep_hitpicking(db, transform_spec):
    """Generate worklist for Hitpicking for Miniprep given a transform_spec object"""

    json = transform_spec.data_json
    samples = {}
    worklist = []

    assert 'sources' in json
    assert 'destinations' in json
    assert len(json['sources']) > 0
    assert len(json['destinations']) > 0

    # get best clones from each plate and compile an easily sortable sample dict
    for src in json['sources']:
        plate_id = src['details']['id']
        wells = db.query(Plate).get(plate_id).current_well_contents(db)
        for sample in wells:
            if sample.passed_ngs and sample.is_best_clone:
                pos = src['details']['position']
                plate_index = ((int(pos[1]) - 1) * CARRIER_MAX_PLATES) + abs(CARRIER_MAX_PLATES - int(pos[3])) # calculate an easily sortable plate index from C#P#
                key = "%02d-%s_%s" % (plate_index, sample.well.well_label[::-1], pos) # concat an easily sortable well index and append original location after _
                samples[key] = sample

    # compile worklist
    order = sorted(samples)
    yield_well = yield_dest_well(len(json['destinations']))
    for key in order:
        dest = yield_well.next()
        src_plate = ((int(key[-3]) - 1) * CARRIER_MAX_PLATES) + int(key[-1])
        worklist.append({
            "SrcWell_Num": samples[key].well.col,
            "Src_Plate": src_plate,
            "SrcWell": samples[key].well.well_label,
            "DestPlate": dest['plate'],
            "DestWell": dest['well']
        })

    # generate worklist CSV
    csv = '"SrcWell_Num","Src_Plate","SrcWell","DestPlate","DestWell"\n'
    for r in worklist:
        csv += '"%s","%s","%s","%s","%s"\n' % (
            r["SrcWell_Num"], r["Src_Plate"], r["SrcWell"], r["DestPlate"], r["DestWell"]
        )

    return csv
