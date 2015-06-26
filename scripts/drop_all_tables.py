
from flask.ext.script import Command
from app import db

class DropAllTables(Command):

    def run(self):
        print "drop all tables"
        db.drop_all()
        print "all tables dropped!"
