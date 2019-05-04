from http import HTTPStatus
from time import time

from flask import request, Flask, Response
from prometheus_client import Counter, Histogram
from prometheus_client.registry import REGISTRY


def register_prometheus(app: Flask, registry=REGISTRY) -> None:
    """
    Automatically collect and expose metrics about HTTP calls in a Flask application.
    :param app: Instance of a Flask application.
    :param registry: Metrics registry to expose, defaults to default Prometheus registry.
    """

    counter = Counter(
        namespace="app",
        subsystem="flask",
        name="http_request",
        unit="total",
        documentation="Total number of HTTP requests handled by Flask",
        labelnames=("match", "blueprint", "endpoint", "method", "path", "status_code"),
        registry=registry,
    )

    histogram = Histogram(
        namespace="app",
        subsystem="flask",
        name="http_request_duration",
        unit="seconds",
        documentation="Time required to handle an HTTP request using Flask",
        labelnames=("match", "blueprint", "endpoint", "method", "path", "status_code"),
        registry=registry,
    )

    def before() -> None:
        request.prometheus_start_time = time()

    def after(response: Response) -> Response:
        if hasattr(request, "prometheus_start_time"):
            now = time()
            duration = now - request.prometheus_start_time
            url_rule = request.url_rule
            endpoint = request.endpoint
            status_code = response.status_code
            labels = {
                "match": url_rule is not None,
                "blueprint": request.blueprint,
                "endpoint": endpoint.replace(f"{request.blueprint}.", "") if endpoint is not None else endpoint,
                "method": request.method,
                "path": url_rule.rule if url_rule is not None else None,
                "status_code": status_code.value if isinstance(status_code, HTTPStatus) else status_code,
            }
            counter.labels(**labels).inc()
            histogram.labels(**labels).observe(duration)

        return response

    app.before_request(before)
    app.after_request(after)
