"""Hamilton worklist generation."""

from twistdb.sampletrack import Plate

INITIAL_VOL = 25  # ul
FINAL_DNA_CONC = 15  # ng/ul

MAX_TRANSFER_VOL = 50  # ul per Leslie
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

    # FIXME we need to get the most *recent* sample rows; assuming here only 1 set
    for sample in plate.samples:
        row = sample.well.well_label + ","

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
