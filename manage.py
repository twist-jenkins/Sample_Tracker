######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: manage.py
#
# This is where we define "scripts" that can be run to do things like load data, run a shell,
# run the web application, etc.
# 
######################################################################################

from flask.ext.script import Manager, Shell, Server

from flask.ext.migrate import Migrate, MigrateCommand

from scripts import (CreateAllTables, LoadLookupTables, DropAllTables)

from app import app, db





manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell())

manager.add_command('createalltables', CreateAllTables())
manager.add_command('loadlookuptables', LoadLookupTables())
manager.add_command('dropalltables', DropAllTables())


manager.run()