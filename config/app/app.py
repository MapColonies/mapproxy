from logging import getLogger
from os import environ
from os.path import dirname, join
import sys
from os import path
from logging.config import fileConfig
from logs import Logs
from mapproxy.wsgiapp import make_wsgi_app
from metrics import Metrics
from traces import Traces


# Custom exception handler to log uncaught exceptions
def custom_exception_handler(exc_type, exc_value, exc_traceback):
    logger = getLogger("mapproxy")
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Set the custom exception handler
sys.excepthook = custom_exception_handler

tracing_enabled = environ.get('TELEMETRY_TRACING_ENABLED', 'false')
metrics_enabled = environ.get('TELEMETRY_METRICS_ENABLED', 'false')

fileConfig(r'/mapproxy/log.ini', {'here': path.dirname(__file__)})

mapproxy_conf = f'{join(dirname(__file__), "mapproxy.yaml")}'

application = make_wsgi_app(mapproxy_conf, reloader=False)
application = Logs(application)
application = Metrics(application) if metrics_enabled.strip().lower() == 'true' else application
application = Traces(application) if tracing_enabled.strip().lower() == 'true' else application
