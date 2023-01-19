========
Overview
========

.. contents::
   :local:


What is Eliot?
==============

Eliot is the Mozilla Symbolication Server which has a symbolication API for
converting memory addresses into symbols (:ref:`symbolication
<symbolication>`).


Architecture
============

Rough architecture diagram of Eliot:

FIXME: redo this

.. image:: drawio/tecken_architecture.drawio.png
   :alt: Tecken architecture diagram


**Sybmolication service (aka symbolication.services.mozilla.com):**

Host: https://symbolication.services.mozilla.com/

The symbolication webapp is a symbolication API microservice that uses the `Symbolic
library <https://github.com/getsentry/symbolic>`_ to parse SYM files and do
symbol lookups.

Code is at `<https://github.com/mozilla-services/eliot>`__.


Repository structure
====================

Here's a bunch of top-level directories and what's in them::

    bin/               -- scripts for running and developing
    docker/            -- Dockerfile and image building bits
    docs/              -- documentation
    schemas/           -- API schemas
    eliot/             -- Symbolication service unit tests and code (Eliot)


.. Note::

   Originally, there was just Tecken which handled upload, download, and
   symbolication. Then we split symbolication into a separate service
   codenamed Eliot [#eliotname]_, but it was in the tecken repository. Then
   we split it out as a completely separate project.

   .. [#eliotname] Tecken Symoblication -> TS Eliot.
