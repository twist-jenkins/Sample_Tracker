from functools import wraps

from sqlalchemy.exc import DBAPIError

from time import sleep 

from .. import db

import logging

from logging_wrapper import get_logger
logger = get_logger(__name__)


DATABASE_RETRIES_MAX = 2

def retry_after_database_error(f):
    """
    Add this to methods that hit the database. It looks for the exceptions you'd expect from a db whose connection died. 
    It retries DATABASE_RETRIES_MAX times (that is it tries once then will "RETRY" DATABASE_RETRIES_MAX more times) if 
    there is an error. This allows SQLAlchemy to recover the connection.

    See this link (even tho SQLAlchemy detects and recovers from errors, it will throw execptions, we are hiding those
    from the rest of the app here. See "Disconnect Handling" section): http://docs.sqlalchemy.org/en/rel_1_0/core/pooling.html
    """
    @wraps(f)
    def wrapped(*args, **kwargs):

        database_retries = 0

        while database_retries < DATABASE_RETRIES_MAX:
            try:
                r = f(*args, **kwargs)
                return r
            except DBAPIError as exc:
                logger.error("Duoh! Another database error. Rolling back transaction")
                logger.error(exc) 
                #
                # Doing this because SQLAlchemy barfs it we are in a transaction and it tries to retry a database call.
                #
                db.session.rollback()
                logger.error("Rolled back")
            except:
                raise 

            # Try again!
            database_retries += 1
            logger.error("Trying database again. Retry # " + str(database_retries))

            #sleep(5)

        raise 

    return wrapped
