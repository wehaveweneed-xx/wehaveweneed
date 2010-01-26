===============
We Have We Need
===============

Overview
========

This is the code behind the `We Have We Need <http://wehaveweneed.org>`_ website and API. We Have We Need is a platform where relief organizations can quickly post their most urgent needs and have them matched by generous donors during a time of crisis. The site was built by a group of geeky do-gooders who saw this as an opportunity to use technology to help bring people and donations together in the aftermath of a devastating earthquake in Haiti.

This code is made available under a BSD-style license (see the `LICENSE` file). A `mailing list <http://groups.google.com/group/wehave_weneed>`_ exists for development discussion. The code is hosted on `GitHub <http://github.com/wehaveweneed/wehaveweneed>`_.

Requirements
============

We Have We Need is written in Python. It depends on a number of external Python libraries which are listed in the `requirements.txt` file. If you have `pip <http://pypi.python.org/pypi/pip>`_ installed, you can install all of We Have We Need's Python dependencies with a single command:

   ``pip install -r requirements.txt``

We Have We Need can be developed and tested without any further external dependencies. For production deployments, however, `PostgresSQL <http://www.postgresql.org/>`_ and `Apache Solr <http://lucene.apache.org/solr/>`_ are recommended.

Usage
=====

Copy the `local_settings.py.example` file to `local_settings.py` and configure the included settings. The django documentation `explains <http://docs.djangoproject.com/en/dev/ref/settings/>`_ the meaning of most of these settings.