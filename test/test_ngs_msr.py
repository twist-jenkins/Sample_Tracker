#!/bin/env python

import pytest
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

os.environ["WEBSITE_ENV"] = "Local"

# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import login_manager

from test_flask_app import AutomatedTestingUser, rnd_bc

ROOT_PLATE_BARCODE = 'SRN 000577 SM-30'
login_manager.anonymous_user = AutomatedTestingUser
client = app.test_client()


def DISABLED_test_pooling():
    # 11. We should be able to get a miseq sample sheet
    # 'https://sampletransfer-stg.twistbioscience.com/api/v1/rest/transform-specs/194.miseq.csv'
    new_spec_url = 'FIXME'
    miseq_csv_url = new_spec_url + ".miseq.csv"
    rv = client.get(miseq_csv_url,
                         content_type="application/json")
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert 'Amplicon' in result


def test_miseq_run_loading():
    rnd = rnd_bc()
    dest_plate_1_barcode = rnd + '_1'
    dest_plate_2_barcode = rnd + '_2'
    transform_map = [{
        "source_plate_barcode": ROOT_PLATE_BARCODE,
        "source_well_name": src_well,
        "source_well_number": src_number,
        "destination_plate_barcode": dest_plate,
        "destination_well_name": dest_well,
        "destination_well_number": dest_number,
        "destination_plate_type": "SPTT_0005",
        "destination_plate_well_count": dest_well_count
    } for (src_well, src_number, dest_plate, dest_well,
           dest_number, dest_well_count) in [
        ('A1', 1, dest_plate_1_barcode, 'A1', 1, 96),
        ('A1', 1, dest_plate_1_barcode, 'A2', 2, 96),
        ('A2', 2, dest_plate_1_barcode, 'B1', 13, 96),
        ('B1', 25, dest_plate_2_barcode, 'A1', 1, 96),
        ('B1', 25, dest_plate_2_barcode, 'A2', 2, 96),
    ]]
    data = {"sampleTransformTypeId": 15,  # QPix To 96 plates
            "sampleTransformTemplateId": 21,
            "transformMap": transform_map
            }
    rv = client.post('/api/v1/track-sample-step',
                          data=json.dumps(data),
                          content_type='application/json')
    assert rv.status_code == 200, rv.data
    result = json.loads(rv.data)
    assert result["success"] is True

    rv = client.get('/api/v1/basic-plate-info/%s'
                         % dest_plate_1_barcode,
                         content_type='application/json')
    assert rv.status_code == 200, rv.data
    result = json.loads(rv.data)
    print result
    assert result["success"] is True


def test_small_ngs_prep_golden():
    rnd = rnd_bc()
    dest_plate_1_barcode = rnd + '_1'
    dest_plate_2_barcode = rnd + '_2'
    transform_map = [{
        "source_plate_barcode": ROOT_PLATE_BARCODE,
        "source_well_name": src_well,
        "source_well_number": src_number,
        "destination_plate_barcode": dest_plate,
        "destination_well_name": dest_well,
        "destination_well_number": dest_number,
        "destination_plate_type": "SPTT_0005",
        "destination_plate_well_count": dest_well_count
    } for (src_well, src_number, dest_plate, dest_well,
           dest_number, dest_well_count) in [
        ('A1', 1, dest_plate_1_barcode, 'A1', 1, 96),
        ('A1', 1, dest_plate_1_barcode, 'A2', 2, 96),
        ('A2', 2, dest_plate_1_barcode, 'B1', 13, 96),
        ('B1', 13, dest_plate_2_barcode, 'A1', 1, 96),
        ('B1', 13, dest_plate_2_barcode, 'A2', 2, 96),
    ]]

    data = {"sampleTransformTypeId": 26,  # NGS Prep: Barcode Hitpicking
            "sampleTransformTemplateId": 21,
            "transformMap": transform_map
            }
    rv = client.post('/api/v1/track-sample-step',
                          data=json.dumps(data),
                          content_type='application/json')
    assert rv.status_code == 200, rv.data
    result = json.loads(rv.data)
    assert result["success"] is True

    rv = client.get('/api/v1/basic-plate-info/%s'
                    % dest_plate_1_barcode,
                    content_type='application/json')
    assert rv.status_code == 200, rv.data
    result = json.loads(rv.data)
    print result
    assert result["success"] is True



