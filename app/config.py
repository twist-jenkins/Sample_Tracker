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
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb"
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb"

    

    SQLALCHEMY_ECHO = False

    GOOGLE_LOGIN_CLIENT_ID = "1093207984325-qhls4ec361elichdn0vfno05u0r7r256.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "EWohyxtKDkcZyF1BBEPu_Jo1"
    GOOGLE_LOGIN_CLIENT_SCOPES = "email"

    GOOGLE_OAUTH2_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'



class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" #"postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb_prod"


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" #"postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb"


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" # "postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb"
    #SQLALCHEMY_DATABASE_URI = "postgresql://synapp_test_user:jOf-yIf-cE-hunT-@10.10.21.38/synapp_test"
    DEBUG = True
    
