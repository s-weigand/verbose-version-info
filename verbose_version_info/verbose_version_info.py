"""Main module."""
from verbose_version_info.metadata_compat import distribution


def basic_version(distribution_name: str) -> str:
    """Retrieve the basic version of a distribution.

    Parameters
    ----------
    distribution_name : str
        [description]

    Returns
    -------
    str
        Version string of the distribution
    """
    return distribution(distribution_name).version
