from logging.config import dictConfig
from logging import getLogger
from os import environ
from os.path import dirname, join
import sys

from logs import Logs
from mapproxy.wsgiapp import make_wsgi_app
from metrics import Metrics
from traces import Traces
from yaml import safe_load

with open(f'{join(".", "settings", "log.yaml")}', 'r') as log_config_file:
    log_config = safe_load(log_config_file)

dictConfig(log_config)

# Custom exception handler to log uncaught exceptions
def custom_exception_handler(exc_type, exc_value, exc_traceback):
    logger = getLogger("mapproxy")
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Set the custom exception handler
sys.excepthook = custom_exception_handler

tracing_enabled = environ.get('TELEMETRY_TRACING_ENABLED', 'false')
metrics_enabled = environ.get('TELEMETRY_METRICS_ENABLED', 'false')

mapproxy_conf = f'{join(dirname(__file__), "mapproxy.yaml")}'

application = make_wsgi_app(mapproxy_conf, reloader=True)
application = Logs(application)
application = Metrics(application) if metrics_enabled.strip().lower() == 'true' else application
application = Traces(application) if tracing_enabled.strip().lower() == 'true' else application
