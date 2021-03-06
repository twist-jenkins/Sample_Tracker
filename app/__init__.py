######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: __init__.py
#
# This is the "root" of the Flask application. It instantiates the "app" object that is used elsewhere.
#
######################################################################################

import os
import logging

from flask import Flask, request, send_from_directory
from flask_assets import Environment
import flask_restful

from webassets.loaders import PythonLoader as PythonAssetsLoader
from twistdb.db import SQLAlchemyX

import assets

logging.basicConfig(level=logging.INFO)
SHOW_SQLALCHEMY_ECHO_TRACE = False  # True
if SHOW_SQLALCHEMY_ECHO_TRACE:
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


######################################################################################
#
# Create the Flask app, load the configuration.
#
######################################################################################

app = Flask(__name__)
env = os.environ.get('WEBSITE_ENV', 'dev')
config_object_name = 'app.config.%sConfig' % env.capitalize()
print "Using configuration environment [%s] and config object [%s]" % (env,config_object_name)
app.config.from_object(config_object_name)
app.config['ENV'] = env
app.debug = True
# app.logger.addHandler(logfile_handler)

######################################################################################
#
# Use the value from the config file - unless the environment provides a dateabase URL (which it will
# in prod on Heroku)
#
######################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',app.config['SQLALCHEMY_DATABASE_URI'])
print "USING DATABASE: ", app.config['SQLALCHEMY_DATABASE_URI']


from twistdb.db import initdb

# initialize database engine:
initdb(engine_url=app.config['SQLALCHEMY_DATABASE_URI'])

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

db = SQLAlchemyX(app)


######################################################################################
#
# Configure Google OAuth Authentication
#
######################################################################################


from flask_googlelogin import GoogleLogin
from flask.ext.login import login_required, LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
googlelogin = GoogleLogin(app, login_manager)
login_manager.login_view = "login"


######################################################################################
#
# All "Routes" Defined here.
#
######################################################################################


from app import routes
from app.routes import transform

# ==========================
#
# "Generic, Utility" Routes
#
# ==========================

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


# ==========================
#
# "Authentication" Routes
#
# ==========================

#
# Show the "login" page (the one with a Google "Sign In" button).
#
@app.route('/login', methods=['GET','POST'])
def login():
    return routes.login()

#
# The user logged in via their Gmail account, but they aren't in the "operator" table.
#
@app.route('/user_missing_from_operator_table')
def user_missing_from_operator_table():
    return routes.user_missing_from_operator_table()


#
# This is invoked when the user clicks the "Sign In" button and enters their Google login (email+password).
# Google oauth calls this function - passing in (via URL query parameter) a "code" value if the user
# clicked the Accept/Allow button when first logging in. If the user clicked Cancel/Decline instead, then no
# code value will be returned.
#
@app.route('/oauth2callback')
def oauth2callback():
    return routes.oauth2callback()

#
# This is a "GET" route that logs the user out from Google oauth (and from this application)
#
@app.route('/logout')
def logout():
    return routes.logout()

# ==========================
#
# The Web Pages
#
# ==========================

#
# This is the "home" page, which is actually the "enter a sample movement" page.
#
"""
@app.route('/')
@login_required
def home():
    return routes.home()
"""
#
# The list of sample transforms
#
@app.route('/sample_transforms')
@login_required
def sample_transforms_page():
    return routes.sample_transforms_page()


#
# This is the page allowing the user to add a barcode to a sample plate.
#
@app.route('/edit_sample_plate')
@login_required
def edit_sample_plate():
    return routes.edit_sample_plate()

#
# This is "Sample Report" page
#
@app.route('/sample_report', defaults={'sample_id':None})
@app.route('/sample_report/<sample_id>')
@login_required
def sample_report_page(sample_id):
    return routes.sample_report_page(sample_id)


#
# This is the "Plate Details Report" page
#
@app.route('/plate_report', defaults={'plate_barcode':None})
@app.route('/plate_report/<plate_barcode>')
@login_required
def plate_report_page(plate_barcode):
    return routes.plate_report_page(plate_barcode)


# ==========================
#
# REST API ROUTES
#
# ==========================

# newer REST API routes:

api = flask_restful.Api(app)

from app.resources import transform_spec, worklist, sample, plate_well

api.add_resource(transform_spec.TransformSpecListResource,
                 '/api/v1/rest/transform-specs')

# 1. POST: Save new spec (returns ID)
# 2. POST: Save new spec and execute (returns ID):
#          uses HTTP header Transform-Execution: Immediate
# 3. PUT: Execute existing spec
api.add_resource(transform_spec.TransformSpecResource,
                 '/api/v1/rest/transform-specs/<spec_id>')

