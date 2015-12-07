from flask.ext.script import Command, Manager, Option
import sys, os
import csv
#import unicodecsv
import unicodecsv, StringIO, cStringIO
import codecs, cStringIO
from app import db
#from app import (BlogPostSectionType, UserSegment, CalendarEventType, NewsArticleType, MediaType, PublicationType)
from sqlalchemy import or_, and_

from twistdb.sampletrack import (SampleTransferTemplate, SampleTransferTemplateDetails)

import collections

import time

import csv

"""
source, plate, number, of, wells,source, well, id,source, plate, number,destination, plate, number, of, wells,destination, well, id,destination, plate, number
384,1,1,96,1,1
,2,1,,2,1
,3,1,,3,1
,4,1,,1,2
,1,2,,2,2
,2,2,,3,2
,3,2,,1,3
,4,2,,2,3
,5,2,,3,3

template = {
    "template_name":"Test Template",
    "details":{
        
    }
}

source, plate, number, of, wells,source, well, id,source, plate, number,destination, plate, number, of, wells,destination, well, id,destination, plate, number
384,1,1,96,1,1

"""

class ImportSampleTransferTemplate(Command):

    option_list = (
        Option('--file_name', '-f', dest='file_name'),
        Option('--sample_transfer_template_name', '-n', dest='sample_transfer_template_name'),
    )

    def run(self,file_name,sample_transfer_template_name):

        print "file_name: ", file_name
        print "sample_transfer_template_name: ", sample_transfer_template_name

        path_and_file = "./starting_configuration_data/" + file_name

        print "Exists? ", os.path.exists(path_and_file)

        read_header = False
        read_plate_sizes = False
        from_plate_size = None
        destination_plate_size = None


        template_details = []
        template = {
            "template_name":sample_transfer_template_name,
            "from_plate_size":0,
            "destination_plate_size":0,
            "details":template_details
        }

        with open(path_and_file, 'rU') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                row = row[0].split(",")
                if read_header:
                    if not read_plate_sizes:
                        template["from_plate_size"] = row[0]
                        template["destination_plate_size"] = row[3]
                        read_plate_sizes = True

                    template_details.append({
                        "source_well_id":row[1],
                        "source_plate_number":row[2],
                        "destination_well_id":row[4],
                        "destination_plate_number":row[5]
                    })


                else:
                    read_header = True
                


        export_path_and_filename = "./app/database_data/template" + str(time.strftime("%m_%d_%Y_%H_%M_%S%p")) + ".py"

        with open(export_path_and_filename,"wa") as f:
            f.write("template = " + repr(template))

        print "done?"






         
