
import os, sys

import time

import hashlib 

import random

import xlrd

import collections

import json

from flask import Flask, render_template, request, Response, redirect, url_for, abort, session, send_from_directory, jsonify

from flask_assets import Environment

from functools import wraps

from webassets.loaders import PythonLoader as PythonAssetsLoader

from werkzeug import secure_filename

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import func, and_

from app import app, db

import assets

from app.dbmodels import (create_unique_object_id, Operator, Sample, SampleTransfer, SampleTransferType, SamplePlate,
    SampleTransferDetail, SamplePlateLayout)

import datetime


#SampleMovementTaskItemData = collections.namedtuple('SampleMovementTaskItemData', 'source_plate_id source_well destination_plate_id destination_well')


def home():
    sample_tranfer_types = db.session.query(SampleTransferType).order_by(SampleTransferType.name)
    return render_template('index.html',sample_tranfer_types=sample_tranfer_types)

def edit_sample_plate():
    return render_template('edit_plate.html')

def sample_report_page(sample_id):
    return render_template('sample_report.html',sample_id=sample_id)


def plate_report_page(plate_barcode):
    return render_template('plate_report.html',plate_barcode=plate_barcode)


def sample_report(sample_id):

    rows = db.session.query(SampleTransfer, SampleTransferDetail, SamplePlateLayout,SamplePlate).filter(and_(
        SampleTransferDetail.source_sample_id==sample_id,SampleTransfer.id==SampleTransferDetail.sample_transfer_id,
        SamplePlateLayout.sample_plate_id==SampleTransferDetail.source_sample_plate_id,
        SamplePlateLayout.sample_id==SampleTransferDetail.source_sample_id,
        SamplePlateLayout.well_id==SampleTransferDetail.source_well_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.source_sample_plate_id)).all()

    first_row = None 

    if len(rows) > 0:
        transfer, transfer_detail, well, plate = rows[0]
        first_row = { 
               "destination_plate_barcode": plate.external_barcode,
               "well_id": well.well_id,
               "column": well.column,
               "row": well.row,
               "task": ""
        }

    rows = db.session.query(SampleTransfer, SampleTransferDetail, SamplePlateLayout,SamplePlate).filter(and_(
        SampleTransferDetail.destination_sample_id==sample_id,SampleTransfer.id==SampleTransferDetail.sample_transfer_id,
        SamplePlateLayout.sample_plate_id==SampleTransferDetail.destination_sample_plate_id,
        SamplePlateLayout.sample_id==SampleTransferDetail.destination_sample_id,
        SamplePlateLayout.well_id==SampleTransferDetail.destination_well_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.destination_sample_plate_id)).all()

    report = [
       { 
           "destination_plate_barcode": plate.external_barcode,
           "well_id": well.well_id,
           "column": well.column,
           "row": well.row,
           "task": transfer.sample_transfer_type.name
       }
       for transfer, transfer_detail, well, plate in rows
    ]

    if first_row:
        report.insert(0,first_row)

    resp = Response(response=json.dumps(report),
        status=200, \
        mimetype="application/json")
    return(resp)


def plate_report(sample_plate_barcode):

    #
    # "ccccccc1234"
    #
    sample_plate = db.session.query(SamplePlate).filter_by(external_barcode=sample_plate_barcode).first()
    sample_plate_id = sample_plate.sample_plate_id

    rows = db.session.query(SamplePlate,SampleTransferDetail).filter(and_(
        SampleTransferDetail.destination_sample_plate_id==sample_plate_id,
        SamplePlate.sample_plate_id==SampleTransferDetail.source_sample_plate_id)).all()

    parent_plates=[]

    
    seen=[]
    for parent_plate, details in rows:
        if parent_plate.sample_plate_id not in seen:
            seen.append(parent_plate.sample_plate_id)
            parent_plates.append({
                "externalBarcode":parent_plate.external_barcode
            })
    

    wells = []

    
    rows = db.session.query(SamplePlateLayout).filter_by(sample_plate_id=sample_plate_id).all()
    for well in rows:
        well_dict = {
            "well_id":well.well_id,
            "column":well.column,
            "row":well.row,
            "sample_id":well.sample_id
        }
        wells.append(well_dict)


    report = {
        "parentPlates":parent_plates,
        "wells":wells
    }

    resp = Response(response=json.dumps(report),
        status=200, \
        mimetype="application/json")
    return(resp)



def get_sample_plate(sample_plate_id):
    sample_plate = db.session.query(SamplePlate).filter_by(sample_plate_id=sample_plate_id).first()

    sample_plate_dict = {
       "sample_plate_id":sample_plate_id,
       "name":sample_plate.name,
       "description":sample_plate.description,
       "samplePlateType":sample_plate.sample_plate_type.name,
       "storageLocation":sample_plate.storage_location.name,
       "status":sample_plate.status,
       "externalBarcode":sample_plate.external_barcode,
    }

    resp = Response(response=json.dumps(sample_plate_dict),
        status=200, \
        mimetype="application/json")
    return(resp)


def sample_plate_external_barcode(sample_plate_id):
    sample_plate = db.session.query(SamplePlate).filter_by(sample_plate_id=sample_plate_id).first()

    if request.method == 'GET':
        sample_plate_dict = {
           "sample_plate_id":sample_plate_id,
           "externalBarcode":sample_plate.external_barcode,
        }

        resp = Response(response=json.dumps(sample_plate_dict),
            status=200, \
            mimetype="application/json")
        return(resp)
    elif request.method == 'POST':
        external_barcode = request.json["externalBarcode"]
        sample_plate.external_barcode = external_barcode
        db.session.commit()
        print "external_barcode: ", external_barcode
        response = {
            "success":True
        }
        return jsonify(response)  