api.add_resource(worklist.WorklistResource,
                 '/api/v1/rest/worklist/<spec_id>')

api.add_resource(sample.SampleResource,
                 '/api/v1/rest/sample/<sample_id>')

api.add_resource(plate_well.PlateWellResource,
                 '/api/v1/rest/plate/<plate_barcode>/well/<well_number>')


# older REST API routes:
#
# The route to which the web page posts the spreadsheet detailing the well-to-well movements of
# samples.
#
@app.route('/dragndrop', methods=['POST'])
def dragndrop():
    return routes.dragndrop()

#
# Returns the JSON representation of a "sample plate" based on the plate's ID.
#
@app.route('/sample_plate/<plate_id>')
def get_sample_plate(plate_id):
    return routes.get_sample_plate(plate_id)

#
# Returns a sample plate id and the barcode for that plate. Or if a POST is sent to this URL,
# updates the barcode for the passed-in sample plate id.
#
@app.route('/sample_plate/<plate_id>/external_barcode',methods=['GET','POST'])
def sample_plate_external_barcode(plate_id):
    return routes.sample_plate_external_barcode(plate_id)

#
# Returns the "Sample Plate" report for a specified sample (specified by id). This can return the
# report as either JSON or a CSV.
#
@app.route('/sample/<sample_id>/report', defaults={'format':"json"})
@app.route('/sample/<sample_id>/report/<format>')
def sample_report(sample_id, format):
    return routes.sample_report(sample_id, format)

#
# Returns the "Plate Details Report" for a specific plate (specified by its barcode). This can return
# the report as either JSON or a CSV.
#
@app.route('/plate/<sample_plate_barcode>/report', defaults={'format':"json"})
@app.route('/plate/<sample_plate_barcode>/report/<format>')
def plate_report(sample_plate_barcode,format):
    return routes.plate_report(sample_plate_barcode,format)


#
# This creates a new "sample movement" or "sample transform."
#
@app.route('/sample_movements', methods=['POST'])
def create_sample_movement():
    return routes.create_sample_movement()

#
# Returns ids of all sample plates. (Used in the UI's "type ahead" field so that the user can specify
# a sample plate by its id).
#
@app.route('/sample_plates')
def get_sample_plates_list():
    return routes.get_sample_plates_list()

#
# Returns barcodes of all sample plates. (Used in the UI's "type ahead" field so that the user can specify
# a sample plate by its barcode).
#
@app.route('/sample_plate_barcodes')
def get_sample_plate_barcodes_list():
    return routes.get_sample_plate_barcodes_list()

#
# Returns the list of sample ids. (Used in the UI's "type ahead" field so that the user can specify
# a sample by its id).
#
@app.route('/samples')
def get_samples_list():
    return routes.get_samples_list()


#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
# ####### ANGULAR APP ROUTES
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################

#
# This is the new app - single page "home"
#
@app.route('/')
def new_home():
    return routes.new_home()


########################################################
# ### api routes
########################################################

#
# This is the route to see if there is a logged-in user. Once the angular route loads from its route, the auth status of the user could change
#
@app.route('/api/v1/user', methods=['GET'])
def user_data():
    return routes.user_data()

@app.route('/google-login', methods=['GET'])
def google_login():
    return routes.google_login()

@app.route('/api/v1/sample-transform-types', methods=['GET'])
def sample_transform_types():
    return routes.sample_transform_types()

@app.route('/api/v1/sample-plate-barcodes', methods=['GET'])
def sample_plate_barcodes():
    return routes.sample_plate_barcodes()

@app.route('/api/v1/track-sample-step', methods=['POST'])
def track_sample_step():
    return routes.create_step_record()

@app.route('/api/v1/sample-plates-list', methods=['GET'])
def sample_plates_list():
    return routes.get_sample_plates_list()

@app.route('/api/v1/plate-info/<plate_id>', methods=['GET'])
def plate_info(plate_id):
    return routes.get_sample_plate(plate_id)

@app.route('/api/v1/update-barcode', methods=['POST'])
def update_barcode():
    return routes.update_plate_barcode()

@app.route('/api/v1/sample-transforms', methods=['GET'])
def sample_transforms():
    return routes.sample_transforms()

@app.route('/api/v1/plate-barcodes/<sample_plate_barcode>/<fmt>',
           methods=['GET'])
@app.route('/api/v1/plate-barcodes/<sample_plate_barcode>',
           defaults={'fmt': 'json'}, methods=['GET'])
def plate_details(sample_plate_barcode, fmt):
    return routes.plate_details(sample_plate_barcode, fmt)

