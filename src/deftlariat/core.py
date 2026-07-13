"""Main module."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Any

from hamcrest import (
    all_of,
    any_of,
    anything,
    close_to,
    contains_string,
    equal_to,
    equal_to_ignoring_case,
    equal_to_ignoring_whitespace,
    greater_than,
    greater_than_or_equal_to,
    has_entries,
    has_entry,
    has_item,
    is_not,
    less_than,
    less_than_or_equal_to,
    match_equality,
    none,
    not_none,
    starts_with,
    string_contains_in_order,
)
from hamcrest.core.matcher import Matcher as HamcrestMatcher

__all__ = [
    "MatcherType",
    "DataFilter",
    "Matcher",
    "NothingMatcher",
    "AnythingMatcher",
    "EqualTo",
    "TextComparer",
    "NumberComparer",
    "ExistsMatchers",
    "DictMatchers",
    "AnyOf",
    "AllOf",
    "Not",
]


class MatcherType(Enum):
    NOTHING = 'Nothing'
    ANYTHING = 'Anything'
    EQUAL_TO = 'EqualTo'
    STARTS_WITH = 'StartsWith'
    CONTAINS_STRING = 'ContainsString'
    CONTAINS_STRING_IN_ORDER = 'ContainsStringInOrder'
    EQUAL_TO_IGNORE_CASE = 'EqualToIgnoreCase'
    EQUAL_TO_IGNORE_WHITESPACE = 'EqualToIgnoreWhitespace'
    GREATER_THAN = 'GreaterThan'
    GREATER_THAN_EQUAL_TO = 'GreaterThanEqualTo'
    LESS_THAN = 'LessThan'
    LESS_THAN_EQUAL_TO = 'LessThanEqualTo'
    CLOSE_TO = 'CloseTo'
    NONE = 'None'
    NONE_OR_EMPTY = 'NoneOrEmpty'
    NOT_NONE = 'NotNone'
    NOT_NONE_OR_EMPTY = 'NotNoneOrEmpty'
    HAS_ENTRY = 'HasEntry'
    HAS_ENTRIES = 'HasEntries'


class DataFilter(ABC):
    """Anything that can decide whether a data record matches."""

    @abstractmethod
    def is_match(self, data_record: dict[str, Any]) -> bool:
        """Check if the data record matches."""
        pass


class Matcher(DataFilter):
    """Abstract base class for all field-key matchers."""

    matcher_type: MatcherType
    match_col_key: str
    my_logger: logging.Logger
    match_values: Any

    def __init__(self, match_col_key: str) -> None:
        self.matcher_type = MatcherType.NOTHING
        self.match_col_key = match_col_key
        self.my_logger = logging.getLogger(__name__)
        # Concrete subclasses that bind values at construction time will
        # overwrite this; matchers with no bound values (e.g. ExistsMatchers,
        # AnythingMatcher, NothingMatcher) leave it as None.
        self.match_values = None

    @abstractmethod
    def is_match(self, data_record: dict[str, Any]) -> bool:
        """Check if the data record matches the bound match values."""
        pass

    def validate_key_exists(self, data_record: dict[str, Any]) -> bool:
        """Validate match-key-column exists in data record."""
        if self.match_col_key not in data_record:
            self.my_logger.debug("'%s' not present in data record; matcher will return False", self.match_col_key)
            return False
        else:
            return True

    def get_key_val(self) -> tuple[str, str]:
        """Generate a value suitable for hashing, dictionary key."""
        return (self.matcher_type.value, self.match_col_key)

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}('
                f'{self.matcher_type!r}, {self.match_col_key!r})')

    def __str__(self) -> str:
        return (f'Matcher for {self.matcher_type.value!r} '
                f'matching on field {self.match_col_key!r}')

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            return (self.matcher_type, self.match_col_key, self.match_values) == \
                (other.matcher_type, other.match_col_key, other.match_values)  # type: ignore
        else:
            return NotImplemented

    # Hash intentionally ignores match_values: it's a coarser key than
    # equality (class, matcher_type, match_col_key), but that's fine for
    # the hash/eq contract -- objects that are __eq__ always share this
    # same subset of fields, so equal objects still hash equal.
    def __hash__(self) -> int:
        return hash((self.__class__, self.matcher_type, self.match_col_key))


class NothingMatcher(Matcher):
    """Matcher never successfully matches any input. Always returns False."""

    def __init__(self, match_col_key: str) -> None:
        super().__init__(match_col_key)
        self.matcher_type = MatcherType.NOTHING

    def is_match(self, data_record: dict[str, Any]) -> bool:
        self.my_logger.info("No Matcher set, defaults to Nothing Matcher. Always False.")
        return False


class AnythingMatcher(Matcher):
    """Matcher always successfully matches any input. Always returns True."""

    my_matcher: HamcrestMatcher[Any]

    def __init__(self, match_col_key: str) -> None:
        super().__init__(match_col_key)
        self.matcher_type = MatcherType.ANYTHING
        self.my_matcher = anything(f"Anything for {match_col_key}")

    def is_match(self, data_record: dict[str, Any]) -> bool:
        return match_equality(self.my_matcher) == data_record


class EqualTo(Matcher):
    """Equal To matching style. Cast everything to str."""

    def __init__(self, match_col_key: str, match_values: Any) -> None:
        super().__init__(match_col_key)
        self.matcher_type = MatcherType.EQUAL_TO

        if isinstance(match_values, list | tuple | str | dict | set) and len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, raising Error")
            raise ValueError("Cannot use Equal To to check for empty "
                              "string. Use None or Not_None.")

        self.match_values = match_values

    def is_match(self, data_record: dict[str, Any]) -> bool:
        if not self.validate_key_exists(data_record):
            return False

        match_values = self.match_values

        if isinstance(match_values, list):
            if len(match_values) == 1 and not isinstance(data_record[self.match_col_key], list):
                q_match_values = match_values[0]
                return (match_equality(equal_to(q_match_values))
                        == data_record[self.match_col_key])

            else:
                # has_item will iterate a sequence ...
                if isinstance(data_record[self.match_col_key], list):
                    check_list = []
                    for dr in data_record[self.match_col_key]:
                        check_list.append(match_equality(
                            has_item(equal_to(dr))) == list(match_values))
                    return any(check_list)
                else:
                    return (match_equality(
                        has_item(equal_to(data_record[self.match_col_key]))) == list(match_values))
        else:
            return (match_equality(equal_to(match_values))
                    == data_record[self.match_col_key])


class TextComparer(Matcher):
    """Text comparison matcher for string operations."""

    my_matcher: Callable[..., HamcrestMatcher[Any]]

    _MATCHER_FUNCS: dict[MatcherType, Callable[..., HamcrestMatcher[Any]]] = {
        MatcherType.STARTS_WITH: starts_with,
        MatcherType.CONTAINS_STRING: contains_string,
        MatcherType.CONTAINS_STRING_IN_ORDER: string_contains_in_order,
        MatcherType.EQUAL_TO_IGNORE_CASE: equal_to_ignoring_case,
        MatcherType.EQUAL_TO_IGNORE_WHITESPACE: equal_to_ignoring_whitespace,
    }

    def __init__(self, match_col_key: str, matcher_type: MatcherType, match_values: Any) -> None:
        super().__init__(match_col_key)

        my_matcher = self._MATCHER_FUNCS.get(matcher_type)
        if my_matcher is None:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")
        self.matcher_type = matcher_type
        self.my_matcher = my_matcher

        if isinstance(match_values, list | tuple | str | dict | set) and len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, raising Error")
            raise ValueError(f"Cannot use {self.matcher_type.value} to check for "
                              "empty string. Use None or Not_None.")

        self.match_values = match_values

    def is_match(self, data_record: dict[str, Any]) -> bool:

        if not self.validate_key_exists(data_record):
            return False

        match_values = self.match_values

        if isinstance(match_values, list):

            if len(match_values) == 1:
                q_match_values = match_values[0]
                return (match_equality(self.my_matcher(q_match_values))
                        == str(data_record[self.match_col_key]))
            else:
                matches_list = [q for q in match_values
                                if match_equality(self.my_matcher(q))
                                == str(data_record[self.match_col_key])]
                return len(matches_list) > 0
        else:
            return (match_equality(self.my_matcher(str(match_values)))
                    == str(data_record[self.match_col_key]))


class NumberComparer(Matcher):
    """Numerical comparison matcher for numeric operations."""

    my_matcher: Callable[..., HamcrestMatcher[Any]]
    convert_none: bool
    replacement_val: int | float | None

    _MATCHER_FUNCS: dict[MatcherType, Callable[..., HamcrestMatcher[Any]]] = {
        MatcherType.GREATER_THAN: greater_than,
        MatcherType.GREATER_THAN_EQUAL_TO: greater_than_or_equal_to,
        MatcherType.LESS_THAN: less_than,
        MatcherType.LESS_THAN_EQUAL_TO: less_than_or_equal_to,
        MatcherType.CLOSE_TO: close_to,
    }

    def __init__(self, match_col_key: str, matcher_type: MatcherType, match_values: Any,
                 convert_none_to: int | float | None = None) -> None:
        super().__init__(match_col_key)
        self.replacement_val = None
        if convert_none_to is None:
            self.convert_none = False
        else:
            self.convert_none = True
            self.replacement_val = convert_none_to

        my_matcher = self._MATCHER_FUNCS.get(matcher_type)
        if my_matcher is None:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")
        self.matcher_type = matcher_type
        self.my_matcher = my_matcher

        cls_name = self.__class__.__name__

        # Special validation for CLOSE_TO: must be a (value, delta) pair
        if matcher_type == MatcherType.CLOSE_TO:
            if isinstance(match_values, list | tuple):
                if len(match_values) != 2:
                    raise ValueError("CLOSE_TO requires a (value, delta) pair")
                # Normalize to tuple
                match_values = tuple(match_values)
            else:
                raise ValueError("CLOSE_TO requires a (value, delta) pair")
            self.match_values = match_values
        elif isinstance(match_values, list):
            if len(match_values) == 0:
                self.my_logger.warning("No Match Values provided, raising Error")
                raise ValueError(fr"Cannot use {cls_name} to check for "
                                  "empty string. Use None or Not_None.")
            elif len(match_values) == 1:
                match_values = match_values[0]
            else:
                raise ValueError(fr"Cannot use {cls_name} to check "
                                  " a list of values")
            self.match_values = match_values
        else:
            self.match_values = match_values

    def get_record_value(self, data_record: dict[str, Any]) -> int | float:
        """If you want to convert a None to an Int, set a replacement value."""
        if self.convert_none and data_record[self.match_col_key] is None:
            return_val = self.replacement_val
        else:
            return_val = data_record[self.match_col_key]
        return return_val  # type: ignore

    def is_match(self, data_record: dict[str, Any]) -> bool:
        if not self.validate_key_exists(data_record):
            return False

        test_val = self.get_record_value(data_record)

        if self.matcher_type == MatcherType.CLOSE_TO:
            # Expect a tuple for Close To for Num, Delta...so unpack values
            return (match_equality(self.my_matcher(*self.match_values))
                    == test_val)
        else:
            return (match_equality(self.my_matcher(self.match_values))
                    == test_val)

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            return ((self.matcher_type, self.match_col_key, self.match_values,
                     self.convert_none, self.replacement_val) ==
                    (other.matcher_type, other.match_col_key, other.match_values,  # type: ignore
                     other.convert_none, other.replacement_val))  # type: ignore
        else:
            return NotImplemented

    # Inherit hash from Matcher to avoid breaking the hash/eq contract
    __hash__ = Matcher.__hash__


class ExistsMatchers(Matcher):
    """Matcher for checking existence/non-existence of values."""

    my_matcher: Callable[..., HamcrestMatcher[Any]]

    _MATCHER_FUNCS: dict[MatcherType, Callable[..., HamcrestMatcher[Any]]] = {
        MatcherType.NONE: none,
        MatcherType.NONE_OR_EMPTY: none,
        MatcherType.NOT_NONE: not_none,
        MatcherType.NOT_NONE_OR_EMPTY: not_none,
    }

    def __init__(self, match_col_key: str, matcher_type: MatcherType) -> None:
        super().__init__(match_col_key)

        my_matcher = self._MATCHER_FUNCS.get(matcher_type)
        if my_matcher is None:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")
        self.matcher_type = matcher_type
        self.my_matcher = my_matcher

    def is_match(self, data_record: dict[str, Any]) -> bool:

        if not self.validate_key_exists(data_record):
            return False

        if self.matcher_type in (MatcherType.NONE, MatcherType.NOT_NONE):
            return (match_equality(self.my_matcher())
                    == data_record[self.match_col_key])
        else:
            r""" Special case of chaining equal to with none """
            if self.matcher_type == MatcherType.NONE_OR_EMPTY:
                result = match_equality(any_of(
                    self.my_matcher(),
                    equal_to(''), equal_to([]), equal_to({}), equal_to(())
                )) == data_record[self.match_col_key]
                return result

            elif self.matcher_type == MatcherType.NOT_NONE_OR_EMPTY:
                result = match_equality(all_of(
                    self.my_matcher(),
                    is_not(equal_to('')), is_not(equal_to([])),
                    is_not(equal_to({})), is_not(equal_to(()))
                )) == data_record[self.match_col_key]
                return result
            else:
                raise NotImplementedError(f"Matcher for {self.matcher_type} not implemented")


class DictMatchers(Matcher):
    """Matcher for dictionary entry matching."""

    my_matcher: Callable[..., HamcrestMatcher[Any]]

    _MATCHER_FUNCS: dict[MatcherType, Callable[..., HamcrestMatcher[Any]]] = {
        MatcherType.HAS_ENTRY: has_entry,
        MatcherType.HAS_ENTRIES: has_entries,
    }

    def __init__(self, match_col_key: str, matcher_type: MatcherType, *match_values: Any) -> None:
        super().__init__(match_col_key)

        my_matcher = self._MATCHER_FUNCS.get(matcher_type)
        if my_matcher is None:
            raise NotImplementedError(f"Matcher for {matcher_type} not implemented")
        self.matcher_type = matcher_type
        self.my_matcher = my_matcher

        if len(match_values) == 0:
            raise ValueError("DictMatchers requires at least one match value")

        if self.matcher_type == MatcherType.HAS_ENTRY and len(match_values) > 2:
            raise ValueError("HAS_ENTRY matcher only accepts two values")

        self.match_values = match_values

    def is_match(self, data_record: dict[str, Any]) -> bool:
        if not self.validate_key_exists(data_record):
            return False

        if not data_record[self.match_col_key]:
            """ If record is None or empty, no match"""
            return False

        match_values = self.match_values

        if isinstance(match_values[0], list) and isinstance(data_record[self.match_col_key], list):
            """ Two lists... """
            check_list = []
            for m_dict in match_values[0]:
                # Unpack list of dictionaries to list of tuples to list of match_values
                mv = [item for tup in m_dict.items() for item in tup]
                check_list.append(match_equality(has_item(has_entries(*mv))) == list(data_record[self.match_col_key]))
            return any(check_list)

        if isinstance(match_values[0], list) and isinstance(data_record[self.match_col_key], dict):
            """ Two lists... """
            check_list = []
            for m_dict in match_values[0]:
                # Unpack list of dictionaries to list of tuples to list of match_values
                mv = [item for tup in m_dict.items() for item in tup]
                check_list.append(match_equality(self.my_matcher(*mv)) == data_record[self.match_col_key])
            return any(check_list)

        if isinstance(data_record[self.match_col_key], list):
            # has_item will iterate a sequence ...
            return match_equality(has_item(has_entry(*match_values))) == list(data_record[self.match_col_key])

        if isinstance(match_values[0], dict):
            check_list = []
            for m_dict in match_values:
                # Unpack list of dictionaries to list of tuples to list of match_values
                mv = [item for tup in m_dict.items() for item in tup]
                check_list.append(match_equality(self.my_matcher(*mv)) == data_record[self.match_col_key])
            return any(check_list)

        return (match_equality(self.my_matcher(*match_values))
                == data_record[self.match_col_key])


class AnyOf(DataFilter):
    """Logical OR combinator: matches if any child filter matches."""

    filters: tuple[DataFilter, ...]

    def __init__(self, *filters: DataFilter) -> None:
        if len(filters) == 0:
            raise ValueError("AnyOf requires at least one filter")
        self.filters = filters

    def is_match(self, data_record: dict[str, Any]) -> bool:
        return any(f.is_match(data_record) for f in self.filters)

    def __repr__(self) -> str:
        inner = ', '.join(repr(f) for f in self.filters)
        return f'{self.__class__.__name__}({inner})'

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            return self.filters == other.filters  # type: ignore
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.__class__, self.filters))


class AllOf(DataFilter):
    """Logical AND combinator: matches only if every child filter matches."""

    filters: tuple[DataFilter, ...]

    def __init__(self, *filters: DataFilter) -> None:
        if len(filters) == 0:
            raise ValueError("AllOf requires at least one filter")
        self.filters = filters

    def is_match(self, data_record: dict[str, Any]) -> bool:
        return all(f.is_match(data_record) for f in self.filters)

    def __repr__(self) -> str:
        inner = ', '.join(repr(f) for f in self.filters)
        return f'{self.__class__.__name__}({inner})'

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            return self.filters == other.filters  # type: ignore
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.__class__, self.filters))


class Not(DataFilter):
    """Negation combinator: inverts the result of a single child filter."""

    filters: tuple[DataFilter]

    def __init__(self, data_filter: DataFilter) -> None:
        self.filters = (data_filter,)

    def is_match(self, data_record: dict[str, Any]) -> bool:
        return not self.filters[0].is_match(data_record)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.filters[0]!r})'

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            return self.filters == other.filters  # type: ignore
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.__class__, self.filters))
