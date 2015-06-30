
from flask.ext.script import Command
from app import db

class CreateAllTables(Command):

    def run(self):
        print "create all tables"
        #db.create_all()
        print "created!"
