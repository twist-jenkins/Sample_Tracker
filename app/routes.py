
import os, sys

import time

import hashlib 

import random

import xlrd

import collections

import json

from flask import g, Flask, render_template, make_response, request, Response, redirect, url_for, abort, session, send_from_directory, jsonify

from flask_assets import Environment

from functools import wraps

from webassets.loaders import PythonLoader as PythonAssetsLoader

from werkzeug import secure_filename

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import func, and_

from app import app, db

import assets

from app.dbmodels import (create_unique_object_id, Operator, Sample, SampleTransfer, SampleTransferType, SamplePlate,
    SampleTransferDetail, SamplePlateLayout, SamplePlateType)

import datetime

from flask.ext.login import current_user, login_user

from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

from app import login_manager

import requests

from app import googlelogin

from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)


######################################################################################
#
# "Authentication" Helper Methods
#
######################################################################################

"""
@app.before_request
def before_request():
    g.user = current_user

def login_to_google(code, redirect_uri):
    

    token = requests.post(app.config['GOOGLE_OAUTH2_TOKEN_URL'], data=dict(
        code=code,
        redirect_uri=redirect_uri,
        grant_type='authorization_code',
        client_id=app.config['GOOGLE_LOGIN_CLIENT_ID'],
        client_secret=app.config['GOOGLE_LOGIN_CLIENT_SECRET'],
    )).json

    if not token or token.get('error'):
        abort(400)

    userinfo = requests.get(app.config['GOOGLE_OAUTH2_USERINFO_URL'], params=dict(
        access_token=token['access_token'],
    )).json
    if not userinfo or userinfo.get('error'):
        abort(400)

    return token, userinfo


#
# Magically called by google_login plumbing when "login_user" is invoked (see "create_or_update_user").
# 
@login_manager.user_loader
def load_user(email):
    return db.session.query(Operator).filter_by(email=email).first()

#
# Called by the "oauth2callback" route code once the user's token and info have been retrieved.
# It is within this code that we look up the user in the "Operator" table and assign that user to the
# google_login "current_user" object and the g.user object.
#
def create_or_update_user(token, userinfo, **params):

    user_email = userinfo.get("email")

    operator = db.session.query(Operator).filter_by(email=user_email).first()
    
    #
    # This causes the "load_user" function to be called!!!
    #
    login_user(operator)  

    #g.user = operator

    return redirect(url_for('home'))



# ==========================
#
# "Authentication" Routes
#
# ==========================


#
# Show the "login" page (the one with a Google "Sign In" button).
#
def login():
    return render_template('login.html',login_url=googlelogin.login_url(scopes=['https://www.googleapis.com/auth/userinfo.email']))


#
# This is invoked when the user clicks the "Sign In" button and enters their Google login (email+password). 
# Google oauth calls this function - passing in (via URL query parameter) a "code" value if the user 
# clicked the Accept/Allow button when first logging in. If the user clicked Cancel/Decline instead, then no
# code value will be returned.
#
def oauth2callback():
    #
    # If there is a "code" value, then that means the user successfully logged in. At this point,
    # we'll make a call to google - exchanging that code value for a token and user data.
    #
    code = request.args.get('code')

    if code:
        token, userinfo = login_to_google(code, url_for('oauth2callback',_external=True)) 
        return create_or_update_user(token, userinfo)

    #
    # If the user gets to the point of logging in to google but then declines to allow our app
    # to access their credentials, "code" will not be sent to us. In that case, we just redirect back
    # to our login page again.
    #
    else:
        return redirect(url_for('login'))


#
# This is a "GET" route that logs the user out from Google oauth (and from this application)
#
def logout():
    logout_user()
    g.user = None
    return redirect(url_for('login'))

"""


# ==========================
#
# The Web Pages
#
# ==========================

"""

#
# This is the "home" page, which is actually the "enter a sample movement" page.
#
def home():
    sample_tranfer_types = db.session.query(SampleTransferType).order_by(SampleTransferType.name)
    return render_template('recordSampleTransfer.html',sample_tranfer_types=sample_tranfer_types,
        current_user_first_and_last=current_user.first_and_last_name)



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
    return render_template('edit_plate.html',current_user_first_and_last=current_user.first_and_last_name)

#
# This is "Sample Report" page
#
def sample_report_page(sample_id):
    return render_template('sample_report.html',sample_id=sample_id,current_user_first_and_last=current_user.first_and_last_name)

#
# This is the "Plate Details Report" page
#
def plate_report_page(plate_barcode):
    return render_template('plate_report.html',plate_barcode=plate_barcode,current_user_first_and_last=current_user.first_and_last_name)

"""



# ==========================
#
# REST API ROUTES
#
# ==========================
