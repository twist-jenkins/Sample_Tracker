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
    SQLALCHEMY_DATABASE_URI = "postgresql://sampletrack:Of2dAd8cir5Y@10.10.120.94/synapp_test"
    """
    synapp_test=#
        create user sampletrack with password 'Of2dAd8cir5Y';
        grant all on sampletrack to sampletrack ;
        grant all privileges on all tables in schema sampletrack to sampletrack ;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO sampletrack;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO sampletrack;
    """


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://twister:Of2dAd8cir5Y@10.10.53.47/twistdb"
    #SQLALCHEMY_DATABASE_URI = "postgresql://synapp_test_user:iE24YYYw7f7MRaFgW9uHf@10.10.20.20/synapp_test"

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
    # WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = \
        "postgresql://sampletrack_user:Of2dAd8cir5Y@localhost/synapp_test"
    """
    psql -d synapp_test   # as superuser
    synapp_test=#
create user sampletrack_user with password 'Of2dAd8cir5Y';
grant all on schema sampletrack to sampletrack_user ;
GRANT ALL ON ALL TABLES IN SCHEMA sampletrack TO sampletrack_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA sampletrack GRANT ALL ON TABLES TO sampletrack_user;
ALTER ROLE sampletrack_user SET search_path TO sampletrack,public;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO sampletrack_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO sampletrack_user;
GRANT USAGE ON schema public TO sampletrack_user;

# can't seem to get the right permissions...
GRANT ALL ON ALL TABLES IN SCHEMA public TO sampletrack_user;
ERROR:  relation "sampletrack.*" does not exist
alter table sampletrack.alembic_version owner to sampletrack_user;
alter table sampletrack.sample_transfer owner to sampletrack_user;
alter table sampletrack.sample_transfer_detail owner to sampletrack_user;
alter table sampletrack.sample_transfer_plan owner to sampletrack_user;
alter table sampletrack.sample_transfer_template owner to sampletrack_user;
alter table sampletrack.sample_transfer_template_details owner to sampletrack_user;
alter table sampletrack.sample_transfer_type owner to sampletrack_user;
alter table sampletrack.shipment_order_item_join set schema public;
    """
