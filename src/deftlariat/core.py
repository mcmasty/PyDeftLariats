"""Main module."""
__version__ = '0.0.1'

from abc import ABC, abstractmethod
from hamcrest import anything, match_equality, equal_to, has_item, starts_with, \
    greater_than, greater_than_or_equal_to
import logging

from enum import Enum


class MatcherType(Enum):
    NOTHING = 'Nothing'
    ANYTHING = 'Anything'
    EQUAL_TO = 'EqualTo'
    STARTS_WITH = 'StartsWith'
    GREATER_THAN = 'GreaterThan'


def pull_val(x):
    return x

class Matcher(ABC):

    def __init__(self, match_col_key):
        self.matcher_type = MatcherType.NOTHING
        self.match_col_key = match_col_key
        self.my_logger = logging.getLogger('matching')

    @abstractmethod
    def is_match(self, match_values, data_record) -> bool:
        pass

    def get_key_val(self):
        """ Generate a value suitable for hashing, dictionary key"""
        return frozenset((self.matcher_type.value, self.match_col_key))

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.matcher_type!r}, {self.match_col_key!r})')

    def __str__(self):
        return (f'Matcher for {self.matcher_type.value!r} '
                f'matching on field {self.match_col_key!r}')

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.matcher_type, self.match_col_key) == \
                   (other.matcher_type, other.match_col_key)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.__class__, self.matcher_type, self.match_col_key))


class NothingMatcher(Matcher):

    def __init__(self, match_col_key):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.NOTHING

    def is_match(self, match_values, data_record) -> bool:
        self.my_logger.info("No Matcher set, defaults to Nothing Matcher. Always False.")
        return False


class AnythingMatcher(Matcher):

    def __init__(self, match_col_key):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.ANYTHING
        self.my_matcher = anything(f"Anything for {match_col_key}")

    def is_match(self, match_values, data_record) -> bool:
        return match_equality(self.my_matcher) == data_record





class EqualTo(Matcher):
    """ Equal To matching style. Cast everything to str. """

    def __init__(self, match_col_key, ):
        super().__init__(match_col_key, )
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.EQUAL_TO

    def is_match(self, match_values, data_record) -> bool:

        if self.match_col_key not in data_record:
            self.my_logger.warning((f"'{self.match_col_key}' not present"
                                    f" in data record \n\n{data_record}\n\n"))
            return False

        if len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, raising Error")
            raise NotImplementedError("Cannot use Equal To to check for empty "
                                      "string. Use None or Not_None.")

        elif isinstance(match_values, list):
            if len(match_values) == 0:
                # covered by len ==0 above
                pass

            elif len(match_values) == 1:
                q_match_values = pull_val(*match_values)
                return (match_equality(equal_to(q_match_values))
                        == str(data_record[self.match_col_key]))

            else:
                # has_item will iterate a sequence ...
                return match_equality(
                    has_item(equal_to(
                        data_record[self.match_col_key]))) == [
                           str(x) for x in match_values]

        else:
            return (match_equality(equal_to(match_values))
                    == str(data_record[self.match_col_key]))


class StartsWith(Matcher):

    def __init__(self, match_col_key):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.STARTS_WITH

    def is_match(self, match_values, data_record) -> bool:

        if self.match_col_key not in data_record:
            self.my_logger.warning((f"'{self.match_col_key}' not present"
                                    f" in data record \n\n{data_record}\n\n"))
            return False

        if len(match_values) == 0:
            self.my_logger.warning("No Match Values provided, raising Error")
            raise NotImplementedError("Cannot use StartsWith to check for "
                                      "empty string. Use None or Not_None.")

        elif isinstance(match_values, list):

            if len(match_values) == 1:
                q_match_values = pull_val(*match_values)
                return (match_equality(starts_with(q_match_values))
                        == str(data_record[self.match_col_key]))
            else:
                matches_list = [q for q in match_values
                                if match_equality(starts_with(q))
                                == str(data_record[self.match_col_key])]
                if len(matches_list) > 0:
                    return True
                else:
                    return False
        else:
            return (match_equality(starts_with(match_values))
                    == str(data_record[self.match_col_key]))


class GreaterThan(Matcher):

    def __init__(self, match_col_key):
        super().__init__(match_col_key)
        self.match_col_key = match_col_key
        self.matcher_type = MatcherType.GREATER_THAN

    def is_match(self, match_values, data_record) -> bool:
        if self.match_col_key not in data_record:
            self.my_logger.warning((f"'{self.match_col_key}' not present"
                                    f" in data record \n\n{data_record}\n\n"))
            return False

        if isinstance(match_values, list):
            if len(match_values) == 0:
                self.my_logger.warning("No Match Values provided, raising Error")
                cls_name = self.__class__.__name__
                raise NotImplementedError(fr"Cannot use {cls_name} to check for "
                                          "empty string. Use None or Not_None.")
            elif len(match_values) == 1:
                q_match_values = pull_val(*match_values)
                return (match_equality(greater_than(q_match_values))
                        == data_record[self.match_col_key])
            else:
                cls_name = self.__class__.__name__
                raise NotImplementedError(fr"Cannot use {cls_name} to check "
                                          " a list of values")
        else:
            return (match_equality(greater_than(match_values))
                    == data_record[self.match_col_key])
