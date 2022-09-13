#!/usr/bin/env python

"""Tests for `src` package."""


import unittest

from click.testing import CliRunner
from deftlariat.scripts import cli
from hamcrest import *


class TestSrc(unittest.TestCase):
    """Tests for `src` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.deft_cli)
        print(result.output)
        assert result.exit_code == 0
        assert 'deft lariats' in result.output
        help_result = runner.invoke(cli.deft_cli, ['--help'])
        assert help_result.exit_code == 0
        assert_that(help_result.output, string_contains_in_order('--version', '--help'))

