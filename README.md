# Sample Tracker

![SampleTracker logo](http://yt3.ggpht.com/-7tic0TpPpeI/AAAAAAAAAAI/AAAAAAAAAAA/bApALLkNBPM/s88-c-k-no/photo.jpg)

A sample tracking webapp based on Flask, Angular, and Python 2.7.

&copy; 2016 Twist Bioscience.



# 1. Frontend Setup

```

TBD!  This doesn't seem to work right now:

# Install javascript/css/font/bower dependencies - managed by bower
bower install
# Install node dependencies
npm install grunt-bower-install-simple --save-dev
npm install
npm install -g grunt-cli
# run grunt 
grunt

```

Note: If you run 
```grunt watch```
instead of ```grunt``` you'll pick up other peoples' upstream changes.

# 2. Backend Setup

### Dev environment -- one-time:

(This assumes you are running OS-X 10.11 / El Capitan)

1. Install XCode
2. Install XCode Command-line Tools (167MB .dmg)
3. Install Postgres.app: http://postgresapp.com/
4. Install Homebrew: http://brew.sh/
5. Install Python:  

```
brew install python

pip install virtualenv
```

### Initial App Setup -- one-time:

```
git clone https://github.com/Twistbioscience/sample_movement_tracker.git

   # you may need to add your ssh key into your github profile

cd sample_movement_tracker

git checkout develop  # Gitflow convention: work against the "develop" branch

virtualenv venv  # Places the virtual environment files alongside the code

source venv/bin/activate  # Changes your $PATH to use the virtual environment

pip install -U setuptools pip  # Update the python setup tools

pip install -r requirements.txt  # Install python dependencies

```

### TwistDB Setup

#### -- DB Option 1: 
Choose this if you don't plan to modify twistdb itself:

```
pip install -e git+ssh://git@github.com/Twistbioscience/twistdb.git@develop#egg=twistdb
```

#### -- DB Option 2: 
Switch to this approach once you start needing to make frequent / iterative changes to twistdb:

```
cd ..

git clone https://github.com/Twistbioscience/twistdb.git

cd twistdb

git checkout develop

cd ../sample_movement_tracker

pip install -e ../twistdb

```

Please merge your stable changes to twistdb@develop frequently, for others to pick up.

NOTE: keeping the various application codebases in sync with the central TwistDB codebase will likely be a challenge.

### Add TwistDB + SMT seed data

```
export WEBSITE_ENV=local

createdb orders_dev         # you might need to 'dropdb orders_dev' first

# ALSO: you might need to set up some postgres permissions here, TBD

python manage.py createdb   # initializes the new postgres database

python manage.py seed       # populates it with seed data e.g. plate types

python manage.py fixtures   # adds fixtures data e.g. test plates
```

At the current phase of development, you might need to re-seed your database multiple times per day.  See below for a one-liner script.

### Run tests

```
run_tests  # TODO: replace this with "python manage.py test"
```


# 3. Run local webserver

```
python manage.py runserver
```

## Re-run after local / remote changes:

```
git pull # TODO: how best to pull remote twistdb changes

grunt watch &  # to avoid having to run "grunt" after some git pulls

dropdb orders_dev && createdb orders_dev && python manage.py createdb && python manage.py seed && python manage.py fixtures

./run_tests
```


# Run headless tests
```
npm install -g phantomjs
grunt test
```

# Older docs

### This is a starting Flask app. 
You should be able to copy all this into a new project and get started.

### After copying, do these steps:




## 3. "npm install" node dependencies

```bash
npm install
```


## 4. run grunt

```bash
grunt
```


## 5. install all Python packages

```bash
pip install -r requirements.txt
```

## 6. (Optional). Create a database...

```bash
pg_ctl -D /usr/local/var/postgres start

psql -d postgres

create database sample_movement_tracker;
```

CONNECT TO THE DB: psql -U twister -h 10.10.21.42 twistdb




