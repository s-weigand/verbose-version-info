"""Console script for verbose_version_info."""

try:
    import typer
except ImportError:
    raise ImportError(
        "The requirements for the cli usage aren't installed.\n"
        "Install verbose-version-info with the cli extras e.g.:\n"
        "`pip install verbose-version-info[cli]`"
    )

cli = typer.Typer(name="vvinfo")


@cli.command()
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
    print("Not yet Implemented!")
    return 0


if __name__ == "__main__":
    cli()
