===================
Python Deft Lariats
===================


.. image:: https://img.shields.io/pypi/v/PyDeftLariats.svg
        :target: https://pypi.python.org/pypi/PyDeftLariats
        :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/PyDeftLariats.svg
        :target: https://pypi.python.org/pypi/PyDeftLariats
        :alt: Python Versions

.. image:: https://github.com/mcmasty/PyDeftLariats/workflows/Python%20package/badge.svg
        :target: https://github.com/mcmasty/PyDeftLariats/actions
        :alt: Build Status

.. image:: https://readthedocs.org/projects/pydeftlariats/badge/?version=latest
        :target: https://pydeftlariats.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
        :target: https://www.gnu.org/licenses/gpl-3.0
        :alt: License


Using PyHamcrest to build a collection of data filters.

"Deft Lariats" is an anagram of "Data Filters". The name pays homage to
`"hamcrest" <https://github.com/hamcrest/PyHamcrest>`_ being an anagram of "matchers", since this project heavily
relies on hamcrest.

The project wraps hamcrest matchers to use as declarative, composable data filters for dictionary-style records.


* Free software: GNU General Public License v3
* Documentation: https://pydeftlariats.readthedocs.io/
* Source Code: https://github.com/mcmasty/PyDeftLariats


Features
--------

* **Field-based matching**: Match on specific dictionary keys with type-aware matchers
* **Composable filters**: Combine multiple matchers for complex filtering logic
* **CLI tool**: ``deft`` command-line interface for streaming data filtering
* **Multiple matcher types**:

  * Text: ``EqualTo``, ``StartsWith``, ``ContainsString``, case-insensitive matching
  * Numeric: ``GreaterThan``, ``LessThan``, ``CloseTo`` with optional null handling
  * Existence: ``None``, ``NotNone``, ``NoneOrEmpty`` checks
  * Dictionary: ``HasEntry``, ``HasEntries`` for nested structure matching

* **Type hints**: Full type annotation support for better IDE experience
* **Well-tested**: Comprehensive unittest suite


Quick Example
-------------

.. code-block:: python

    from deftlariat import EqualTo, NumberComparer, MatcherType

    # Create matchers
    symbol_filter = EqualTo('symbol')
    holdings_filter = NumberComparer('total_holdings', MatcherType.GREATER_THAN_EQUAL_TO)

    # Apply to data records
    data_record = {
        'symbol': 'NASDAQ:AAPL',
        'total_holdings': 1500
    }

    if symbol_filter.is_match('NASDAQ:AAPL', data_record):
        print("Symbol matches!")

    if holdings_filter.is_match(1000, data_record):
        print("Holdings above threshold!")


Installation
------------

.. code-block:: bash

    pip install PyDeftLariats

    # Or with uv
    uv add PyDeftLariats


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
