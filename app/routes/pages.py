
import os, sys

import time

import hashlib 

import random

import xlrd

import collections

import json

from flask import g, Flask, render_template, make_response, request, Response, redirect, url_for, abort, session, send_from_directory, jsonify

from werkzeug import secure_filename

from app import app, db

from app.dbmodels import Operator, SampleTransferType


#
# This is the "home" page, which is actually the "enter a sample movement" page.
#
def home():
    sample_tranfer_types = db.session.query(SampleTransferType).order_by(SampleTransferType.name)
    return render_template('recordSampleTransfer.html',sample_tranfer_types=sample_tranfer_types,
        current_user_first_and_last=g.user.first_and_last_name)



ALLOWED_EXTENSIONS = set(['xls','xlsx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



#
# The route to which the web page posts the spreadsheet detailing the well-to-well movements of 
# samples.
#
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
                "source_plate_barcode":worksheet.cell_value(curr_row,0),
                "source_well_id":worksheet.cell_value(curr_row,1),
                "source_col_and_row":worksheet.cell_value(curr_row,2),
                "destination_plate_type_name":worksheet.cell_value(curr_row,3),
                "destination_plate_barcode":worksheet.cell_value(curr_row,4),
                "destination_well_id":worksheet.cell_value(curr_row,5),
                "destination_col_and_row":worksheet.cell_value(curr_row,6)
            } 
            row = worksheet.row(curr_row)
            task_items.append(task_item)

        response = {
            "success":True,
            "task_items":task_items
        }


    return jsonify(response)  




#
# This is the page allowing the user to add a barcode to a sample plate.
#
def edit_sample_plate():
    return render_template('edit_plate.html',current_user_first_and_last=g.user.first_and_last_name)

#
# This is "Sample Report" page
#
def sample_report_page(sample_id):
    return render_template('sample_report.html',sample_id=sample_id,current_user_first_and_last=g.user.first_and_last_name)

#
# This is the "Plate Details Report" page
#
def plate_report_page(plate_barcode):
    return render_template('plate_report.html',plate_barcode=plate_barcode,current_user_first_and_last=g.user.first_and_last_name)

