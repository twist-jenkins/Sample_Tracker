######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: config.py
#
# This is configuration file for the Flask app. 
# 
######################################################################################

class Config(object):
    SECRET_KEY = 'secret key, hi scott'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./database_data/data.db'    
    SQLALCHEMY_DATABASE_URI = "postgresql://swilliams:@localhost/sample_movement_tracker"
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb"

    # psql -U twister -h 10.10.21.42 twistdb
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    pass


class StagingConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    
