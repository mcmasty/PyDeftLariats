"""Main module."""
__version__ = '0.0.1'

from abc import ABC, abstractmethod
from hamcrest import anything, match_equality, equal_to, has_item, starts_with
import logging

from enum import Enum


class MatcherType(Enum):
    ANYTHING = 'Anything'
    EQUAL_TO = 'EqualTo'
    STARTS_WITH = 'StartsWith'


class Matcher(ABC):

    def __init__(self, match_col_key, matcher_type):
        self.matcher_type = matcher_type
        self.match_col_key = match_col_key
        self.my_logger = logging.getLogger('matching')

    @abstractmethod
    def is_match(self, match_values, lead_data) -> bool:
        pass

    def get_key_val(self):
        """ Generate a value suitable for hashing, dictionary key"""
        return frozenset((self.matcher_type.value, self.match_col_key.value))

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.matcher_type!r}, {self.match_col_key!r})')

    def __str__(self):
        return (f'Matcher for {self.matcher_type.value!r} "'
                f'"matching of {self.match_col_key.value!r}')

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.matcher_type, self.match_col_key) == \
                   (other.matcher_type, other.match_col_key)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.__class__, self.matcher_type, self.match_col_key))


class AnythingMatcher(Matcher):

    def __init__(self, match_col_key, matcher_type):
        super().__init__(match_col_key, matcher_type)
        self.match_col_key = match_col_key
        self.my_matcher = anything(f"Anything for {match_col_key}")

    def is_match(self, match_values, lead_data) -> bool:
        # Special handling for '*_row' ... e.g. 'person_row'
        if self.match_col_key.value not in lead_data \
                and '_row' not in self.match_col_key.value:
            self.my_logger.warning((f"'{self.match_col_key}' not in lead data,"
                                    " but anyting matcher, so proceed."))
        return match_equality(self.my_matcher) == lead_data


class EqualTo(Matcher):
    """ Equal To matching style. Cast everything to str. """

    def __init__(self, match_col_key, matcher_type):
        super().__init__(match_col_key, matcher_type)
        self.match_col_key = match_col_key

    def is_match(self, match_values, lead_data) -> bool:
        def pull_val(x): return x
        if self.match_col_key.value not in lead_data:
            self.my_logger.warning((f"'{self.match_col_key.value}' not present"
                                    f" in lead data \n\n{lead_data}\n\n"))
            return False

        if len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, return False")
            return False
        elif len(match_values) == 1:
            q_match_values = pull_val(*match_values)
            return (match_equality(equal_to(q_match_values))
                    == str(lead_data[self.match_col_key.value]))

        else:
            # has_item will iterate a sequence ...
            return match_equality(
                has_item(equal_to(
                    lead_data[self.match_col_key.value]))) == [
                str(x) for x in match_values]


class StartsWith(Matcher):

    def __init__(self, match_col_key, matcher_type):
        super().__init__(match_col_key, matcher_type)
        self.match_col_key = match_col_key

    def is_match(self, match_values, lead_data) -> bool:
        def pull_val(x): return x
        if self.match_col_key.value not in lead_data:
            self.my_logger.warning((f"'{self.match_col_key.value}' not present"
                                    f" in lead data \n\n{lead_data}\n\n"))
            return False

        if len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, return False")
            return False
        elif len(match_values) == 1:
            q_match_values = pull_val(*match_values)
            return (match_equality(starts_with(q_match_values))
                    == str(lead_data[self.match_col_key.value]))
        else:

            matches_list = [q for q in match_values
                            if match_equality(starts_with(q))
                            == str(lead_data[self.match_col_key.value])]
            if len(matches_list) > 0:
                return True
            else:
                return False
