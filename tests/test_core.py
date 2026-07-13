from unittest import TestCase

from hamcrest import *

from deftlariat import (
    AllOf,
    AnyOf,
    AnythingMatcher,
    DictMatchers,
    EqualTo,
    ExistsMatchers,
    Matcher,
    MatcherType,
    Not,
    NumberComparer,
    TextComparer,
)


class TestAnythingMatcher(TestCase):
    def test_dumb(self):
        assert_that(True, equal_to(True), "Dumb test.")

    def test_record_is_match(self):
        a_matcher = AnythingMatcher("full_record")
        test_data = {}
        assert_that(a_matcher.is_match(test_data), equal_to(True))

        test_obj = object()
        assert_that(a_matcher.is_match(test_obj), equal_to(True))

        assert_that(a_matcher.is_match(None), equal_to(True))

        assert_that(a_matcher.is_match(1), equal_to(True))

        assert_that(a_matcher.is_match(1), equal_to(True))

        assert_that(a_matcher.is_match('cat'), equal_to(True))


class TestEqualTo(TestCase):
    def test_is_match_single(self):
        test_data_record = {'name': 'Scarlet Shelton'}

        target_value = 'Scarlet Shelton'
        name_check = EqualTo('name', target_value)
        assert_that(name_check.is_match(test_data_record),
                    equal_to(True),
                    "Is target value in test data?")

        target_value = 'Bob Fisher'
        name_check = EqualTo('name', target_value)
        assert_that(name_check.is_match(test_data_record),
                    equal_to(False),
                    "Is target value in test data?")

    def test_empty_list_raises_error(self):
        target_value = []

        with self.assertRaises(ValueError):
            EqualTo('name', target_value)

    def test_is_match_list(self):
        test_data_record = {'name': 'Scarlet Shelton'}

        # Test a single item list
        target_value = ['Scarlet Shelton']
        name_check = EqualTo('name', target_value)
        self.assertTrue(name_check.is_match(test_data_record),
                        "Check against single item list")

        # Test successful, but look for one of many people
        target_value = ['Rudy Stout', 'Todd Lee', 'Scarlet Shelton']
        name_check = EqualTo('name', target_value)
        self.assertTrue(name_check.is_match(test_data_record),
                        "Check against multi item list")

        # Remove Scarlet and test again, should not be found
        target_value.pop(2)
        name_check = EqualTo('name', target_value)
        self.assertFalse(name_check.is_match(test_data_record), "Check against list")

    def test_is_key_not_in_data(self):
        test_data_record = {'full_name': 'Scarlet Shelton'}

        # Test a single item list
        target_value = ['Scarlet Shelton']
        name_check = EqualTo('name', target_value)

        self.assertFalse(name_check.is_match(test_data_record),
                         "Check against single item list")

    def test_boolean(self):
        test_data_record = {'full_name': True}

        target_value = [False]
        name_check = EqualTo('full_name', target_value)

        self.assertFalse(name_check.is_match(test_data_record),
                         "Check boolean no match")

        name_check = EqualTo('full_name', [True])
        self.assertTrue(name_check.is_match(test_data_record),
                        "Check boolean does match")


    def test_obj(self):
        class MyObject:
            def __init__(self, something):
                self.foo = something

            def __eq__(self, other):
                return self.foo == other.foo

        a = MyObject('cad')
        test_data_record = {'full_name': [a]}

        b = MyObject(None)
        target_value = [b]
        name_check = EqualTo('full_name', target_value)
        self.assertFalse(name_check.is_match(test_data_record),
                         "Check boolean no match")

        target_value = [MyObject('cad'), MyObject('aaa')]
        name_check = EqualTo('full_name', target_value)
        self.assertTrue(name_check.is_match(test_data_record),
                        "One of the target objects ('cad') matches the data record")




