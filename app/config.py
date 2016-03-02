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
    #SQLALCHEMY_DATABASE_URI = 'postgresql://test@localhost/test'

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # to turn off annoying warnings

    GOOGLE_LOGIN_CLIENT_ID = "751130267692-eed3irkpojv6euceh41bkopk3v9q9e97.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "BejdwirP4k6g0l8WDZyMBTwL"
    GOOGLE_LOGIN_CLIENT_SCOPES = "email"

    GOOGLE_OAUTH2_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb" #"postgresql://twister:Of2dAd8cir5Y@10.10.21.42/twistdb_prod"
    SQLALCHEMY_DATABASE_URI = "postgresql://synapp_test_user:iE24YYYw7f7MRaFgW9uHf@10.10.20.20/synapp_test"
    #SQLALCHEMY_DATABASE_URI = 'postgresql://test@localhost/test'


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.120.94/warp1smt"
    # SQLALCHEMY_DATABASE_URI = "postgresql://sampletrack:Of2dAd8cir5Y@10.10.120.94/synapp_test"
    """
    synapp_test=#
        create user sampletrack with password 'Of2dAd8cir5Y';
        grant all on sampletrack to sampletrack ;
        grant all privileges on all tables in schema sampletrack to sampletrack ;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO sampletrack;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO sampletrack;
    """


class Warp1Config(Config):
    # SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.120.94/warp1smt"
    SQLALCHEMY_DATABASE_URI = "The Warp1 database is now considered frozen"


class Warp2Config(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.120.94/warp2smt231"

class Warp3Config(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.120.94/warp3smt234"

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/smtdev"

    DEBUG = True


class UnittestConfig(Config):
    TESTING = True
    DEBUG = True
    # WTF_CSRF_ENABLED = True
    DATABASE = ":memory:"  # tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE


class LocalConfig(Config):
    TESTING = True
    DEBUG = True
    # SQLALCHEMY_ECHO = True

    # WTF_CSRF_ENABLED = True
    # SQLALCHEMY_DATABASE_URI = "postgresql://test:test@dev01.twistbioscience.com/test"
    SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost/orders_dev'


class LocalechoConfig(LocalConfig):
    SQLALCHEMY_ECHO = True


class Warp1localConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://:@localhost/orders_dev'
