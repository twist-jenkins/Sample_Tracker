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

    GOOGLE_LOGIN_CLIENT_ID = "1093207984325-qhls4ec361elichdn0vfno05u0r7r256.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "EWohyxtKDkcZyF1BBEPu_Jo1"
    GOOGLE_LOGIN_CLIENT_SCOPES = "email"
    GOOGLE_LOGIN_REDIRECT_URI = "http://localhost:5000/oauth2callback"

    GOOGLE_OAUTH2_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

    """

    GOOGLE_LOGIN_CLIENT_ID  Client ID (create one at https://code.google.com/apis/console)
GOOGLE_LOGIN_CLIENT_SECRET  Client Secret
GOOGLE_LOGIN_CLIENT_SCOPES  Default scopes
GOOGLE_LOGIN_REDIRECT_URI


    Client ID   
1093207984325-qhls4ec361elichdn0vfno05u0r7r256.apps.googleusercontent.com
Email address   
1093207984325-qhls4ec361elichdn0vfno05u0r7r256@developer.gserviceaccount.com
Client secret   
EWohyxtKDkcZyF1BBEPu_Jo1
Redirect URIs   
http://localhost:5000/oauth2callback
JavaScript origins  
http://localhost:5000
    """


class ProdConfig(Config):
    pass


class StagingConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    
