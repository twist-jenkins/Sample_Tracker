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

from app import app, db

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell())


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """
    from twistdb.db import initdb
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    print '@@ config:', db_url
    initdb(engine_url=db_url, create_tables=True)
    # Base.metadata.create_all(bind=db.engine) test


@manager.command
def dropdb():
    """Remove database schema and tables."""
    with app.app_context():
        from twistdb.util import seed
        seed.drop_data(db.engine)


@manager.command
def seed():
    """ Seed a database with starting default table values for CVs."""
    from twistdb.util import seed
    seed.seed_data(db.engine)

    # for now, go ahead and add the fixtures too.
    # TODO: populate fixtures more intelligently, as part of testing, not setup
    # add_fixtures()


@manager.command
def fixtures():
    """ Add database fixtures with test data values."""
    from twistdb.util import seed
    fixture_root = "test/fixture_data"
    seed.seed_data(db.engine, fixture_root)


@manager.command
def fixture_ginkgo():
    """ Add database fixtures with test data values from Ginkgo order."""
    from twistdb.util import seed
    fixture_root = "test/ginkgo_fixture"
    seed.seed_data(db.engine, fixture_root)


@manager.command
def fixture_warp1():
    """ Add database fixtures with test data values from WARP1."""
    from twistdb.util import seed
    fixture_root = "test/fixture_warp1"
    seed.seed_data(db.engine, fixture_root)

@manager.command
def fixture_warp3():
    """ Add database fixtures with test data values from WARP3."""
    from twistdb.util import seed
    fixture_root = "test/fixture_warp3"
    seed.seed_data(db.engine, fixture_root)


manager.run()
