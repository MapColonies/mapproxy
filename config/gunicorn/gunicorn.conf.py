import os

bind = "0.0.0.0:8080"
accesslog="-"
loglevel = "debug"
wsgi_app = "app:application"
user=os.geteuid()
group=os.getegid()
workers=1
threads = 10
worker_class = "gevent"