class TestTextCompareBoundaryCases(TestCase):
    def setUp(self) -> None:

        self.text_matcher_types = [MatcherType.STARTS_WITH, MatcherType.CONTAINS_STRING,
                              MatcherType.CONTAINS_STRING_IN_ORDER,
                              MatcherType.EQUAL_TO_IGNORE_WHITESPACE,
                              MatcherType.EQUAL_TO_IGNORE_CASE]

    def test_empty_input_list(self):
        target_value = []
        for m_type in self.text_matcher_types:
            with self.assertRaises(ValueError, msg=f"Checking {m_type}"):
                TextComparer('text_col', m_type, target_value)

    def test_key_not_in_data_record(self):
        test_data_record = {'rating': 'Superduper'}

        # Field bound at construction is valid; the record just doesn't have the key.
        target_value = ['Super']
        for m_type in self.text_matcher_types:
            comparer = TextComparer('text_col', m_type, target_value)
            assert_that(comparer.is_match(test_data_record),
                        equal_to(False), 'Col not present in data recrod returns FALSE')

    def test_bad_matcher_type(self):

        with self.assertRaises(NotImplementedError):
            TextComparer("Foo", MatcherType.GREATER_THAN_EQUAL_TO, "bar")


class TestStartsWith(TestCase):
    def test_dumb(self):
        self.assertTrue(True)

    def test_is_match_multiple_values(self):
        test_data_record = {'equipment': 'baseball'}

        # Test a single item list
        target_value = ['base']
        ball_starts_with = TextComparer('equipment', MatcherType.STARTS_WITH, target_value)
        self.assertTrue(ball_starts_with.is_match(test_data_record),
                        "find one of the balls")

        # Test a longer list
        target_value = ['foot', 'soccer', 'base']
        ball_starts_with = TextComparer('equipment', MatcherType.STARTS_WITH, target_value)
        self.assertTrue(ball_starts_with.is_match(test_data_record),
                        "find one of the balls")

        # Test a longer list, that will fail
        target_value = ['foot', 'soccer', 'basket']
        ball_starts_with = TextComparer('equipment', MatcherType.STARTS_WITH, target_value)
        self.assertFalse(ball_starts_with.is_match(test_data_record),
                         "No balls to find")

    def test_is_match_single_value(self):
        test_data_record = {'rating': 'Superduper'}

        # Test a single item list
        target_value = 'Super'
        rating_starts_with = TextComparer('rating', MatcherType.STARTS_WITH, target_value)

        self.assertTrue(rating_starts_with.is_match(test_data_record),
                        "looking at field not in data record")

    def test_is_match_convert_to_str(self):
        test_data_record = {'department': 11223344}

        # Test a single item
        target_value = '1122'
        dept_starts_with = TextComparer('department', MatcherType.STARTS_WITH, target_value)
        self.assertTrue(dept_starts_with.is_match(test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['1122']
        dept_starts_with = TextComparer('department', MatcherType.STARTS_WITH, target_value)
        self.assertTrue(dept_starts_with.is_match(test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '3333']
        dept_starts_with = TextComparer('department', MatcherType.STARTS_WITH, target_value)
        self.assertTrue(dept_starts_with.is_match(test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        dept_starts_with = TextComparer('department', MatcherType.STARTS_WITH, target_value)
        self.assertFalse(dept_starts_with.is_match(test_data_record),
                         "No-Match - one of departments")


class TestEqualToIgnoreCase(TestCase):
    def test_dumb(self):
        self.assertTrue(True)

    def test_is_match_multiple_values(self):
        test_data_record = {'equipment': 'basEBAll'}

        # Test a single item list
        target_value = ['baseball']
        eq_ignore_case = TextComparer('equipment', MatcherType.EQUAL_TO_IGNORE_CASE, target_value)
        self.assertTrue(eq_ignore_case.is_match(test_data_record),
                        "find one of the balls")

        # Test a longer list
        target_value = ['football', 'baseball']
        eq_ignore_case = TextComparer('equipment', MatcherType.EQUAL_TO_IGNORE_CASE, target_value)
        self.assertTrue(eq_ignore_case.is_match(test_data_record),
                        "find one of the balls")

        # Test a longer list, that will fail
        target_value = ['foot', 'soccer', 'basket']
        eq_ignore_case = TextComparer('equipment', MatcherType.EQUAL_TO_IGNORE_CASE, target_value)
        self.assertFalse(eq_ignore_case.is_match(test_data_record),
                         "No balls to find")

    def test_ignore_whitespace(self):
        test_data_record = {'department': 11223344}

        # Test a single item
        target_value = '11223344'
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertTrue(eq_ignore_whitespace.is_match(test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['11223344']
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertTrue(eq_ignore_whitespace.is_match(test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '11223344']
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertTrue(eq_ignore_whitespace.is_match(test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertFalse(eq_ignore_whitespace.is_match(test_data_record),
                         "No-Match - one of departments")

        test_data_record = {'department': '  11223344  '}

        # Test a single item
        target_value = '11223344'
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertTrue(eq_ignore_whitespace.is_match(test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['11223344']
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertTrue(eq_ignore_whitespace.is_match(test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '11223344']
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertTrue(eq_ignore_whitespace.is_match(test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        eq_ignore_whitespace = TextComparer('department', MatcherType.EQUAL_TO_IGNORE_WHITESPACE, target_value)
        self.assertFalse(eq_ignore_whitespace.is_match(test_data_record),
                         "No-Match - one of departments")


class TestNumberComparisons(TestCase):

    def test_dumb(self):
        self.assertTrue(True)

    def test_single_value(self):
        test_data_record = {'my_number': 5}

        def nc(m_type, values):
            return NumberComparer('my_number', m_type, values).is_match(test_data_record)

        # Test a single item
        target_value = 4
        self.assertTrue(nc(MatcherType.GREATER_THAN, target_value), " 5 > 4 = True")
        self.assertTrue(nc(MatcherType.GREATER_THAN_EQUAL_TO, target_value), " 5 >= True ")
        self.assertFalse(nc(MatcherType.LESS_THAN, target_value), " 5 < 4 = False")
        self.assertFalse(nc(MatcherType.LESS_THAN_EQUAL_TO, target_value), " 5 <= 4 = False ")
        self.assertTrue(nc(MatcherType.CLOSE_TO, (target_value, 2)), " 5 close to (4,2) = True")
        self.assertTrue(nc(MatcherType.CLOSE_TO, (target_value, 1)), " 5 close to (4,2) = True")

        # Test a single item
        target_value = 10

        self.assertFalse(nc(MatcherType.GREATER_THAN, target_value), " 5 > 10 = False")
        self.assertFalse(nc(MatcherType.GREATER_THAN_EQUAL_TO, target_value), " 5 >= 10 False ")
        self.assertTrue(nc(MatcherType.LESS_THAN, target_value), " 5 < 10 = True")
        self.assertTrue(nc(MatcherType.LESS_THAN_EQUAL_TO, target_value), " 5 <= 10 = True ")
        self.assertFalse(nc(MatcherType.CLOSE_TO, (target_value, 2)), " 5 close to (10,2) = False")
        self.assertFalse(nc(MatcherType.CLOSE_TO, (target_value, 1)), " 5 close to (10,2) = False")

    def test_none_value_without_replacement(self):
        # Documents current behavior for None record values when convert_none_to is not set
        nc = NumberComparer('n', MatcherType.GREATER_THAN, 4)
        test_data_record = {'n': None}
        self.assertFalse(nc.is_match(test_data_record),
                        "None value without convert_none_to replacement returns False")


class TestNumberComparisonsWithReplacement(TestCase):

    def test_single_none_with_replacement(self):
        test_data_record = {'my_number': None}

        # Test a single item
        target_value = 4
        self.assertTrue(NumberComparer('my_number', MatcherType.GREATER_THAN, target_value, convert_none_to=5)
                        .is_match(test_data_record),
                        " 5 > 4 = True")
        self.assertTrue(NumberComparer('my_number', MatcherType.GREATER_THAN_EQUAL_TO, target_value, convert_none_to=5)
                        .is_match(test_data_record),
                        " 5 >= True ")
        self.assertFalse(NumberComparer('my_number', MatcherType.LESS_THAN, target_value, convert_none_to=5)
                         .is_match(test_data_record),
                         " 5 < 4 = False")
        self.assertFalse(NumberComparer('my_number', MatcherType.LESS_THAN_EQUAL_TO, target_value, convert_none_to=5)
                         .is_match(test_data_record),
                         " 5 <= 4 = False ")
        self.assertTrue(NumberComparer('my_number', MatcherType.CLOSE_TO, (target_value, 2), convert_none_to=5)
                        .is_match(test_data_record),
                        " 5 close to (4,2) = True")
        self.assertTrue(NumberComparer('my_number', MatcherType.CLOSE_TO, (target_value, 1), convert_none_to=5)
                        .is_match(test_data_record),
                        " 5 close to (4,2) = True")

        # Test a single item
        target_value = 10

        self.assertFalse(NumberComparer('my_number', MatcherType.GREATER_THAN, target_value, convert_none_to=5)
                         .is_match(test_data_record),
                         " 5 > 10 = False")
        self.assertFalse(NumberComparer('my_number', MatcherType.GREATER_THAN_EQUAL_TO, target_value, convert_none_to=5)
                         .is_match(test_data_record),
                         " 5 >= 10 False ")
        self.assertTrue(NumberComparer('my_number', MatcherType.LESS_THAN, target_value, convert_none_to=5)
                        .is_match(test_data_record),
                        " 5 < 10 = True")
        self.assertTrue(NumberComparer('my_number', MatcherType.LESS_THAN_EQUAL_TO, target_value, convert_none_to=5)
                        .is_match(test_data_record),
                        " 5 <= 10 = True ")
        self.assertFalse(NumberComparer('my_number', MatcherType.CLOSE_TO, (target_value, 2), convert_none_to=5)
                         .is_match(test_data_record),
                         " 5 close to (10,2) = False")
        self.assertFalse(NumberComparer('my_number', MatcherType.CLOSE_TO, (target_value, 1), convert_none_to=5)
                         .is_match(test_data_record),
                         " 5 close to (10,2) = False")

    def test_is_gt_list_value(self):
        test_data_record = {'my_number': 5}

        # Test a single item list
        target_value = [4]
        number_gt_check = NumberComparer('my_number', MatcherType.GREATER_THAN, target_value, convert_none_to=5)
        self.assertTrue(number_gt_check.is_match(test_data_record),
                        "looking at field not in data record")

        # Test a single item list
        target_value = [10]
        number_gt_check = NumberComparer('my_number', MatcherType.GREATER_THAN, target_value, convert_none_to=5)
        self.assertFalse(number_gt_check.is_match(test_data_record),
                         "looking at field not in data record")

    def test_empty_list_raise_error(self):
        target_value = []
        with self.assertRaises(ValueError):
            NumberComparer('my_number', MatcherType.GREATER_THAN, target_value, convert_none_to=5)

    def test_multiple_vals_raise_error(self):
        target_value = [1, 2, 3, 4]
        with self.assertRaises(ValueError):
            NumberComparer('my_number', MatcherType.GREATER_THAN, target_value, convert_none_to=5)


class AbstractTestMatcher(Matcher):
    """ A class sole for testing the Abstract Base Class """

    def __init__(self, match_key_col):
        super().__init__(match_key_col)

    def is_match(self, data_record):
        raise NotImplementedError


class TestMatcher(TestCase):
    def test_reper(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        assert_that("some_key_field", is_in(abc_matcher.__repr__()), "Check output")

    def test_get_key_value(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        test_key = (MatcherType.NOTHING.value, 'some_key_field')
        assert_that(abc_matcher.get_key_val(), equal_to(test_key))

    def test_str(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        assert_that("some_key_field", is_in(abc_matcher.__str__()), "Check output")

    def test_match(self):
        abc_matcher = AbstractTestMatcher("some_key_field")
        with self.assertRaises(NotImplementedError):
            abc_matcher.is_match({"data": "record"})

    def test_equality_same_field_and_values(self):
        m1 = EqualTo('name', 'Scarlet Shelton')
        m2 = EqualTo('name', 'Scarlet Shelton')
        assert_that(m1, equal_to(m2))
        assert_that(hash(m1), equal_to(hash(m2)))

    def test_equality_same_field_different_values(self):
        m1 = EqualTo('name', 'Scarlet Shelton')
        m2 = EqualTo('name', 'Bob Fisher')
        assert_that(m1, is_not(equal_to(m2)))

    def test_equality_different_field(self):
        m1 = EqualTo('name', 'Scarlet Shelton')
        m2 = EqualTo('full_name', 'Scarlet Shelton')
        assert_that(m1, is_not(equal_to(m2)))


class TestNumberMatcherBoundaryCases(TestCase):
    def setUp(self) -> None:

        self.number_matcher_types = [MatcherType.GREATER_THAN, MatcherType.GREATER_THAN_EQUAL_TO,
                                MatcherType.LESS_THAN, MatcherType.LESS_THAN_EQUAL_TO,
                                MatcherType.CLOSE_TO]

    def test_empty_input(self):
        for m_type in self.number_matcher_types:
            target_value = []
            with self.assertRaises(ValueError, msg=f"Checking {m_type}"):
                NumberComparer('number_col', m_type, target_value)

    def test_key_not_in_data_record(self):
        test_data_record = {'some_other_columns': 11223344}

        for m_type in self.number_matcher_types:
            target_value = (1, 1) if m_type == MatcherType.CLOSE_TO else 1
            comparer = NumberComparer('number_col', m_type, target_value)

            assert_that(comparer.is_match(test_data_record),
                        equal_to(False), "Return False when field not available.")

    def test_reject_multiple_inputs(self):
        for m_type in self.number_matcher_types:
            target_value = [1, 2, 3, 4]
            with self.assertRaises(ValueError, msg=f"Checking {m_type}"):
                NumberComparer('number_col', m_type, target_value)

    def test_bad_matcher_type(self):
        with self.assertRaises(NotImplementedError):
            NumberComparer("Foo", MatcherType.STARTS_WITH, 1)


class TestExistenceMatcherBoundaryCases(TestCase):
    def setUp(self) -> None:

        exists_matcher_types = [MatcherType.NONE, MatcherType.NONE_OR_EMPTY,
                                MatcherType.NOT_NONE, MatcherType.NOT_NONE_OR_EMPTY]

        self.my_exists_comparer_list = []
        for m_type in exists_matcher_types:
            self.my_exists_comparer_list.append(ExistsMatchers('number_col', m_type))

    def test_key_not_in_data_record(self):
        test_data_record = {'some_other_columns': 11223344}

        for comparer in self.my_exists_comparer_list:
            assert_that(comparer.is_match(test_data_record),
                        equal_to(False), "Return False when field not available.")

    def test_bad_matcher_type(self):
        with self.assertRaises(NotImplementedError):
            NumberComparer("Foo", MatcherType.STARTS_WITH, 1)


class TestExistsMatchers(TestCase):

    def test_is_none(self):
        my_is_none = ExistsMatchers('some_col', MatcherType.NONE)

        test_data_record = {'some_col': None}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

    def test_not_none(self):
        my_not_none = ExistsMatchers('some_col', MatcherType.NOT_NONE)

        test_data_record = {'some_col': None}
        assert_that(my_not_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_not_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_not_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_not_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

    def test_is_none_or_empty(self):
        my_is_none = ExistsMatchers('some_col', MatcherType.NONE_OR_EMPTY)

        test_data_record = {'some_col': None}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': {}}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': ()}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

    def test_not_none_or_empty(self):
        my_is_none = ExistsMatchers('some_col', MatcherType.NOT_NONE_OR_EMPTY)

        test_data_record = {'some_col': None}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': 'data'}
        assert_that(my_is_none.is_match(test_data_record), equal_to(True),
                    "It is actually None")

        test_data_record = {'some_col': ''}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': []}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': {}}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")

        test_data_record = {'some_col': ()}
        assert_that(my_is_none.is_match(test_data_record), equal_to(False),
                    "It is actually None")


class TestDictMatchers(TestCase):

    def test_has_entries(self):
        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, 'a', 'b')
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, {'a': 'b'})
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, {'foo': 'bar'})
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))
        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, 'foo', 'bar')
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, 'a', 'b', 'c', 'd')
                    .is_match(data_record={'dumb': {'c': 'd', 'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, 'a', 'b')
                    .is_match(data_record={'dumb': [
                        {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, [{'a': 'b'}, {'1': '2'}])
                    .is_match(data_record={'dumb': [
                        {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, [{'a': 'g'}, {'1': 'g'}])
                    .is_match(data_record={'dumb': [
                        {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(False))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, [{'a': 'g'}, {'1': 'g'}])
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, [{'a': 'b'}, {'1': '2'}])
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES,
                                  [{'a': 'b'}, {'1': '2'}, {'id': 'asdf', 'identifier': 'foo'}])
                    .is_match(data_record={'dumb': [{'a': 'b'}, {'id': 'asdf', 'identifier': 'foo'}]}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRIES, [{'a': 'b'}, {'1': '2'}])
                    .is_match(data_record={'dumb': None}),
                    equal_to(False))



    def test_has_entry(self):
        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, 'a', 'b')
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, {'a': 'b'})
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, {'foo': 'bar'})
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))
        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, 'foo', 'bar')
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, 'a', 'b')
                    .is_match(data_record={'dumb': [
                        {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, [{'a': 'b'}, {'1': '2'}])
                    .is_match(data_record={'dumb': [
                        {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(True))


        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, [{'a': 'g'}, {'1': 'g'}])
                    .is_match(data_record={'dumb': [
                        {'1': '2'}, {'c': 'd'}, {'a': 'b'}]}),
                    equal_to(False))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, [{'a': 'g'}, {'1': 'g'}])
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(False))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, [{'a': 'b'}, {'1': '2'}])
                    .is_match(data_record={'dumb': {'a': 'b'}}),
                    equal_to(True))

        assert_that(DictMatchers('dumb', MatcherType.HAS_ENTRY, [{'a': 'b'}, {'1': '2'}])
                    .is_match(data_record={'dumb': None}),
                    equal_to(False))



    def test_has_entry_bad_input(self):
        with self.assertRaises(ValueError):
            DictMatchers('dumb', MatcherType.HAS_ENTRY, 'a', 'b', 'c', 'd')

    def test_has_entries_skill_records(self):
        target_skills = [
            {'id': '61d8923376841a071b5fb398', 'identifier': 'Alto Sax'},
            {'id': '61d8923376841a071b5fb39a', 'identifier': 'Tenor Sax'},
            {'id': '61d8923376841a071b5fb39c', 'identifier': 'Bari Sax'},
            {'id': '61d8923376841a071b5fb39e', 'identifier': 'Trumpet'},
            {'id': '61d8923376841a071b5fb3a0', 'identifier': 'Trombone'},
            {'id': '6223aa9d10a7d3001e006f66', 'identifier': '2nd Trumpet'},
        ]

        assert_that(DictMatchers('skills', MatcherType.HAS_ENTRIES, 'identifier', 'Trumpet')
                    .is_match(data_record={'skills': target_skills}),
                    equal_to(True))

        assert_that(DictMatchers('skills', MatcherType.HAS_ENTRIES, 'identifier', 'Violin')
                    .is_match(data_record={'skills': target_skills}),
                    equal_to(False))


class TestAnyOf(TestCase):
    def test_true_when_one_child_matches(self):
        test_data_record = {'name': 'Scarlet Shelton', 'age': 40}

        combined = AnyOf(
            EqualTo('name', 'Nobody Here'),
            NumberComparer('age', MatcherType.GREATER_THAN_EQUAL_TO, 40),
        )
        assert_that(combined.is_match(test_data_record), equal_to(True))

    def test_false_when_no_child_matches(self):
        test_data_record = {'name': 'Scarlet Shelton', 'age': 40}

        combined = AnyOf(
            EqualTo('name', 'Nobody Here'),
            NumberComparer('age', MatcherType.GREATER_THAN, 100),
        )
        assert_that(combined.is_match(test_data_record), equal_to(False))

    def test_requires_at_least_one_filter(self):
        with self.assertRaises(ValueError):
            AnyOf()


class TestAllOf(TestCase):
    def test_true_only_when_all_match(self):
        test_data_record = {'name': 'Scarlet Shelton', 'age': 40}

        combined = AllOf(
            EqualTo('name', 'Scarlet Shelton'),
            NumberComparer('age', MatcherType.GREATER_THAN_EQUAL_TO, 40),
        )
        assert_that(combined.is_match(test_data_record), equal_to(True))

    def test_false_when_one_child_does_not_match(self):
        test_data_record = {'name': 'Scarlet Shelton', 'age': 40}

        combined = AllOf(
            EqualTo('name', 'Scarlet Shelton'),
            NumberComparer('age', MatcherType.GREATER_THAN, 100),
        )
        assert_that(combined.is_match(test_data_record), equal_to(False))

    def test_requires_at_least_one_filter(self):
        with self.assertRaises(ValueError):
            AllOf()


class TestNot(TestCase):
    def test_inverts_match(self):
        test_data_record = {'name': 'Scarlet Shelton'}

        matcher = EqualTo('name', 'Scarlet Shelton')
        assert_that(Not(matcher).is_match(test_data_record), equal_to(False))

        matcher = EqualTo('name', 'Somebody Else')
        assert_that(Not(matcher).is_match(test_data_record), equal_to(True))


class TestNestedCombinators(TestCase):
    def test_any_of_containing_all_of(self):
        test_data_record = {'name': 'Scarlet Shelton', 'age': 40, 'country': 'US'}

        nested = AnyOf(
            AllOf(
                EqualTo('name', 'Scarlet Shelton'),
                EqualTo('country', 'CA'),
            ),
            EqualTo('country', 'US'),
        )
        assert_that(nested.is_match(test_data_record), equal_to(True))

        nested = AnyOf(
            AllOf(
                EqualTo('name', 'Scarlet Shelton'),
                EqualTo('country', 'CA'),
            ),
            EqualTo('country', 'MX'),
        )
        assert_that(nested.is_match(test_data_record), equal_to(False))


class TestNumberComparerEquality(TestCase):
    def test_equality_same_all_args(self):
        """Two NumberComparers with identical args should be equal."""
        m1 = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=0)
        m2 = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=0)
        assert_that(m1, equal_to(m2))
        assert_that(hash(m1), equal_to(hash(m2)))

    def test_inequality_different_convert_none_to(self):
        """Two NumberComparers differing only in convert_none_to should NOT be equal."""
        m1 = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=0)
        m2 = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=100)
        assert_that(m1, is_not(equal_to(m2)))

    def test_inequality_different_replacement_val(self):
        """Two NumberComparers differing in replacement_val should NOT be equal."""
        m1 = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=50)
        m2 = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=75)
        assert_that(m1, is_not(equal_to(m2)))

    def test_equality_no_convert_none_to(self):
        """Two NumberComparers both without convert_none_to should be equal."""
        m1 = NumberComparer('n', MatcherType.GREATER_THAN, 5)
        m2 = NumberComparer('n', MatcherType.GREATER_THAN, 5)
        assert_that(m1, equal_to(m2))
        assert_that(hash(m1), equal_to(hash(m2)))

    def test_hashable_with_convert_none(self):
        """NumberComparers with convert_none_to should still be hashable."""
        m = NumberComparer('n', MatcherType.GREATER_THAN, 5, convert_none_to=0)
        # Should not raise
        h = hash(m)
        assert_that(h, not_none())


class TestDictMatchersEmptyValues(TestCase):
    def test_dict_matchers_no_values_raises_error(self):
        """DictMatchers with no match values should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            DictMatchers('dumb', MatcherType.HAS_ENTRY)
        assert_that(str(context.exception), contains_string("requires at least one"))

    def test_dict_matchers_has_entries_no_values_raises_error(self):
        """DictMatchers HAS_ENTRIES with no match values should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            DictMatchers('dumb', MatcherType.HAS_ENTRIES)
        assert_that(str(context.exception), contains_string("requires at least one"))


class TestEqualToScalarValues(TestCase):
    def test_equal_to_scalar_int_match(self):
        """EqualTo with scalar int should match when data value equals the scalar."""
        matcher = EqualTo('id', 0)
        assert_that(matcher.is_match({'id': 0}), equal_to(True))

    def test_equal_to_scalar_int_no_match(self):
        """EqualTo with scalar int should not match when data value differs."""
        matcher = EqualTo('id', 0)
        assert_that(matcher.is_match({'id': 1}), equal_to(False))

    def test_equal_to_scalar_int_comparison(self):
        """EqualTo with scalar int should support various values."""
        matcher = EqualTo('count', 42)
        assert_that(matcher.is_match({'count': 42}), equal_to(True))
        assert_that(matcher.is_match({'count': 41}), equal_to(False))

    def test_equal_to_list_still_works(self):
        """EqualTo with list should still work as before."""
        matcher = EqualTo('name', ['Alice', 'Bob'])
        assert_that(matcher.is_match({'name': 'Alice'}), equal_to(True))
        assert_that(matcher.is_match({'name': 'Charlie'}), equal_to(False))

    def test_equal_to_string_still_works(self):
        """EqualTo with string should still work as before."""
        matcher = EqualTo('name', 'Alice')
        assert_that(matcher.is_match({'name': 'Alice'}), equal_to(True))
        assert_that(matcher.is_match({'name': 'Bob'}), equal_to(False))


class TestTextComparerScalarValues(TestCase):
    def test_text_comparer_scalar_int_match(self):
        """TextComparer with scalar int should convert and match."""
        matcher = TextComparer('department', MatcherType.STARTS_WITH, 42)
        assert_that(matcher.is_match({'department': 42}), equal_to(True))
        assert_that(matcher.is_match({'department': 420}), equal_to(True))

    def test_text_comparer_scalar_int_no_match(self):
        """TextComparer with scalar int should not match non-matching values."""
        matcher = TextComparer('department', MatcherType.STARTS_WITH, 42)
        assert_that(matcher.is_match({'department': 'hello'}), equal_to(False))

    def test_text_comparer_list_still_works(self):
        """TextComparer with list should still work as before."""
        matcher = TextComparer('equipment', MatcherType.STARTS_WITH, ['base'])
        assert_that(matcher.is_match({'equipment': 'baseball'}), equal_to(True))


class TestNumberComparerCloseTo(TestCase):
    def test_close_to_valid_tuple(self):
        """NumberComparer CLOSE_TO with valid (value, delta) tuple should work."""
        matcher = NumberComparer('my_number', MatcherType.CLOSE_TO, (4, 2))
        assert_that(matcher.is_match({'my_number': 5}), equal_to(True))
        assert_that(matcher.is_match({'my_number': 3}), equal_to(True))
        assert_that(matcher.is_match({'my_number': 7}), equal_to(False))

    def test_close_to_valid_list(self):
        """NumberComparer CLOSE_TO with valid [value, delta] list should work and normalize to tuple."""
        matcher = NumberComparer('my_number', MatcherType.CLOSE_TO, [4, 2])
        # Should convert to tuple internally and work correctly
        assert_that(matcher.is_match({'my_number': 5}), equal_to(True))
        assert_that(matcher.is_match({'my_number': 3}), equal_to(True))

    def test_close_to_single_value_raises_error(self):
        """NumberComparer CLOSE_TO with only one value should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            NumberComparer('n', MatcherType.CLOSE_TO, [5])
        assert_that(str(context.exception), contains_string("CLOSE_TO requires a (value, delta) pair"))

    def test_close_to_scalar_raises_error(self):
        """NumberComparer CLOSE_TO with scalar value should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            NumberComparer('n', MatcherType.CLOSE_TO, 5)
        assert_that(str(context.exception), contains_string("CLOSE_TO requires a (value, delta) pair"))

    def test_close_to_three_values_raises_error(self):
        """NumberComparer CLOSE_TO with three values should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            NumberComparer('n', MatcherType.CLOSE_TO, [4, 2, 1])
        assert_that(str(context.exception), contains_string("CLOSE_TO requires a (value, delta) pair"))
