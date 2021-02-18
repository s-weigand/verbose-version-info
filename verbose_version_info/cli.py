"""Console script for verbose_version_info."""
import sys

import click


@click.command()
def main(args=None) -> int:
    """Console script for verbose_version_info.

    Parameters
    ----------
    args : list, optional
        Commandlineargs, by default None

    Returns
    -------
    int
        Returncode
    """
    click.echo("Replace this message by putting your code into " "verbose_version_info.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
