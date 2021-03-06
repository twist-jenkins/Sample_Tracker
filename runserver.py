#!/usr/bin/env python

######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: runserver.py
#
# This is used to run the server locally for development when you want the server listening
# on part 80.
# 
######################################################################################



from app import app
import os

port = int(os.environ.get('WEBSITE_PORT', 80))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
