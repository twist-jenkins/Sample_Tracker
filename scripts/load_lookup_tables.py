from flask.ext.script import Command
import sys, os
import csv
#import unicodecsv
import unicodecsv, StringIO, cStringIO
import codecs, cStringIO
from app import db
#from app import (BlogPostSectionType, UserSegment, CalendarEventType, NewsArticleType, MediaType, PublicationType)
from sqlalchemy import or_, and_

from app.dbmodels import SampleTransferType




class LoadLookupTables(Command):

    def truncate_lookup_tables(self):
        """
        db.session.query(BlogPostSectionType).delete()
        db.session.query(UserSegment).delete()
        db.session.query(CalendarEventType).delete()
        db.session.query(NewsArticleType).delete()
        db.session.query(MediaType).delete()
        db.session.query(PublicationType).delete()
        """
        db.session.query(SampleTransferType).delete()

    def load_sample_transfer_type_table(self):
        for row_data in [
            "Add PCR Master Mix", "Transfer Aliquot", "Move Specimen"
        ]:
            row = SampleTransferType(row_data)
            db.session.add(row)

        db.session.commit()


    """

    def load_block_post_section_type_table(self):

        for row_data in [
            "text_only", "text_and_image", "image_only", "pullquote"
        ]:
            row = BlogPostSectionType(row_data)
            db.session.add(row)

        db.session.commit()


    def load_user_segment_table(self):

        for row_data in [
            "segmentA", "segmentB"
        ]:
            row = UserSegment(row_data)
            db.session.add(row)

        db.session.commit()


    def load_calendar_event_type_table(self):

        for row_data in [
            "conference", "presentation", "hiring event"
        ]:
            row = CalendarEventType(row_data)
            db.session.add(row)

        db.session.commit()


    def load_news_article_type_table(self):

        for row_data in [
            "pr", "news", "journal article", "interview"
        ]:
            row = NewsArticleType(row_data)
            db.session.add(row)

        db.session.commit()



    def load_media_type_table(self):

        for row_data in [
            "newspaper", "magazine", "webpage", "audio", "video", "tweet"
        ]:
            row = MediaType(row_data)
            db.session.add(row)

        db.session.commit()




    def load_publication_type_table(self):

        for row_data in [
            "newspaper", "magazine", "website", "book", "radio", "podcast", "television"
        ]:
            row = PublicationType(row_data)
            db.session.add(row)

        db.session.commit()
    """



    def run(self):
        
        print "Reloading the lookup tables..."

        self.truncate_lookup_tables()

        self.load_sample_transfer_type_table()

        """

        self.truncate_lookup_tables()

        self.load_block_post_section_type_table()

        self.load_calendar_event_type_table()

        self.load_news_article_type_table()

        self.load_media_type_table()

        self.load_publication_type_table()
        """

