===============
We Have We Need
===============

Overview
========

This is the code behind the `We Have We Need <http://wehaveweneed.org>`_ website
and API. We Have We Need is a platform where relief organizations can quickly
post their most urgent needs and have them matched by generous donors during a
time of crisis. The site was built by a group of geeky do-gooders who saw this
as an opportunity to use technology to help bring people and donations together
in the aftermath of a devastating earthquake in Haiti.

This code is made available under a BSD-style license (see the `LICENSE` file).
A `mailing list <http://groups.google.com/group/wehave_weneed>`_ exists for development discussion.
The code is hosted on `GitHub <http://github.com/wehaveweneed/wehaveweneed>`_.

Requirements
============

We Have We Need is written in Python using Django framework. A pip requirements.txt
file is include in the project. If you do not have pip, use requirements.txt as a
guide for the packages that need to be installed.

Run We Have We Need From Scratch
================================

This section explains how to setup this application on a clean Ubuntu install.

---------------------------
Install system dependencies
---------------------------
::

    sudo apt-get update
    sudo apt-get install git-core python-setuptools mercurial python-psycopg2 memcached python-memcache

--------------------------
Install PIP and virtualenv
--------------------------
::

    sudo easy_install pip
    sudo pip install virtualenv

--------------------------
Create virtual environment
--------------------------
::

    python virtualenv.py virt-wehaveweneed

-----------------------
Install Python packages
-----------------------

Now that you have `pip <http://pypi.python.org/pypi/pip>`_ installed, you should
be able to install all of We Have We Need's Python dependencies
with a single command::

    pip install -E virt-wehaveweneed -r requirements.txt

This command installs all required packages into the We Have We Need virtual environment.

----------------------
Grab the latest source
----------------------
::

    get clone http://github.com/wehaveweneed/wehaveweneed.git

-----------------------
Get Application Running
-----------------------
::

    source wehaveweneed-virt/bin/activate
    cd wehaveweneed

In order to run the application, you must first customize the Django settings
to your specific configuration. Please refer to the `Settings` section.

If you are using SQLite as your database, just run syncdb::

    python manage.py syncdb

Go ahead and say yes to create an admin account on your development machine.
Now you are ready to run the development server::

    python manage runserver

The app is now running and is available on localhost: http://127.0.0.1:8000/

Settings
========

Copy the `local_settings.example.py` file to `local_settings.py` and configure
the included settings. The django documentation
`explains <http://docs.djangoproject.com/en/dev/ref/settings/>`_
the meaning of most of these settings.


Production Deployment
=====================

For production deployment we recommend using
`PostgresSQL <http://www.postgresql.org/>`_ as the database and
`Apache Solr <http://lucene.apache.org/solr/>`_ for the search backend.


API Examples
============

WeNeed API Examples!


HELP
=====
We Have We Need

Overview
This is the code behind the We Have We Need website and API. We Have We Need
is a platform where relief organizations can quickly post their most urgent
needs and have them matched by generous donors during a time of crisis. The
site was built by a group of geeky do-gooders who saw this as an opportunity
to use technology to help bring people and donations together in the aftermath
of a devastating earthquake in Haiti.

This code is made available under a BSD-style license (see the LICENSE file).
A mailing list exists for development discussion. The code is hosted on GitHub.
Requirements
We Have We Need is written in Python.

Installing Required Components – Database, Database Encryption, Web Server:
We Have We Need can be developed and tested without any further external
dependencies. For production deployments, however, PostgresSQL and Apache Solr
are recommended.







Installing PostgresSQL:
=======================

Install Postgress:
    sudo apt-get install postgresQL postgresQL-client postgresQL-contrib postgresQL-plpython-[version number] 

Change DB settings to 'postgresql_psycopg2' settings file:
    DATABASE_ENGINE = 'postgresql_psycopg2'



Create the db
    createdb crisis
    
Now syncdb and restart server.

    python manage.py syncdb
    python manage runserver
