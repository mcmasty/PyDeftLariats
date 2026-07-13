=======
History
=======

0.0.1 (2021-05-29)
------------------

* First release on PyPI.


0.0.6 (2021-05-30)
------------------
* Basic set of Text & Number matchers

1.0.0 (2021-05-30)
------------------
* Better testing and refactoring in the spirit of DRY

1.1.0 (2021-05-30)
------------------
* Adding existence logic: None, NotNone, NoneOrEmpty, NotNoneOrEmpty


1.1.3 (2021-05-30)
------------------
* Added options to convert None to int value for numeric comparisons

1.2.12 (2026-07-13)
-------------------
* Migrated packaging to uv + hatchling (PEP 621)
* Added type hints and pyrefly type checking
* CI updated to uv with Python 3.11-3.13
* Docs and badges refreshed

2.0.0 (2026-07-13)
-------------------
* **Breaking:** Match values now bind at construction time instead of being
  passed to ``is_match()``. E.g. ``EqualTo('symbol', 'OTCMKTS:FRMO').is_match(record)``
  instead of ``EqualTo('symbol').is_match('OTCMKTS:FRMO', record)``.
* **Breaking:** Every matcher now implements a uniform
  ``is_match(self, data_record: dict[str, Any]) -> bool`` signature. The
  ``# type: ignore[override]`` escapes previously needed for ``ExistsMatchers``
  and ``DictMatchers`` are gone.
* **Breaking:** Invalid input values (empty match values, an unsupported
  multi-element list for ``NumberComparer``) now raise ``ValueError`` at
  construction time instead of ``NotImplementedError`` at match time.
  Unsupported ``MatcherType`` values still raise ``NotImplementedError``,
  now at construction time.
* Added ``DataFilter`` abstract base class; ``Matcher`` now extends it.
* Added ``AnyOf``, ``AllOf``, and ``Not`` combinators for composing filters
  (logical OR, AND, and negation).
* Added explicit ``__all__`` to ``deftlariat.core``.
* ``Matcher.__eq__`` now also compares bound ``match_values``.
* Removed the no-op ``pull_val()`` indirection.

