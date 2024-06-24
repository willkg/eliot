# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Utilities for setting up markus.
"""

from dataclasses import dataclass
import logging
from pathlib import Path

import markus
from markus.filters import AddTagFilter, RegisteredMetricsFilter

import yaml


_IS_MARKUS_SET_UP = False

LOGGER = logging.getLogger(__name__)


@dataclass
class Metric:
    stat_type: str
    description: str


# Complete index of all Eliot metrics. This is used in documentation and to filter
# outgoing metrics.
def _load_registered_metrics():
    # Load the eliot_metrics.yaml file in this directory
    path = Path(__file__).parent / "eliot_metrics.yaml"
    with open(path) as fp:
        data = yaml.safe_load(fp)
    return data


ELIOT_METRICS = _load_registered_metrics()


def set_up_metrics(statsd_host, statsd_port, statsd_namespace, hostname, debug=False):
    """Initialize and configures the metrics system.

    :arg statsd_host: the statsd host to send metrics to
    :arg statsd_port: the port on the host to send metrics to
    :arg statsd_namespace: the namespace (if any) for these metrics
    :arg hostname: the host name
    :arg debug: whether or not to additionally log metrics to the logger

    """
    global _IS_MARKUS_SET_UP, METRICS
    if _IS_MARKUS_SET_UP:
        return

    markus_backends = [
        {
            "class": "markus.backends.datadog.DatadogMetrics",
            "options": {
                "statsd_host": statsd_host,
                "statsd_port": statsd_port,
                "statsd_namespace": statsd_namespace,
            },
        }
    ]
    if debug:
        markus_backends.append(
            {
                "class": "markus.backends.logging.LoggingMetrics",
                "options": {
                    "logger_name": "markus",
                    "leader": "METRICS",
                },
            }
        )
    markus.configure(markus_backends)

    if debug:
        # In local dev and test environments, we want the RegisteredMetricsFilter to
        # raise exceptions when metrics are used incorrectly.
        metrics_filter = RegisteredMetricsFilter(
            registered_metrics=ELIOT_METRICS, raise_error=True
        )
        METRICS.filters.append(metrics_filter)

    if hostname:
        # Add host tag to all metrics if the hostname is set
        # FIXME(willkg): do we need to cleanse the hostname?
        METRICS.filters.append(AddTagFilter(f"host:{hostname}"))

    _IS_MARKUS_SET_UP = True


METRICS = markus.get_metrics("eliot")
