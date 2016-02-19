"""Hamilton worklist generation."""

from twistdb.sampletrack import Plate

INITIAL_VOL = 27  # ul, assuming pre-frag analysis
FINAL_DNA_CONC = 15  # ng/ul

MAX_TRANSFER_VOL = 48  # ul per Leslie, 50-2 since initial vol increased by 2 to 27
VOL_FORMAT = "{0:.2f}"

WORKLIST_HEADERS = "Well ID,Volume\n"


def post_pca_normalization_worklist(db, plate_id):
    """Generate bulk water to well_id for dilution post-PCA product."""

    worklist = WORKLIST_HEADERS + plate_id + ",\n"
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
    row_skip_order = range(1, plate.layout.row_count) * 2

    for curr_col in xrange(plate.layout.col_count):
        for curr_row in row_skip_order[::2]:  # skip a column each time
            wlabel = chr(curr_row - 1 + ord('A')) + str(curr_col)
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
