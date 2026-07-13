"""Console script for PyDeftLariats."""
import json
import sys

import click

from deftlariat import AnyOf, EqualTo, MatcherType, NumberComparer, __version__


@click.group(no_args_is_help=True)
@click.version_option(version=__version__)
def deft_cli():
    """Console script for deft lariats."""
    pass


@deft_cli.command()
@click.option('--data-file',
              help='file to work with',
              type=click.File('r'),
              default=sys.stdin)
def example_coingecko(data_file) -> None:
    """
    Coin Gecko Example. Demonstrate how to use the data filter with a list of dictionaries from
    coingecko.com API. Return records that match any one of three configured filters.
    """
    click.echo("Example One - Data Filter.  \nThis example will search the input list of dictionaries for "
               "records that match any of three filters, combined with the AnyOf combinator.\n\n"
               "The three filters are:\n"
               "1. EqualTo - Check if the value of a the `symbol` field is equal to a target value `OTCMKTS:FRMO`.\n"
               "2. NumberComparer - Check if the value of the `total_holdings` field is greater than or equal to "
               " the target value: `1000`\n"
               "3. NumberComparer - Check if the value of the `percentage_of_total_supply` field is greater than "
               "or equal to the target value: `0.1`\n"
               "Matching records will be printed to stdout.\n\n\n"
               )

    with data_file as f:
        try:
            # First read the data as a string
            content = f.read()

            # Check if there's any content
            if not content.strip():
                # No Data on stdin, so return
                click.echo("No Data found - Either File or stdin")
                return

            # Then parse it as JSON
            data = json.loads(content)
            # If data is not a list, wrap it in a list
            if not isinstance(data, list):
                data = [data]
        except json.JSONDecodeError as e:
            click.echo(f"Error parsing JSON: {e}")
            return

    combined = AnyOf(
        EqualTo('symbol', 'OTCMKTS:FRMO'),
        NumberComparer('total_holdings', MatcherType.GREATER_THAN_EQUAL_TO, 1000),
        NumberComparer('percentage_of_total_supply', MatcherType.GREATER_THAN_EQUAL_TO, 0.1),
    )
    for x in data:
        if combined.is_match(x):
            click.echo(f"Data Filter hit for record:\n{x}\n\n")