@app.route('/api/v1/basic-plate-info/<plate_barcode>', methods=['GET'])
def basic_plate_info(plate_barcode):
    return routes.plate_details(plate_barcode, "json", True)

@app.route('/api/v1/source-plate-well-data', methods=['POST'])
def source_plate_well_data():
    return routes.source_plate_well_data()


@app.route('/api/v1/check-plates-are-new', methods=['POST'])
def check_plates_are_new():
    return routes.check_plates_are_new()


@app.route('/api/v1/transform-preview/type-<int:transform_type_id>/template-<int:transform_template_id>', methods=('POST',))
def transform_params( transform_type_id, transform_template_id  ):
    from app.routes import transform

    print '@@ transform_type_id:%s, transform_template_id:%s' % (transform_type_id, transform_template_id)

    # shorter names!
    from constants import (
        TRANS_TYPE_EXTRACTION_TITIN as EXTRACTION_TITIN_T,
        TRANS_TPL_EXTRACTION_TITIN as EXTRACTION_TITIN,
        TRANS_TYPE_PRIMER_HITPICK_CREATE_SRC as PRIMER_CREATE_SRC_T,
        TRANS_TPL_PCR_PRIMER_HITPICK as PRIMER_HITPICK,
        TRANS_TYPE_PCR_PRIMER_HITPICK as PRIMER_HITPICK_T,
        TRANS_TPL_SAME_PLATE as SAME_PLATE,
        TRANS_TPL_SAME_LAYOUT as SAME_LAYOUT,
        TRANS_TYPE_ADD_PCA_MASTER_MIX as PRIMER_MASTER_T,
        TRANS_TYPE_PCA_THERMOCYCLE as PRIMER_THERMO_T,
        TRANS_TYPE_PCA_PREPLANNING as PRIMER_PREPLANNING_T,
        TRANS_TPL_PCA_PREPLANNING as PRIMER_PREPLANNING,
        TRANS_TYPE_NGS_THERMOCYCLE as NGS_THERO_T,
        TRANS_TYPE_PCA_THERMOCYCLE as PCA_THERMO_T,
        TRANS_TYPE_PCA_PCR_THERMOCYCLE as PCR_THERMO_T,
        TRANS_TPL_REBATCH_FOR_TRANSFORM as REBATCH_XFORM,
        TRANS_TYPE_REBATCH_FOR_TRANSFORM as REBATCH_XFORM_T,
        TRANS_TYPE_UPLOAD_QUANT as UPLOAD_QUANT_T,
        TRANS_TYPE_NGS_INDEX_HITPICKING as NGS_HITPICKING_T,
        TRANS_TPL_NGS_INDEX_HITPICKING as NGS_HITPICKING,
        TRANS_TYPE_NGS_MASTERMIX_ADDITION as NGS_MASTERMIX_T,
        TRANS_TPL_PCR_PRIMER_HITPICK as PCR_PRIMER_HITPICK,
        TRANS_TYPE_CHP_DEPROTECTION as CHP_DEPROTECTION_T,
        TRANS_TYPE_NGS_LOAD_ON_SEQUENCER as NGS_LOAD_T,
        TRANS_TYPE_NGS_POOLING as NGS_POOLING_T,
        TRANS_TPL_NGS_POOLING as NGS_POOLING,
        TRANS_TYPE_VECTOR_HITPICK as VECTOR_HITPICK_T,
        TRANS_TYPE_VECTOR_HITPICK_CREATE_SRC as VECTOR_CREATE_SRC_T,
        TRANS_TPL_VECTOR_CREATE_SRC as VECTOR_CREATE_SRC,
        TRANS_TYPE_ECR_PCR_PLANNING as ECR_PCR_PLANNING_T,
        TRANS_TPL_ECR_PCR_PLANNING as ECR_PCR_PLANNING,
        TRANS_TYPE_ECR_PCR_SOURCE_PLATE_CREATION as ECR_PCR_SOURCE_PLATE_CREATION_T,
        TRANS_TPL_ECR_PCR_SOURCE_PLATE_CREATION as ECR_PCR_SOURCE_PLATE_CREATION,
        TRANS_TYPE_ECR_PCR_PRIMER_HITPICKING as ECR_PCR_PRIMER_HITPICKING_T,
        TRANS_TPL_ECR_PCR_PRIMER_HITPICKING as ECR_PCR_PRIMER_HITPICKING,
        TRANS_TYPE_ECR_PCR_THERMOCYCLE as ECR_THERMO_T,
        TRANS_TYPE_ECR_PCR_UPLOAD_QUANT as ECR_PCR_UPLOAD_QUANT_T,
        TRANS_TYPE_VECTOR_NORM as VECTOR_NORM_T,
        TRANS_TYPE_PLS_DILUTION as PLS_DILUTION_T,
        TRANS_TPL_MULTIPLEX_SAME_PLATE as MULTIPLEX_SAME_PLATE,
        TRANS_TYPE_MIN_PLANNING as MIN_PLANNING_T,
        TRANS_TPL_MIN_PLANNING as MIN_PLANNING,
        TRANS_TYPE_PCA_PCR_ALIQUOTING as PCA_PCR_ALIQUOTING_T,
        TRANS_TYPE_ECR_PCR_DENATURATION as ECR_PCR_DENATURATION_T,
        TRANS_TYPE_ECR_STAMP_DRY_DOWN as ECR_STAMP_DRY_DOWN_T,
        TRANS_TYPE_ECR_BIODOT as ECR_BIODOT_T,
        TRANS_TYPE_ECR_CYBIO_DISPENSE as ECR_CYBIO_DISPENSE_T,
        TRANS_TYPE_ECR_THERMOCYCLING as ECR_THERMOCYCLING_T,
        TRANS_TYPE_ECR_PCR_ALIQUOTING_FOR_QUANT as ECR_PCR_ALIQUOTING_FOR_QUANT_T,
        TRANS_TYPE_ECR_PCR_STAMP_TO_ECHO as ECR_PCR_STAMP_TO_ECHO_T,
        TRANS_TYPE_FRG_ALIQUOTING_FOR_FRAG as FRG_ALIQUOTING_FOR_FRAG_T,
        TRANS_TPL_FRG_ALIQUOTING_FOR_FRAG as FRG_ALIQUOTING_FOR_FRAG,
        TRANS_TYPE_RCA_CELL_DILUTION_ON_CYBIO as RCA_CELL_DILUTION_ON_CYBIO_T,
        TRANS_TYPE_RCA_BOILING as RCA_BOILING_T,
        TRANS_TYPE_RCA_REAGENT_ADDITION as RCA_REAGENT_ADDITION_T,
        TRANS_TYPE_RCA_FIRST_DILUTION as RCA_FIRST_DILUTION_T
    )

    f = {
        (EXTRACTION_TITIN_T, EXTRACTION_TITIN):
            transform.generic_same_to_same,
        (CHP_DEPROTECTION_T, SAME_PLATE):
            transform.generic_same_to_same,
        (PCA_PCR_ALIQUOTING_T, SAME_LAYOUT):
            transform.generic_same_to_same,
        (ECR_PCR_DENATURATION_T, SAME_PLATE):
            transform.generic_same_to_same,
        (NGS_POOLING_T, NGS_POOLING):
            transform.ngs_pooling,
        (VECTOR_HITPICK_T, SAME_PLATE):
            transform.vector_hitpicking,
        (VECTOR_CREATE_SRC_T, VECTOR_CREATE_SRC):
            transform.vector_create_src,
        (VECTOR_NORM_T, SAME_PLATE):
            transform.generic_same_to_same,
        (PRIMER_PREPLANNING_T, PRIMER_PREPLANNING):
            transform.ecr_pcr_planning, # transform.primer_preplanning,
        (PRIMER_CREATE_SRC_T, VECTOR_CREATE_SRC):
            transform.ecr_pcr_source_plate_creation, # transform.primer_create_src,
        (PRIMER_MASTER_T, SAME_PLATE):
            transform.primer_master_mix,
        (PRIMER_THERMO_T, SAME_PLATE):
            transform.thermocycle,
        (NGS_THERO_T, SAME_PLATE):
            transform.thermocycle,
        (PCA_THERMO_T, SAME_PLATE):
            transform.thermocycle,
        (PCR_THERMO_T, SAME_PLATE):
            transform.thermocycle,
        (ECR_THERMO_T, SAME_PLATE):
            transform.thermocycle,
        (REBATCH_XFORM_T, REBATCH_XFORM):
            transform.rebatch_transform,
        (UPLOAD_QUANT_T, SAME_PLATE):
            transform.quant_upload,
        (ECR_PCR_UPLOAD_QUANT_T, SAME_PLATE):
            transform.quant_upload,
        (NGS_HITPICKING_T, NGS_HITPICKING):
            transform.ngs_hitpicking,
        (MIN_PLANNING_T, MIN_PLANNING):
            transform.min_planning,
        (12, 13):
            transform.generic_same_to_same,  # CLO Transformation
        (13, 14):
            transform.generic_same_to_same,  # CLO Plating on Hamilton
        (19, 18):
            transform.generic_same_to_same,  # RCA Aliquoting
        (25, SAME_PLATE):
            transform.ngs_tagmentation,  # ?? no type constant?
        (NGS_MASTERMIX_T, SAME_PLATE):
            transform.ngs_mastermix,
        (PCR_PRIMER_HITPICK, ):
            transform.pcr_primer_hitpick,
        (NGS_LOAD_T, SAME_PLATE):
            transform.ngs_load,
        (ECR_PCR_PLANNING_T, ECR_PCR_PLANNING):
            transform.ecr_pcr_planning,
        (ECR_PCR_SOURCE_PLATE_CREATION_T, ECR_PCR_SOURCE_PLATE_CREATION):
            transform.ecr_pcr_source_plate_creation,
        (ECR_PCR_PRIMER_HITPICKING_T, ECR_PCR_PRIMER_HITPICKING):
            transform.ecr_pcr_primer_hitpicking,
        (PLS_DILUTION_T, MULTIPLEX_SAME_PLATE):
            transform.pls_dilution,
        (ECR_PCR_PLANNING_T, ECR_PCR_PLANNING):
            transform.ecr_pcr_planning,
        (ECR_PCR_SOURCE_PLATE_CREATION_T, ECR_PCR_SOURCE_PLATE_CREATION):
            transform.ecr_pcr_source_plate_creation,
        (ECR_STAMP_DRY_DOWN_T, SAME_LAYOUT):
            transform.generic_same_layout,
        (ECR_PCR_PRIMER_HITPICKING_T, ECR_PCR_PRIMER_HITPICKING):
            transform.ecr_pcr_primer_hitpicking,
        (ECR_BIODOT_T, SAME_PLATE):
            transform.generic_same_to_same,
        (ECR_CYBIO_DISPENSE_T, SAME_LAYOUT):
            transform.generic_same_layout,
        (ECR_THERMOCYCLING_T, SAME_PLATE):
            transform.thermocycle,
        (ECR_PCR_ALIQUOTING_FOR_QUANT_T, SAME_LAYOUT):
            transform.generic_same_layout,
        (ECR_PCR_STAMP_TO_ECHO_T, SAME_LAYOUT):
            transform.generic_same_layout,
        (FRG_ALIQUOTING_FOR_FRAG_T, FRG_ALIQUOTING_FOR_FRAG):
            transform.frag_aliquoting,
        (RCA_CELL_DILUTION_ON_CYBIO_T, SAME_LAYOUT):
            transform.generic_same_layout,
        (RCA_BOILING_T, SAME_PLATE):
            transform.generic_same_to_same,
        (RCA_REAGENT_ADDITION_T, SAME_PLATE):
            transform.generic_same_to_same,
        (RCA_FIRST_DILUTION_T, SAME_PLATE):
            transform.generic_same_to_same,
    }.get((transform_type_id, transform_template_id), transform.preview)

    print '@@ transform_type_id:%s, transform_template_id:%s -> %s' \
        % (transform_type_id, transform_template_id, f.__name__)

    return f(transform_type_id, transform_template_id)

