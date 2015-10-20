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

    GOOGLE_LOGIN_CLIENT_ID = "751130267692-eed3irkpojv6euceh41bkopk3v9q9e97.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "BejdwirP4k6g0l8WDZyMBTwL"
    GOOGLE_LOGIN_CLIENT_SCOPES = "email"

    GOOGLE_OAUTH2_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'



class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" #"postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb_prod"
    SQLALCHEMY_DATABASE_URI = "postgresql://synapp_test_user:iE24YYYw7f7MRaFgW9uHf@10.10.20.20/synapp_test"


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" #"postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb"


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" # "postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb"
    #SQLALCHEMY_DATABASE_URI = "postgresql://synapp_test_user:iE24YYYw7f7MRaFgW9uHf@10.10.20.20/synapp_test"
    #SQLALCHEMY_DATABASE_URI = "postgresql://synapp_test_user:jOf-yIf-cE-hunT-@10.10.21.38/synapp_test"
    DEBUG = True


class UnittestConfig(Config):
    TESTING = True
    DEBUG = True
    # WTF_CSRF_ENABLED = True
    DATABASE = ":memory:"  # tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE


class LocalunittestConfig(Config):
    TESTING = True
    DEBUG = True
    # WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "postgresql://cledogar:postgres@localhost/dev"
