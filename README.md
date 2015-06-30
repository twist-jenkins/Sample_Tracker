# This is a starting Flask app. 
You should be able to copy all this into a new project and get started.

# After copying, do these steps:

## 1. Create a virtual enironment

```bash
virtualenv venv
source venv/bin/activate
```


## 2. Install javascript/css/font/bower dependencies - managed by bower

```bash
bower install
```


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




