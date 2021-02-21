"""Console script for verbose_version_info."""
import sys

try:
    import click
except ImportError:
    raise ImportError(
        "The requirements for the cli usage aren't installed.\n"
        "Install verbose-version-info with the cli extras e.g.:\n"
        "`pip install verbose-version-info[cli]`"
    )


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
    click.echo("Not yet Implemented!")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
