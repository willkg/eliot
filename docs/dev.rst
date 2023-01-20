===========
Development
===========

.. contents::
   :local:


Setup quickstart
================

1. Install required software: Docker, make, and git.

   **Linux**:

       Use your package manager.

   **OSX**:

       Install `Docker for Mac <https://docs.docker.com/docker-for-mac/>`_.

       Use `homebrew <https://brew.sh>`_ to install make and git:

       .. code-block:: shell

          $ brew install make git

   **Other**:

       Install `Docker <https://docs.docker.com/engine/installation/>`_.

       Install `make <https://www.gnu.org/software/make/>`_.

       Install `git <https://git-scm.com/>`_.

2. Clone the repository so you have a copy on your host machine.

   Instructions for cloning are `on the Eliot page in GitHub
   <https://github.com/mozilla-services/eliot>`_.

3. (*Optional for Linux users*) Set UID and GID for Docker container user.

   If you're on Linux or you want to set the UID/GID of the app user that
   runs in the Docker containers, run:

   .. code-block:: shell

      $ make .env

   Then edit the file and set the ``APP_UID`` and ``APP_GID`` variables. These
   will get used when creating the app user in the base image.

   If you ever want different values, change them in ``.env`` and re-run
   ``make build``.

4. Build Docker images.

   From the root of this repository, run:

   .. code-block:: shell

      $ make build

   That will build the app Docker image required for development.


Eliot consists of a webapp and a disk cache manager.

To run Eliot, do:

.. code-block:: shell

   $ make run


The webapp is at `<http://localhost:8000>`__.

The logs its configuration at startup. You can override any of those
configuration settings in your ``.env`` file.


Bugs / Issues
=============

All bugs are tracked in `Bugzilla <https://bugzilla.mozilla.org/>`_.

Write up a new bug:

https://bugzilla.mozilla.org/enter_bug.cgi?product=Eliot

Please make sure there's a bug for any work you want to do before you do
anything. The conversations in the bug can be enlightening and flesh out
issues.


Code workflow
=============

Bugs
----

Either find a bug to work on or write up a new one.

Assign the bug to yourself.

Work out any questions about the problem, the approach to fix it, and any
additional details by posting comments in the bug comments.


Commits
-------

Commits should be self-contained and tests should pass. If there's outstanding
work to do, note that in the commit.


Pull requests
-------------

Pull request summary should indicate the bug the pull request addresses. For
example::

    bug 1797200: removed frob from tree class

Pull request descriptions should cover at least some of the following:

1. what is the issue the pull request is addressing?
2. why does this pull request fix the issue?
3. how should a reviewer review the pull request?
4. what did you do to test the changes?
5. any steps-to-reproduce for the reviewer to use to test the changes

After creating a pull request, attach the pull request to the relevant bugs.

We use the `rob-bugson Firefox addon
<https://addons.mozilla.org/en-US/firefox/addon/rob-bugson/>`_. If the pull
request has "bug nnnnnnn: ..." in the summary, then rob-bugson will see that
and create a "Attach this PR to bug ..." link.

Then ask someone to review the pull request. If you don't know who to ask, look
at other pull requests to see who's currently reviewing things.


Code reviews
------------

Pull requests should be reviewed before merging.

Style nits should be covered by linting as much as possible.

Code reviews should review the changes in the context of the rest of the
system.


Landing code
------------

Once the code has been reviewed and all tasks in CI pass, the pull request
author should merge the code.

This makes it easier for the author to coordinate landing the changes with
other things that need to happen like landing changes in another repository,
data migrations, configuration changes, and so on.

We use "Rebase and merge" in GitHub.


Conventions
===========

Git conventions
---------------

First line is a summary of the commit. It should start with::

  bug nnnnnnn: summary


After that, the commit should explain *why* the changes are being made and any
notes that future readers should know for context or be aware of.


Python code conventions
-----------------------

All Python code files should have an MPL v2 header at the top::

  # This Source Code Form is subject to the terms of the Mozilla Public
  # License, v. 2.0. If a copy of the MPL was not distributed with this
  # file, You can obtain one at http://mozilla.org/MPL/2.0/.


We use `black <https://black.readthedocs.io/en/stable/>`_ to reformat Python
code.


To lint all the code, do:

.. code-block:: bash

  $ make lint


To reformat all the code, do:

.. code-block:: bash

  $ make lintfix


HTML/CSS conventions
--------------------

2-space indentation.


Javascript code conventions
---------------------------

2-space indentation.

All JavaScript code files should have an MPL v2 header at the top::

  /*
   * This Source Code Form is subject to the terms of the Mozilla Public
   * License, v. 2.0. If a copy of the MPL was not distributed with this
   * file, You can obtain one at http://mozilla.org/MPL/2.0/.
   */


Managing dependencies
=====================

Python dependencies are maintained in the ``requirements.in`` file and
"compiled" with hashes and dependencies of dependencies in the
``requirements.txt`` file.

To add a new dependency, add it to the file and then do:

.. code-block:: shell

   $ make rebuildreqs

Then rebuild your docker environment:

.. code-block:: shell

  $ make build

If there are problems, it'll tell you.

In some cases, you might want to update the primary and all the secondary
dependencies. To do this, run:

.. code-block:: shell

   $ make updatereqs


Configuration
=============

Configuration is managed using `everett <https://everett.readthedocs.io/>`__.

See :ref:`configuration-chapter` for Eliot configuration.


Metrics
=======

Metrics are emitted using `markus <https://markus.readthedocs.io/>`__.

Metrics are listed in ``eliot/libmarkus.py``. These can then be used anywhere
in the codebase.

.. code-block:: python

   from eliot.libmarkus import METRICS

and then:

.. code-block:: python

   METRICS.histogram("eliot.symbolicate.frames_count", value=len(frames))


See :ref:`metrics-chapter` for list of metrics emitted by Eliot.


Documentation
=============

Documentation for Eliot is build with `Sphinx <http://www.sphinx-doc.org/>`__
and is available on ReadTheDocs at `<https://mozilla-eliot.readthedocs.io/>`__.

To build the docs, do:

.. code-block:: shell

  $ make docs

Then view ``docs/_build/html/index.html`` in your browser.


Testing
=======

Eliot's tests use the `pytest <https://pytest.org/>`__ test framework.

To run all the tests, do:

.. code-block:: shell

   $ make test

Tests for the Symbolication Service webapp go in ``tests/``.

If you need to run specific tests or pass in different arguments, you can use
the testshell:

.. code-block:: shell

   $ make testshell
   app@xxx:/app$ pytest

   <pytest output>

   app@xxx:/app$ pytest tests/test_app.py

   <pytest output>
