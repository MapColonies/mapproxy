from os import environ

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased


class Traces():
    def __init__(self, app):
        self.app = app
        # Get telemetry endpoint from env
        endpoint = environ.get('TELEMETRY_TRACING_ENDPOINT', 'localhost:4317')
        sampling_ratio_denominator = int(environ.get('TELEMETRY_TRACING_SAMPLING_RATIO_DENOMINATOR', '1000'))

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
        RedisInstrumentor().instrument()
        SQLite3Instrumentor().instrument()

        # Add OpenTelemetry middleware and activate application
        self.tracing_app = OpenTelemetryMiddleware(
            self.app, None, None, tracer_provider)

    def __call__(self, environ, start_response):
        # tracer = trace.get_tracer(__name__)

        # with tracer.start_as_current_span("my_span_name"):
        #     # Your code here

        #     # You can add attributes to the span
        #     span = trace.get_current_span()
        #     span.set_attribute("custom_attribute", "attribute_value")

        #     # You can log events associated with the span
        #     span.add_event("event_name", {"event_attribute": "event_value"})

        # # The span is automatically closed when the context exits


        response = self.tracing_app(environ, start_response)
        return response
