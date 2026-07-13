

# Python Deft Lariats

[![PyPI Version](https://img.shields.io/pypi/v/PyDeftLariats.svg)](https://pypi.python.org/pypi/PyDeftLariats)
[![Python Versions](https://img.shields.io/pypi/pyversions/PyDeftLariats.svg)](https://pypi.python.org/pypi/PyDeftLariats)
[![Build Status](https://github.com/mcmasty/PyDeftLariats/workflows/Python%20package/badge.svg)](https://github.com/mcmasty/PyDeftLariats/actions)
[![Documentation Status](https://readthedocs.org/projects/pydeftlariats/badge/?version=latest)](https://pydeftlariats.readthedocs.io/en/latest/?version=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Using PyHamcrest to build a collection of data filters.**

"Deft Lariats" is an anagram of "Data Filters". The name pays homage to ["hamcrest"](https://github.com/hamcrest/PyHamcrest) being an anagram of "matchers", since this project heavily relies on hamcrest.

---

### **🧠 What PyDeftLariats Does**

- **Abstracts PyHamcrest matchers into field-based matchers**, allowing structured matching against dictionary-style data records (e.g., rows in a dataset or events in a stream).
- **Provides reusable, composable matchers** for specific field keys and types: text, numbers, existence, dictionaries, etc.
- **Enables rule-style matching logic** to be implemented declaratively and extensibly.

---



### Example Usage

Extract specific records from the Coingecko API using PyDeftLariats.



- assuming you have jq installed

- One Record form the Coingecko API
```
{
  "name": "Mogo Inc.",
  "symbol": "NASDAQ:MOGO",
  "country": "CA",
  "total_holdings": 18,
  "total_entry_value_usd": 595494,
  "total_current_value_usd": 391423,
  "percentage_of_total_supply": 0
}
```


- Use jq to extract the record from the Coingecko API and stream to deft
- `deft` is the command line tool for PyDeftLariats

**Goal**: return all records that match any of the following criteria:
- `symbol` is `OTCMKTS:FRMO`
- `total_holdings` is greater than or equal to `1000`
- `percentage_of_total_supply` is greater than or equal to `0.1`

how that gets created in code... the Python code for `example-coingecko` fuction is:

```python
    ...
    field_key = 'symbol'
    filter_one = EqualTo(field_key)
    target_value = 'OTCMKTS:FRMO'

    filter_two = NumberComparer('total_holdings', MatcherType.GREATER_THAN_EQUAL_TO)
    filter_three = NumberComparer('percentage_of_total_supply', MatcherType.GREATER_THAN_EQUAL_TO)
    for x in data:
        if any([filter_one.is_match(target_value, x),
                filter_two.is_match(1000, x),
                filter_three.is_match(0.1, x),
                ]):
            click.echo(f"Data Filter hit for record:\n{x}\n\n")
```

Running from the command line:


``` 
curl 'https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin' |  jq '.companies[]' | deft example-coingecko
```



## Available Matchers

### Basic Matchers
- **EqualTo** - Exact equality matching (supports lists)
- **AnythingMatcher** - Always matches (useful for testing)
- **NothingMatcher** - Never matches (default/fallback)

### Text Matchers (TextComparer)
- **STARTS_WITH** - String prefix matching
- **CONTAINS_STRING** - Substring matching
- **CONTAINS_STRING_IN_ORDER** - Multiple substrings in order
- **EQUAL_TO_IGNORE_CASE** - Case-insensitive equality
- **EQUAL_TO_IGNORE_WHITESPACE** - Whitespace-insensitive equality

### Number Matchers (NumberComparer)
- **GREATER_THAN** - Numeric comparison >
- **GREATER_THAN_EQUAL_TO** - Numeric comparison ≥
- **LESS_THAN** - Numeric comparison <
- **LESS_THAN_EQUAL_TO** - Numeric comparison ≤
- **CLOSE_TO** - Approximate equality with delta

### Existence Matchers (ExistsMatchers)
- **NONE** - Field is None
- **NOT_NONE** - Field is not None
- **NONE_OR_EMPTY** - Field is None or empty ([], {}, '', ())
- **NOT_NONE_OR_EMPTY** - Field has a value

### Dictionary Matchers (DictMatchers)
- **HAS_ENTRY** - Dictionary contains specific key-value pair
- **HAS_ENTRIES** - Dictionary contains multiple key-value pairs

---

## Installation

```bash
# Using pip
pip install PyDeftLariats

# Using uv (recommended)
uv add PyDeftLariats
```

## Requirements

- Python 3.11+
- PyHamcrest ~= 2.1.0
- Click ~= 8.2.1

---

## Documentation

Full documentation available at [https://pydeftlariats.readthedocs.io/](https://pydeftlariats.readthedocs.io/)

## Contributing

Contributions welcome! Please read [CONTRIBUTING.rst](CONTRIBUTING.rst) for details.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

## License

GNU General Public License v3 - see [LICENSE](LICENSE) file for details.