# hamilton operation routes

@app.route('/api/v1/rest-ham/hamiltons/<hamilton_barcode>', methods=['GET'])
def get_hamilton_by_barcode(hamilton_barcode):
    return routes.get_hamilton_by_barcode(hamilton_barcode)

@app.route('/api/v1/rest-ham/hamiltons/<hamilton_barcode>/carriers/<carrier_barcode>', methods=['GET'])
def get_carrier_by_barcode(carrier_barcode, hamilton_barcode):
    return routes.get_carrier_by_barcode(carrier_barcode, hamilton_barcode)

@app.route('/api/v1/rest-ham/hamilton-plates/<plate_barcode>/transform/<transform_type_id>', methods=['GET'])
def get_plate_ready_for_step(plate_barcode, transform_type_id):
    return routes.get_plate_ready_for_step(plate_barcode, transform_type_id)

@app.route('/api/v1/rest-ham/hamilton-plates/transform/<transform_type_id>', methods=['POST'])
def process_hamilton_sources(transform_type_id):
    return routes.process_hamilton_sources(transform_type_id)

@app.route('/api/v1/rest-ham/trash-samples', methods=['POST'])
def trash_samples():
    return routes.trash_samples()

@app.route('/api/v1/rest-ham/hamilton_worklist/<spec_id>', methods=['GET'])
def get_worklist(spec_id):
    return routes.get_worklist(spec_id)

@app.route('/api/v1/get-date-time', methods=['GET'])
def get_date_time():
    return routes.get_date_time()
