# Sample Tracker

![SampleTracker logo](http://yt3.ggpht.com/-7tic0TpPpeI/AAAAAAAAAAI/AAAAAAAAAAA/bApALLkNBPM/s88-c-k-no/photo.jpg)

A sample tracking webapp based on Flask, Angular, and Python 2.7.

&copy; 2016 Twist Bioscience.



## Frontend Setup

```
# Install javascript/css/font/bower dependencies - managed by bower

bower install

# Install node dependencies

npm install

# run grunt 

grunt
```

If you run 
```grunt watch```
instead of ```grunt``` you'll pick up changes.

## Backend Setup

### Initial Setup -- one-time:

```
# Create a Python virtual environment

virtualenv venv
source venv/bin/activate
pip install -U setuptools pip

# Install python dependencies

pip install -r requirements.txt

```

### Set your dev database target:

Choose "local" for locally installed postgres (faster) or "dev" to hit the dev database (easier).

```
export WEBSITE_ENV=local  # or
export WEBSITE_ENV=dev  # or
export WEBSITE_ENV=warp1staging

```

### TwistDB Setup -- Option 1:

Rerun this as needed to pick up others' changes to twistdb develop branch:

```
pip install -e git+ssh://git@github.com/Twistbioscience/twistdb.git@develop#egg=twistdb
```

### TwistDB Setup -- Option 2:

Choose this alternative if you need to make iterative changes to twistdb:

```
pip uninstall twistdb
cd ..
git clone twistdb
cd -
export PYTHONPATH=../twistdb
```

Please merge your stable changes to twistdb@develop early & often, for others to pick up.

### Add TwistDB + SMT seed data

```
python manage.py seed
```

### Run tests

```
python run_tests # FIXME
```



# open http://localhost:8000


# Run headless tests
npm install -g phantomjs
grunt test
```

# This is a starting Flask app. 
You should be able to copy all this into a new project and get started.

# After copying, do these steps:




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




