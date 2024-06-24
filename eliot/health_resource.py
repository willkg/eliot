# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Application-health related Falcon resources.
"""

import json
import logging
import os

from eliot.libmarkus import METRICS

from dockerflow.version import get_version
import falcon


LOGGER = logging.getLogger(__name__)


class BrokenResource:
    """Handle ``/__broken__`` endpoint."""

    def on_get(self, req, resp):
        """Implement GET HTTP request."""
        METRICS.incr("pageview", tags=["path:/__broken__", "method:get"])
        # This is intentional breakage
        raise Exception("intentional exception")


class VersionResource:
    """Handle ``/__version__`` endpoint."""

    def __init__(self, basedir):
        self.basedir = basedir

    def on_get(self, req, resp):
        """Implement GET HTTP request."""
        METRICS.incr("pageview", tags=["path:/__version__", "method:get"])
        resp.status = falcon.HTTP_200
        LOGGER.info(
            "version: basedir: %s, exists?: %s",
            self.basedir,
            os.path.exists(os.path.join(self.basedir, "version.json")),
        )
        resp.text = json.dumps(get_version(self.basedir) or {})


class LBHeartbeatResource:
    """Handle ``/__lbheartbeat__`` to let the load balancing know application health."""

    def on_get(self, req, resp):
        """Implement GET HTTP request."""
        METRICS.incr("pageview", tags=["path:/__lbheartbeat__", "method:get"])
        resp.content_type = "application/json; charset=utf-8"
        resp.status = falcon.HTTP_200


class HeartbeatResource:
    """Handle ``/__heartbeat__`` for app health."""

    def on_get(self, req, resp):
        """Implement GET HTTP request."""
        METRICS.incr("pageview", tags=["path:/__heartbeat__", "method:get"])
        resp.content_type = "application/json; charset=utf-8"
        resp.status = falcon.HTTP_200