ALLOWED_EXTENSIONS = set(['xls','xlsx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def dragndrop():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + filename
        path_and_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_and_file_name)

        workbook = xlrd.open_workbook(path_and_file_name, on_demand = True)
        print "SHEET NAMES: ", workbook.sheet_names()

        worksheet = workbook.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1

        task_items = []

        print "NUMBER OF ROWS: ", num_rows

        curr_row = 0
        while curr_row < num_rows:
            curr_row += 1
            task_item = {
                "source_plate_id":worksheet.cell_value(curr_row,0),
                "source_well":worksheet.cell_value(curr_row,1),
                "destination_plate_id":worksheet.cell_value(curr_row,2),
                "destination_well":worksheet.cell_value(curr_row,3)
            } 
            row = worksheet.row(curr_row)
            task_items.append(task_item)

        response = {
            "success":True,
            "task_items":task_items
        }


    return jsonify(response)  


"""
    sample_plate_id = db.Column(db.String(40), primary_key=True)
    type_id = db.Column(db.String(40), db.ForeignKey('sample_plate_type.type_id'))
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.operator_id'))
    storage_location_id = db.Column(db.String(10), db.ForeignKey('storage_location.storage_location_id'))
    date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    name = db.Column(db.String(100))
    description = db.Column(db.String(2048))
    external_barcode = db.Column(db.String(100))
    status = db.Column(db.Enum('disposed','in_use','new'),default="new")

"""

def create_sample_movement():
    data = request.json

    #print "received data: ", data
    #
    # SPLT_5457fcf1e208466dd16d3b08
    #

    operator = db.session.query(Operator).filter_by(email="swilliams@twistbioscience.com").first()

    sample_transfer_type_id = data["sampleTransferTypeId"]

    wells = data.get("wells",None)

    if wells:
        print "do wells stuff"
    else:
        source_barcode = data["sourceBarcodeId"]
        destination_barcode = data["destinationBarcodeId"]

        print "source_barcode: ", source_barcode
        print "destination_barcode: ", destination_barcode

        source_plate = db.session.query(SamplePlate).filter_by(external_barcode=source_barcode).first()
        print "SOURCE PLATE: ", source_plate

        source_plate_type_id = source_plate.type_id 
        storage_location_id = source_plate.storage_location_id

        destination_plate_name = create_unique_object_id("PLATE_")
        destination_plate_description = create_unique_object_id("PLATEDESC_")

        #
        # 1. Create the destination sample plate.
        #
        destination_plate = SamplePlate(source_plate_type_id,operator.operator_id,storage_location_id,
            destination_plate_name, destination_plate_description, destination_barcode)
        db.session.add(destination_plate)
        db.session.flush()

        #
        # 2. Create a "sample_transfer" row representing this entire transfer.
        #
        sample_transfer = SampleTransfer(sample_transfer_type_id, operator.operator_id)
        db.session.add(sample_transfer)
        db.session.flush()


        #
        # 3. Iterate through all the wells in the "source" plate. We'll create similar wells for the
        # destination plate.
        #
        order_number = 1
        for source_plate_well in source_plate.wells:

            #
            # 3a. Create a row representing a well in the desination plate.
            #
            destination_plate_well = SamplePlateLayout(destination_plate.sample_plate_id,
                source_plate_well.sample_id,source_plate_well.well_id,operator.operator_id,source_plate_well.row,source_plate_well.column)
            db.session.add(destination_plate_well)

            #
            # 3.b. Create a row representing a transfer from a well in the "source" plate to a well
            # in the "desination" plate.
            #
            source_to_destination_well_transfer = SampleTransferDetail(sample_transfer.id, order_number,
               source_plate.sample_plate_id, source_plate_well.well_id, source_plate_well.sample_id,
               destination_plate.sample_plate_id, destination_plate_well.well_id, destination_plate_well.sample_id)
            db.session.add(source_to_destination_well_transfer)

            order_number += 1

        #
        # Commit the transaction here.
        #
        db.session.commit()

      

 

    response = {
        "success":True
    }


    return jsonify(response)  


def get_sample_plates_list():
    plates = db.session.query(SamplePlate).order_by(SamplePlate.sample_plate_id).all()

    plate_ids = [plate.sample_plate_id for plate in plates]
    
    resp = Response(response=json.dumps(plate_ids),
        status=200, \
        mimetype="application/json")
    return(resp)

def get_sample_plate_barcodes_list():
    plates = db.session.query(SamplePlate).order_by(SamplePlate.sample_plate_id).all()

    plate_barcodes = [plate.external_barcode for plate in plates if plate.external_barcode is not None]
    
    resp = Response(response=json.dumps(plate_barcodes),
        status=200, \
        mimetype="application/json")
    return(resp)


def get_samples_list():

    a = datetime.datetime.now()
    #sql = text('select sample_id from sample')

     
    result = db.engine.execute('select sample_id from sample order by sample_id')
    sample_ids = []
    for row in result:
        sample_ids.append(row[0])
     


    #samples = db.session.query(Sample).all()
    #sample_ids = [sample.sample_id for sample in samples]


    b = datetime.datetime.now()

    c = b - a
    print "TOTAL SECS: ", c.seconds
    print "TOTAL microseconds: ", c.microseconds
    
    resp = Response(response=json.dumps(sample_ids),
        status=200, \
        mimetype="application/json")
    return(resp)




