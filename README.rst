Colab Super Archives Plugin
===========================

.. image:: https://travis-ci.org/colab/colab-superarchives-plugin.svg?branch=master
    :target: https://travis-ci.org/colab/colab-superarchives-plugin

.. image:: https://coveralls.io/repos/github/colab/colab-superarchives-plugin/badge.svg?branch=master
    :target: https://coveralls.io/github/colab/colab-superarchives-plugin?branch=master


Additional Configuration
------------------------

You should add the following in the ``/etc/colab/settings.d/super_archives.py`` configuration file or the ``/etc/colab/settings.py``

.. code-block:: python

    SUPER_ARCHIVES_PATH = '/var/lib/mailman/archives/private'
    SUPER_ARCHIVES_EXCLUDE = []
    SUPER_ARCHIVES_LOCK_FILE = '/var/lock/colab/import_emails.lock'
