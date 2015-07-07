
#
# Authentication route handlers.
#
from authentication import login, oauth2callback, logout

#
# Route handlers for the pages of the application.
#
from pages import home, dragndrop, edit_sample_plate, sample_report_page, plate_report_page

#
# The REST API used by the web pages.
#
from api import ( get_sample_plate, sample_plate_external_barcode, sample_report, plate_report, 
    create_sample_movement, get_sample_plates_list, get_sample_plate_barcodes_list, get_samples_list )
