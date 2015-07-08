######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: app/routes/pages.py
#
# These are the handlers for all the web pages of the application. (These are not JSON/REST routes, they
# are only web page routes.)
# 
######################################################################################

import os, sys

import time

import hashlib 

import random

import xlrd

import collections

import json

from flask import g, Flask, render_template, make_response, request, Response, redirect, url_for, abort, session, send_from_directory, jsonify

from sqlalchemy import and_ 

from app import app, db

from app.dbmodels import Operator, SampleTransferType, SampleTransfer, SampleTransferDetail


#
# This is the "home" page, which is actually the "enter a sample movement" page.
#
def home():
    sample_tranfer_types = db.session.query(SampleTransferType).order_by(SampleTransferType.name)
    return render_template('recordSampleTransfer.html',sample_tranfer_types=sample_tranfer_types,
        current_user_first_and_last=g.user.first_and_last_name)





#
# The list of sample transfers
#
def sample_transfers_page():
    rows = db.session.query(SampleTransfer, SampleTransferDetail).filter(
        SampleTransferDetail.sample_transfer_id==SampleTransfer.id).order_by(
        SampleTransfer.date_transfer.desc()).all()

    sample_transfer_details = []

    seen = []

    for transfer,details in rows:
        if (transfer.id,details.source_sample_plate_id,details.destination_sample_plate_id) not in seen:
            seen.append((transfer.id,details.source_sample_plate_id,details.destination_sample_plate_id))
            sample_transfer_details.append((transfer,details))



    return render_template('viewSampleTransfers.html',
        sample_transfer_details=sample_transfer_details,
        current_user_first_and_last=g.user.first_and_last_name)





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

