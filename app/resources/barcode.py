"""Define REST resources for Label and Barcode printing."""

# import json
# import logging
# from datetime import datetime
import re

import flask_restful
# from flask import request
# from flask.ext.restful import abort
# from flask_login import current_user

# from marshmallow import Schema, fields

from app import app
# from app import db, constants
from app.utils import json_api_success#, scoped_session

# from twistdb.sampletrack import Sample, Plate

################################################################################

__author__ = 'Chris Barlow <cbarlow@twistbioscience.com>'

api = flask_restful.Api(app)

# default printer (IP, PORT)
PRINTERS = {
    'zebra':    ('10.10.20.40', 9100),
    'zebra3':   ('10.10.20.98', 9100),
}

# LABELS config including default printer, regex for validating input data, and the ZPL template for printing the label
# is initially set to an empty string and subsequently defined below this dictionary
LABELS = {
    'CARRIER': {
        'printer': 'zebra',
        'regex': r'',
        'template': ''
    },
    'CARRIER_POS': {
        'printer': 'zebra',
        'regex': r'',
        'template': ''
    },
    'PLATE': {
        'printer': 'zebra3',
        'regex': r'^p[A-Z]{3}xB\d{4}[A-Z]{2}\d{6}$',
        'template': ''
    },
    'TUBE': {
        'printer': 'zebra',
        'regex': r'',
        'template': ''
    }
}

LABELS['CARRIER']['template'] = '''
# START LABEL (^start label^don't reverse colors)
^XA^LRN
# PRINT MAX WIDTH in dots (1.5inch == 300dpi?)
^PW1200
# LABEL HOME (start position) (0,11 seems to be the top-center)
^LH0,0
%s
^XZ
'''

LABELS['CARRIER_POS']['template'] = '''
# START LABEL (^start label^don't reverse colors)
^XA^LRN
# PRINT MAX WIDTH in dots (1.5inch == 300dpi?)
^PW1200
# LABEL HOME (start position) (0,11 seems to be the top-center)
^LH0,0
%s
^XZ
'''

# LABELS['PLATE']['template'] = '''
# # START LABEL (^start label^don't reverse colors)
# ^XA^LRN
# # PRINT MAX WIDTH in dots (1.5inch == 300dpi?)
# ^PW1250
# # LABEL HOME (start position) (0,11 seems to be the top-center)
# ^LH0,30
# # BARCODE DEFAULTS (width,width_ratio,height)
# ^BY5,4,60
# # Code 128 Barcode
# ^BCI,60,N,N,N^FO10,30^FD%s^FS
# # Text on Right
# ^FO400,95^A1N,25,20^FD%s%s^FS
# ^XZ
# '''

LABELS['PLATE']['template'] = '''
^XA
^XFE:PLATE.ZPL^FS
^FN1^FD%s^FS
^FN2^FD%s^FS
^FN3^FD%s^FS
^XZ
'''

LABELS['TUBE']['template'] = '''
# START LABEL (^start label^don't reverse colors)
^XA^LRN
# PRINT MAX WIDTH in dots (1.5inch == 300dpi?)
^PW1200
# LABEL HOME (start position) (0,11 seems to be the top-center)
^LH0,0
%s
^XZ
'''

################################################################################

class BarcodeError(Exception):
    """Generic Barcode error"""
    pass

class Zebra:
    """Anything related to Zebra printing including opening socket connections and sending ZPL data to printers"""

    def print_zpl(self, zpl, printer=None):
        """Send ZPL to printer"""
        if printer not in PRINTERS:
            raise BarcodeError('Unknown printer (%s)' % printer)

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(PRINTERS[printer])

        lines = zpl.strip().split('\n')

        if not lines or not len(lines) or lines == ['']:
            print "- EMPTY LABEL DATA RECEIVED; EXITING -"
            return False

        zpl = '\n'.join([l for l in lines if l[0] != '#'])
        print zpl

        s.send(zpl)
        return zpl

    def send(self, label_data, label_type='plate', printer=None):
        """Generate ZPL from label template and send it to the label's default printer"""
        label_type = label_type.upper()
        label_vars = LABELS[label_type]

        # validate label_data against the label type's regex
        if not len(re.findall(label_vars['regex'], label_data)):
            raise BarcodeError(123, 'Invalid label data for %s.' % label_type)

        # build label ZPL from its template and send the genrated ZPL to the printer
        if label_type == 'CARRIER':
            return self.print_zpl(label_vars['template'], printer or label_vars['printer'])

        elif label_type == 'CARRIER_POS':
            return self.print_zpl(label_vars['template'], printer or label_vars['printer'])

        elif label_type == 'PLATE':
            args = (label_data, label_data[:10], label_data[10:])
            return self.print_zpl(label_vars['template'] % args, printer or label_vars['printer'])

        elif label_type == 'TUBE':
            return self.print_zpl(label_vars['template'], printer or label_vars['printer'])

class BarcodeResource(flask_restful.Resource):
    """REST endpoint for label and barcode printing"""

    # init Zebra
    def __init__(self):
        self.zebra = Zebra()

    def get(self, label_data, label_type='PLATE', printer=None, *args, **kwargs):
        label_type = label_type.upper()
        if not printer:
            printer = LABELS[label_type]['printer']

        import datetime
        result = {
            'date': str(datetime.datetime.now())[:19],
            'status': 'label_printed',
            'label_type': label_type,
            'label_data': label_data,
            'label_printer': printer
        }

        try:
            result['zpl'] = self.zebra.send(label_data, label_type, printer)
        except BarcodeError, err:
            result['status'] = 'invalid_label_format'
            print "BarcodeError: %s" % repr(err.args)
            return json_api_success(result, 200)

        return json_api_success(result, 200)

    ### NOT IMPLEMENTED ###
    def delete(self, label_data, label_type='PLATE', printer=None):
        raise NotImplementedError
    def post(self, label_data, label_type='plate', printer=None):
        raise NotImplementedError
    def put(self, label_data, label_type='plate', printer=None):
        raise NotImplementedError
