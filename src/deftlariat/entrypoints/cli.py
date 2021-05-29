"""Console script for src."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for deft lariats."""
    click.echo(" Get ready to lasso some data with deft lariats! ")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
