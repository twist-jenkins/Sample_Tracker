
#
# Authentication route handlers.
#
from authentication import login, user_missing_from_operator_table, oauth2callback, logout

#
# Route handlers for the pages of the application.
#
from pages import home, sample_transfers_page, edit_sample_plate, sample_report_page, plate_report_page

#
# The REST API used by the web pages.
#
from api import ( dragndrop, get_sample_plate, sample_plate_external_barcode, sample_report, plate_report, 
    create_sample_movement, get_sample_plates_list, get_sample_plate_barcodes_list, get_samples_list )



################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
######## ANGULAR
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

# Route handlers for the pages of the application.
#
from angular import ( new_home, user_data, google_login, sample_transfer_types, sample_plate_barcodes, update_plate_barcode, 
                      sample_transfers, create_step_record, plate_details, source_plate_well_data, check_plates_are_new )

from .transfer import preview, save, execute
