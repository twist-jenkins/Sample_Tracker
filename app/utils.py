import os
from contextlib import contextmanager
__author__ = "Ryan Johnson"
__version_info__ = ('0', '0', '8')
__version__ = '.'.join(__version_info__)
__module_name__ = 'hitpicking-utils-' + __version__


def char2num(val):
    """
    Convert the given unicode character into an integer.
    """
    if isinstance(val, int):
        return val

    if not isinstance(val, unicode):
        raise ValueError('invalid argument: {!r}'.format(val))

    val = val.upper()

    if not ((ord(val) >= ord(u'A')) and (ord(val) <= ord(u'Z'))):
        raise ValueError('invalid argument: {!r}'.format(val))

    return (ord(val) - ord(u'A')) + 1


def num2char(val):
    """
    Convert the given integer into a unicode character.
    """
    if isinstance(val, unicode):
        return val

    if not (isinstance(val, int) and (val >= 1) and (val <= 26)):
        raise ValueError('invalid argument: {!r}'.format(val))

    return unichr(ord(u'A') + (val - 1))


def chunked(iterable, size):
    """
    Breaks the iterable into lists of length "size".
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def get_path(output_dir, filename, default):
    if output_dir and not os.path.exists(output_dir):
        # Try to make the output directory if it doesn't already exist.
        try:
            os.makedirs(output_dir)
        except os.error:
            pass

    if not output_dir:
        output_dir = os.getcwd()

    if not filename:
        filename = default

    return os.path.join(output_dir, filename)


def write_delimited(filename, data, delimiter='\t'):
    rows = data['rows']
    headers = data['headers']
    with open(filename, 'w') as f:
        f.write(delimiter.join(h for h in headers) + '\n')
        for row in rows:
            f.write(delimiter.join('{!s}'.format(i) for i in row) + '\n')


def json_api_success(data, status_code, headers=None):
    json_api_response = {"data": data,
                         "errors": [],
                         "meta": {}
                         }
    if headers is None:
        return json_api_response, status_code
    else:
        return json_api_response, status_code, headers


# TODO:
# def json_api_error(err_list, status_code, headers=None):
#     json_api_response = {"data": {},
#                          "errors": err_list,
#                          "meta": {}
#                          }
#     if headers is None:
#         return json_api_response, status_code
#     else:
#         return json_api_response, status_code, headers


cached_session_factory = None


def get_session_factory(db_engine=None):
    global cached_session_factory

    if cached_session_factory:
        return cached_session_factory

    from sqlalchemy.orm import sessionmaker

    if not db_engine:
        import sqlalchemy as SA
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise RuntimeError('no database URL provided')
        db_engine = SA.create_engine(db_url, echo=False)

    Session = sessionmaker(bind=db_engine)
    cached_session_factory = Session

    return cached_session_factory


@contextmanager
def scoped_session(db_engine=None):
    """
    Provide a transactional scope around a series of operations.
    """
    session = get_session_factory(db_engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
