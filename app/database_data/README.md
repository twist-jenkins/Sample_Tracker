These files are genereated using the "import_sample_transfer_template" script. That 
script should be run against an XML file describing the template. It generates the
".py" file. You then drop the .py file into this package and then create a new
alembic migration that will import the template into the database.