from logging.config import dictConfig
from os import environ
from os.path import dirname, join

from logs import Logs
from mapproxy.wsgiapp import make_wsgi_app
from metrics import Metrics
from telemetry import Telemetry
from yaml import safe_load

with open('./log.yaml', 'r') as log_config_file:
    log_config = safe_load(log_config_file)

dictConfig(log_config)

tracing_enabled = environ.get('TELEMETRY_TRACING_ENABLED', 'false')

mapproxy_conf = f'{join(dirname(__file__), "config", "mapproxy.yaml")}'

application = make_wsgi_app(mapproxy_conf)
application = Metrics(application)
application = Logs(application)
application = Telemetry(application) if tracing_enabled.strip().lower() == 'true' else application
