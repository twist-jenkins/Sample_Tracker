from flask.ext.script import Command, Manager, Option
import sys, os
import csv
#import unicodecsv
import unicodecsv, StringIO, cStringIO
import codecs, cStringIO
from app import db
#from app import (BlogPostSectionType, UserSegment, CalendarEventType, NewsArticleType, MediaType, PublicationType)
from sqlalchemy import or_, and_

from app.dbmodels import (SamplePlate, SamplePlateLayout, SampleTransfer, SampleTransferDetail)

import collections

SamplePlateLayoutKey = collections.namedtuple('SamplePlateLayoutKey', 'sample_plate_id well_id sample_id')

class DeleteSampleTransfer(Command):

    option_list = (
        Option('--sample_transfer_id', '-id', dest='sample_transfer_id'),
    )

    def run(self, sample_transfer_id ):
        print "delete the sample transfer with this id: ", sample_transfer_id

        sample_plate_keys = []
        sample_plate_layout_row_keys = []


        #
        # 1. Collect the sample plate layout keys and the sample plate keys.
        #
        sample_plate_layout_rows = db.session.query(SampleTransferDetail).filter(
            SampleTransferDetail.sample_transfer_id == sample_transfer_id).all()

        for row in sample_plate_layout_rows:
            key = SamplePlateLayoutKey(sample_plate_id=row.destination_sample_plate_id,
                well_id=row.destination_well_id,sample_id=row.destination_sample_id)
            sample_plate_layout_row_keys.append(key)
            if row.destination_sample_plate_id not in sample_plate_keys:
                sample_plate_keys.append(row.destination_sample_plate_id)


        rows = db.session.query(SampleTransferDetail).filter(
            SampleTransferDetail.sample_transfer_id == sample_transfer_id).all()
        #for row in rows:
        #    print "SampleTransferDetail ROW: ", row 

        #
        # 2. Delete sample transfer detail rows.
        #
        db.session.query(SampleTransferDetail).filter(
            SampleTransferDetail.sample_transfer_id == sample_transfer_id).delete()
        db.session.commit()

        #
        # 2. Delete the sample transfer row.
        #
        db.session.query(SampleTransfer).filter_by(id=sample_transfer_id).delete()

        #
        # 3. Delete all the "sample plate layout" rows that the sample transfer details pointed to.
        #
        for key in sample_plate_layout_row_keys:
            db.session.query(SamplePlateLayout).filter(and_(
                SamplePlateLayout.sample_plate_id==key.sample_plate_id,
                SamplePlateLayout.well_id==key.well_id,
                SamplePlateLayout.sample_id==key.sample_id
                )).delete()

        #
        # 4. Delete the "destination" sample plates that were part of the transfer.
        #
        for key in sample_plate_keys:
            db.session.query(SamplePlate).filter_by(sample_plate_id=key).delete()

        db.session.commit()

        print "OK, it has been deleted!"

