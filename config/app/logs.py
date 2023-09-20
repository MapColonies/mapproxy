from datetime import datetime
from time import gmtime

import uwsgi
from pythonjsonlogger import jsonlogger


def get_current_formatted_time(datefmt='%Y-%m-%dT%H:%M:%S'):
    time_stamp = datetime.now().timestamp()
    date_time = datetime.fromtimestamp(time_stamp)
    return date_time.strftime(datefmt)

class Logs():
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        uwsgi.set_logvar('timestamp', get_current_formatted_time())
        response = self.app(environ, start_response)
        return response

# use existing lib or utilize cookbook json example
class CustomJSONFormatter(jsonlogger.JsonFormatter):
    def __init__(self, format, rename_fields, datefmt=None):
        jsonlogger.JsonFormatter.__init__(self, format, rename_fields=rename_fields, datefmt=datefmt)
        self.converter = gmtime
    
    def formatTime(self, record, datefmt=None):
        timestamp = datetime.fromtimestamp(record.created)
        if datefmt:
            return timestamp.strftime(datefmt)
        return timestamp.isoformat(timespec='milliseconds')

