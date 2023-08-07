from os import environ

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased


class Telemetry():
    def __init__(self, app):
        self.app = app
        # Get telemetry endpoint from env
        endpoint = environ.get('TELEMETRY_ENDPOINT', 'localhost:4317')
        sampling_ratio_denominator = int(environ.get('TELEMETRY_SAMPLING_RATIO_DENOMINATOR', '1000'))

        # Create span exporter
        span_exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)

        # sample 1 in every n traces
        sampler = TraceIdRatioBased(1 / sampling_ratio_denominator)

        # Set trance provider and processor
        tracer_provider = TracerProvider(sampler=sampler)
        trace.set_tracer_provider(tracer_provider)
        processor = SimpleSpanProcessor(span_exporter)
        tracer_provider.add_span_processor(processor)

        # Activate instruments
        # LoggingInstrumentor().instrument(set_logging_format=True)
        BotocoreInstrumentor().instrument()
        SQLite3Instrumentor().instrument()

        # Add OpenTelemetry middleware and activate application
        self.tracing_app = OpenTelemetryMiddleware(
            self.app, None, None, tracer_provider)

    def __call__(self, environ, start_response):
        response = self.tracing_app(environ, start_response)
        return response
