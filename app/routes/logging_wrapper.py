

import functools

import logging


import inspect


class Proxy(object):
    """The Proxy base class."""

    def __init__(self, obj):
        """The initializer."""
        super(Proxy, self).__init__()
        #Set attribute.
        self._obj = obj
        
    def __getattr__(self, attrib):
        m = getattr(self._obj, attrib)
        if attrib in ["debug","info","warning","error","critical","exception"]:
            def wrapper(*args,**kwargs):
                # do stuf here
                #args(0) = "SCOTT: " + args[0]
                #x = "Scott " + args[0]

                (frame, filename, line_number,
                    function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

                x = "(line: " + str(line_number) + ") " + args[0]
                #print "ARGS: ", args 
                #print "kw args: ", kwargs
                return m(x,*args[1:],**kwargs)
            return wrapper
        else:
            return m

def get_logger(logger_name):
    logger = Proxy(logging.getLogger(logger_name))
    #logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    #logger = Proxy(logger)
    return logger 

