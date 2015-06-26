######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: dbmodels.py
#
# The database models used by SQLAlchemy. These are used for the parts of the web app that
# are data driven - such as the "publications" page.
# 
######################################################################################


from app import app
from app import db
import datetime


"""
operator_id character varying(10) NOT NULL,
    jira_username character varying(100),
    email character varying(120) NOT NULL,
    user_id character varying(80) NOT NULL,
    first_name character varying(80),
    middle_initial character varying(1),
    last_name character varying(80),
    role integer,
    last_seen timestamp without time zone,
    initials character varying(10),
    ip_addr character varying(20),
    login_count integer
"""

class SampleTransferType(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name ):
        self.name = name

    def __repr__(self):
        return '<SampleTransferType id: [%d] name: [%s] >' % (self.id,self.name)


