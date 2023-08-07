from prometheus_client import make_wsgi_app as make_prometheus_wsgi_app

# uncomment to remove default collector metrics
# import prometheus_client
# prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
# prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
# prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

class Metrics():
    def __init__(self, app):
        self.app = app
        self.metrics_app = make_prometheus_wsgi_app()
    
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/metrics':
            response = self.metrics_app(environ, start_response)
            return response
        response = self.app(environ, start_response)
        return response
