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

from scripts import (CreateAllTables, LoadLookupTables, DropAllTables,
    DeleteSampleTransfer, ImportSampleTransferTemplate)

from app import app, db





manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell())

manager.add_command('createalltables', CreateAllTables())
manager.add_command('loadlookuptables', LoadLookupTables())
manager.add_command('dropalltables', DropAllTables())

#
# Example: python manage.py deletesampletransfer -id 3
#
manager.add_command('deletesampletransfer', DeleteSampleTransfer())

#
# Example: python manage.py importtemplate -f TemplateExample.xlsx -n "the template name"
#
# python manage.py importtemplate -f Template384to48.csv -n "384 to 48"
#
manager.add_command('importtemplate', ImportSampleTransferTemplate())


@manager.command
def seed():
    """ Seed a database with starting default table values for CVs."""
    from twistdb.util import seed
    seed_data_file_name = "app/seed_data/smt_seed_data.xlsx"
    tables_to_seed = ['sampletrack.sample_transfer_template',
                      'sampletrack.sample_transfer_type',
                      'public.sample_plate_type',
                      'public.sample_plate',
                      'public.barcode_sequence',
                      'public.sample_type'
                      ]
    seed.seed_data(db.engine, seed_data_file_name, tables_to_seed)


manager.run()
