.. _configuration-chapter:

=============
Configuration
=============

.. contents::
   :local:

Webapp
======

The Symbolication Service (aka Eliot) is run as worker processes by Gunicorn
which is run by Honcho.

Gunicorn configuration:

.. everett:option:: ELIOT_GUNICORN_WORKERS
   :default: "1"

   Specifies the number of gunicorn workers.

   Gunicorn docs suggest to set it to ``(2 x $num_cores) + 1``.

   https://docs.gunicorn.org/en/stable/settings.html#workers

   https://docs.gunicorn.org/en/stable/design.html#how-many-workers

   Used in `bin/run_eliot_web.sh
   <https://github.com/mozilla-services/eliot/blob/main/bin/run_eliot_web.sh>`_.


.. everett:option:: ELIOT_GUNICORN_TIMEOUT
   :default: "300"

   Specifies the timeout value.

   https://docs.gunicorn.org/en/stable/settings.html#timeout

   Used in `bin/run_eliot_web.sh
   <https://github.com/mozilla-services/eliot/blob/main/bin/run_eliot_web.sh>`_.


.. everett:option:: PORT
   :default: "8000"

   Specifies the port to listen to.

   Used in `bin/run_eliot_web.sh
   <https://github.com/mozilla-services/eliot/blob/main/bin/run_eliot_web.sh>`_.


Webapp configuration:

.. autocomponentconfig:: eliot.app.EliotApp
   :show-table:
   :hide-name:
   :namespace: ELIOT
   :case: upper


Disk cache manager
==================

The disk cache manager is run as a single process by Honcho.

.. autocomponentconfig:: eliot.cache_manager.DiskCacheManager
   :show-table:
   :hide-name:
   :namespace: ELIOT
   :case: upper
