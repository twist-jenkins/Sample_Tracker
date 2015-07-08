
######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: runserver.py
#
# This is used to run the server locally for development when you want the server listening
# on part 80.
# 
######################################################################################



from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)