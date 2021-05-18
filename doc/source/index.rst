
Django GraphQL JWT Flow
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Installation
============

Configuration
=============
The library is configurable by using the ``JWT_FLOW`` dictionary in your
settings file.

``KEY_FORMAT``
   The format in which the key is presented. Ignored if the key is read from
   file. Can be one of:

   * ``PEM``
   * ``JSON``
   * ``DICT``

   If not provided it is assumed to be a python dictionary.

``KEY``
   The private key if asymmetric algorithms are used and the key itself in the
   case of symmetric algorithms. The key should be exported and provided as
   value corresponding to the `KEY_FORMAT` setting.

   Ignored if `KEY_FILE` is set.

``KEY_FILE``
   A Path object or string to a file containing the key. The file extension is
   used to determine the key format.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`