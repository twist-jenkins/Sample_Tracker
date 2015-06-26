
import os, sys

import time

import hashlib 

import random

import xlrd

import collections

from flask import Flask, render_template, request, Response, redirect, url_for, abort, session, send_from_directory, jsonify

from flask_assets import Environment

from functools import wraps

from webassets.loaders import PythonLoader as PythonAssetsLoader

from werkzeug import secure_filename

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import func 

from app import app, db

import assets

from app.dbmodels import SampleTransferType



#SampleMovementTaskItemData = collections.namedtuple('SampleMovementTaskItemData', 'source_plate_id source_well destination_plate_id destination_well')


def home():
    sample_tranfer_types = db.session.query(SampleTransferType).order_by(SampleTransferType.name)
    return render_template('index.html',sample_tranfer_types=sample_tranfer_types)



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


def create_sample_movement():
    data = request.json

    print "received data: ", data

    wells = data.get("wells",None)
    print "wells: ", wells

    response = {
        "success":True
    }


    return jsonify(response)  


