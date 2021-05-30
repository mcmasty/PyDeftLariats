from unittest import TestCase
from hamcrest import assert_that, equal_to
from deftlariat.core import AnythingMatcher, EqualTo, StartsWith, GreaterThan


class TestAnythingMatcher(TestCase):
    def test_dumb(self):
        assert_that(True, equal_to(True), "Dumb test.")

    def test_record_is_match(self):
        a_matcher = AnythingMatcher("full_record")
        test_data = dict()
        assert_that(a_matcher.is_match('full_record', test_data), equal_to(True))

        test_obj = object()
        assert_that(a_matcher.is_match('full_record', test_obj), equal_to(True))

        assert_that(a_matcher.is_match('full_record', None), equal_to(True))

        assert_that(a_matcher.is_match('full_record', 1), equal_to(True))

        assert_that(a_matcher.is_match('fish', 1), equal_to(True))

        assert_that(a_matcher.is_match('dog', 'cat'), equal_to(True))


class TestEqualTo(TestCase):
    def test_is_match_single(self):
        test_data_record = {'name': 'Scarlet Shelton'}
        name_check = EqualTo('name')

        target_value = 'Scarlet Shelton'
        assert_that(name_check.is_match(target_value, test_data_record),
                    equal_to(True),
                    "Is target value in test data?")

        target_value = 'Bob Fisher'
        assert_that(name_check.is_match(target_value, test_data_record),
                    equal_to(False),
                    "Is target value in test data?")

    def test_empty_list_raises_error(self):
        test_data_record = {'name': 'Scarlet Shelton'}

        target_value = []
        name_check = EqualTo('name')

        with self.assertRaises(NotImplementedError):
            name_check.is_match(target_value, test_data_record)

    def test_is_match_list(self):
        test_data_record = {'name': 'Scarlet Shelton'}
        name_check = EqualTo('name')

        # Test a single item list
        target_value = ['Scarlet Shelton']
        self.assertTrue(name_check.is_match(target_value, test_data_record),
                        "Check against single item list")

        # Test successful, but look for one of many people
        target_value = ['Rudy Stout', 'Todd Lee', 'Scarlet Shelton']
        self.assertTrue(name_check.is_match(target_value, test_data_record),
                        "Check against multi item list")

        # Remove Scarlet and test again, should not be found
        target_value.pop(2)
        self.assertFalse(name_check.is_match(target_value, test_data_record), "Check against list")

    def test_is_key_not_in_data(self):
        test_data_record = {'full_name': 'Scarlet Shelton'}

        # Test a single item list
        target_value = ['Scarlet Shelton']
        name_check = EqualTo('name')

        self.assertFalse(name_check.is_match(target_value, test_data_record),
                         "Check against single item list")


class TestStartsWith(TestCase):
    def test_dumb(self):
        self.assertTrue(True)

    def test_is_key_not_in_data(self):
        test_data_record = {'rating': 'Superduper'}

        # Test a single item list
        target_value = ['Super']
        name_check = StartsWith('name')

        self.assertFalse(name_check.is_match(target_value, test_data_record),
                         "looking at field not in data record")

    def test_is_match_multiple_values(self):
        test_data_record = {'equipment': 'baseball'}
        ball_starts_with = StartsWith('equipment')

        # Test a single item list
        target_value = ['base']
        self.assertTrue(ball_starts_with.is_match(target_value, test_data_record),
                        "find one of the balls")

        # Test a longer list
        target_value = ['foot', 'soccer', 'base']
        self.assertTrue(ball_starts_with.is_match(target_value, test_data_record),
                        "find one of the balls")

        # Test a longer list, that will fail
        target_value = ['foot', 'soccer', 'basket']
        self.assertFalse(ball_starts_with.is_match(target_value, test_data_record),
                         "No balls to find")

    def test_is_match_single_value(self):
        test_data_record = {'rating': 'Superduper'}

        # Test a single item list
        target_value = 'Super'
        rating_starts_with = StartsWith('rating')

        self.assertTrue(rating_starts_with.is_match(target_value, test_data_record),
                        "looking at field not in data record")

    def test_is_match_convert_to_str(self):
        test_data_record = {'department': 11223344}
        dept_starts_with = StartsWith('department')

        # Test a single item
        target_value = '1122'
        self.assertTrue(dept_starts_with.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item list
        target_value = ['1122']
        self.assertTrue(dept_starts_with.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a multiple item list
        target_value = ['2222', '1122', '3333']
        self.assertTrue(dept_starts_with.is_match(target_value, test_data_record),
                        "find one of departments")

        # Test a single item  -- No Match
        target_value = '122'
        self.assertFalse(dept_starts_with.is_match(target_value, test_data_record),
                         "No-Match - one of departments")

    def test_is_match_empty_list(self):
        test_data_record = {'department': 11223344}
        dept_starts_with = StartsWith('department')

        target_value = []

        with self.assertRaises(NotImplementedError):
            dept_starts_with.is_match(target_value, test_data_record)


class TestGreaterThan(TestCase):
    def test_dumb(self):
        self.assertTrue(True)

    def test_is_key_not_in_data(self):
        test_data_record = {'my_number': 5}
        number_gt_check = GreaterThan('salary')

        # Test a single item list
        target_value = [18]
        self.assertFalse(number_gt_check.is_match(target_value, test_data_record),
                         "looking at field not in data record")

    def test_is_gt_single_value(self):
        test_data_record = {'my_number': 5}
        number_gt_check = GreaterThan('my_number')

        # Test a single item list
        target_value = 4
        self.assertTrue(number_gt_check.is_match(target_value, test_data_record),
                        "looking at field not in data record")

        # Test a single item list
        target_value = 10
        self.assertFalse(number_gt_check.is_match(target_value, test_data_record),
                         "looking at field not in data record")

    def test_is_gt_list_value(self):
        test_data_record = {'my_number': 5}
        number_gt_check = GreaterThan('my_number')

        # Test a single item list
        target_value = [4]
        self.assertTrue(number_gt_check.is_match(target_value, test_data_record),
                        "looking at field not in data record")

        # Test a single item list
        target_value = [10]
        self.assertFalse(number_gt_check.is_match(target_value, test_data_record),
                         "looking at field not in data record")

    def test_empty_list_raise_error(self):
        test_data_record = {'department': 11223344}
        dept_gt = GreaterThan('department')

        target_value = []
        with self.assertRaises(NotImplementedError):
            dept_gt.is_match(target_value, test_data_record)

    def test_multiple_vals_raise_error(self):
        test_data_record = {'department': 11223344}
        dept_gt = GreaterThan('department')

        target_value = [1, 2, 3, 4]
        with self.assertRaises(NotImplementedError):
            dept_gt.is_match(target_value, test_data_record)
