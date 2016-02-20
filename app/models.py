import logging

from twistdb.sampletrack import Plate
from twistdb import create_unique_id


def check_destination_plate(db_session, barcode, transform_template_id):
    """Is there already a plate in the database with the barcode being specified?
    # If so, that is an error!"""
    destination_plate = db_session.query(Plate).filter_by(external_barcode=barcode).first()

    if destination_plate and transform_template_id != 2:
        logging.error("Encountered error creating sample transform. "
                      "A plate with the barcode: [%s] already exists",
                      barcode)
        errorMessage = "A plate with the destination plate barcode: [%s] already exists" % (barcode)
        raise IndexError(errorMessage)


def create_destination_plate(db_session, operator, destination_barcode,
                             source_plate_type_id, storage_location, transform_template_id):
    """creates a destination plate for a transform"""

    # TODO: use a proper barcode, not a bson objectid

    check_destination_plate(db_session, destination_barcode, transform_template_id)

    destination_plate_id = create_unique_id("PLATE_")()
    destination_plate_name = "smt placeholder name"
    destination_plate_description = "smt placeholder descr"
    plate = Plate(id=destination_plate_id,
                  type_id=source_plate_type_id,
                  operator_id=operator.operator_id,
                  storage_location=storage_location,
                  name=destination_plate_name,
                  description=destination_plate_description,
                  external_barcode=destination_barcode)

    db_session.add(plate)
    return plate
