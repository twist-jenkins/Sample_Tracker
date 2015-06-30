######################################################################################
#
# Copyright (c) 2015 Twist Bioscience 
#
# File: __init__.py
#
# This is the "root" of the Flask application. It instantiates the "app" object that is used elsewhere.
# 
######################################################################################

import os, sys

import time

import hashlib 

import random

from flask import Flask, render_template, request, Response, redirect, url_for, abort, session, send_from_directory, jsonify

from flask_assets import Environment

from functools import wraps

from webassets.loaders import PythonLoader as PythonAssetsLoader

from werkzeug import secure_filename

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import func 

import assets




######################################################################################
#
# Create the Flask app, load the configuration.
#
######################################################################################

app = Flask(__name__)
env = os.environ.get('WEBSITE_ENV', 'dev')
app.config.from_object('app.config.%sConfig' % env.capitalize())
app.config['ENV'] = env
app.debug = True

print "USING ENVIRONMENT: " + env


#
# Use the value from the config file - unless the environment provides a dateabase URL (which it will
# in prod on Heroku)
#
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',app.config['SQLALCHEMY_DATABASE_URI'])

print "USING DB CONNECTION: " + app.config['SQLALCHEMY_DATABASE_URI']


UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



######################################################################################
#
# Configure the Flask-Assets functionality. Each "bundle" is a chunk of JavaScript/CSS/etc. files that will be
# available to the browser from one of the "deploy" directories within the "static" directory.
#
######################################################################################

assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)


######################################################################################
#
# The database.
#
######################################################################################

db = SQLAlchemy(app)

from dbmodels import *


#from dbmodels import (Author, Article, BlogPostSectionType, BlogPostAuthor, BlogPost, BlogPostSection, 
#    BlogUpdateJournal, UserSegment, TopOfPageContent, TopOfPageContentUpdateJournal, CalendarEventType,
#    CalendarEvent,NewsArticleType, MediaType, PublicationType, Publication, NewsArticle)


#from blog_controller import LoadBlogPosts
#
#from top_of_page_controller import TopOfPageController
#
#from calendar_events_controller import CalendarEventsController
#
#from news_articles_controller import NewsArticlesController
#
#from publications_controller import PublicationsController


######################################################################################
#
# Route! In a larger app, you'd want to break these out into a "routes.py" file.
#
######################################################################################

import routes

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def home():
    return routes.home()

@app.route('/edit_sample_plate')
def edit_sample_plate():
    return routes.edit_sample_plate()

@app.route('/sample_plate/<sample_plate_id>')
def get_sample_plate(sample_plate_id):
    return routes.get_sample_plate(sample_plate_id)

@app.route('/sample_plate/<sample_plate_id>/external_barcode',methods=['GET','POST'])
def sample_plate_external_barcode(sample_plate_id):
    return routes.sample_plate_external_barcode(sample_plate_id)


@app.route('/sample_report', defaults={'sample_id':None})
@app.route('/sample_report/<sample_id>')
def sample_report_page(sample_id):
    return routes.sample_report_page(sample_id)

@app.route('/sample/<sample_id>/report')
def sample_report(sample_id):
    return routes.sample_report(sample_id)

@app.route('/plate_report', defaults={'plate_barcode':None})
@app.route('/plate_report/<plate_barcode>')
def plate_report_page(plate_barcode):
    return routes.plate_report_page(plate_barcode)

@app.route('/plate/<sample_plate_barcode>/report')
def plate_report(sample_plate_barcode):
    return routes.plate_report(sample_plate_barcode)


"""
def home():
    return render_template('index.html')
"""


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        customer = CustomerController.customer_by_email(email)
        admin_user = UserController.admin_user_by_email(email)

        logger.info("Login attempt for user [%s]" % (email))
        logger.info("customer %r" % (customer))
        logger.info("admin_user %r" % (admin_user))

        if admin_user:
            session['admin_user_id'] = admin_user.id
            return redirect(url_for('orders'))
        elif customer:
            session['customer_id'] = customer.id
            if customer.institution:
                return redirect(url_for('customer_settings',customer_id=customer.id))
            else:
                return redirect(url_for('customer_onboard',customer_id=customer.id))
        else:
            return "Invalid Login. Go here: <a href='" + url_for('login') + "'>Log In</a>"
    else:
        return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id',None)
    session.pop('customer_id',None)
    session.pop('admin_user_id',None)
    return redirect(url_for('login'))




@app.route('/dragndrop', methods=['POST'])
def dragndrop():
    return routes.dragndrop()

@app.route('/sample_movements', methods=['POST'])
def create_sample_movement():
    return routes.create_sample_movement()


@app.route('/sample_plates')
def get_sample_plates_list():
    return routes.get_sample_plates_list()


@app.route('/sample_plate_barcodes')
def get_sample_plate_barcodes_list():
    return routes.get_sample_plate_barcodes_list()


@app.route('/samples')
def get_samples_list():
    return routes.get_samples_list()


"""
@app.route('/create_sample_moveme', methods=['POST'])
def calculate_sequence_statistics():
    return ServiceRoutes.calculate_sequence_statistics()
"""


