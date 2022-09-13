"""Console script for src."""
import sys
import json

import click

from deftlariat import __version__
from deftlariat import EqualTo, NumberComparer, MatcherType


@click.group()
@click.version_option(version=__version__)
def deft_cli():
    """Console script for deft lariats."""


@deft_cli.command()
def hello(name: str) -> None:
    click.echo(f"Hello {str}")


zip_code_list = ['']


@deft_cli.command()
@click.option('--data-file',
              help='file to work with',
              type=click.File('r'),
              default=sys.stdin)
def example_one(data_file) -> None:

    with data_file as f:
        if f.isatty():
            # No Data on stdin, so return
            click.echo("No Data found - Either File or stdin")
            return
        # data = f.read()  # If a proper json lost, load into list
        data = json.load(f)

    # TODO: Assume stream is a json list
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
            click.echo(f"Data Filter hit: record:\n{x}\n\n")

