import logging

from app.dbmodels import SamplePlate
from app.dbmodels import create_unique_object_id


def check_destination_plate(db_session, barcode):
    """Is there already a plate in the database with the barcode being specified?
    # If so, that is an error!"""
    destination_plate = db_session.query(SamplePlate).filter_by(external_barcode=barcode).first()

    if destination_plate:
        logging.error("Encountered error creating sample transfer. "
                      "A plate with the barcode: [%s] already exists",
                      barcode)
        errorMessage = "A plate with the destination plate barcode: [%s] already exists" % (barcode)
        raise IndexError(errorMessage)


def create_destination_plate(db_session, operator, destination_barcode,
                             source_plate_type_id, storage_location_id):
    """creates a destination plate for a transfer"""

    check_destination_plate(db_session, destination_barcode)
    destination_plate_name = create_unique_object_id("PLATE_")
    destination_plate_description = create_unique_object_id("PLATEDESC_")
    plate = SamplePlate(source_plate_type_id,
                        operator.operator_id,
                        storage_location_id,
                        destination_plate_name,
                        destination_plate_description,
                        destination_barcode)
    db_session.add(plate)
    return plate
