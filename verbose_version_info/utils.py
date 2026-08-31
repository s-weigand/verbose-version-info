"""Utility modules with convenience functions."""

from datetime import datetime
from functools import lru_cache
from importlib.metadata import Distribution
from importlib.metadata import PackageNotFoundError
from importlib.metadata import PackagePath
from importlib.metadata import distribution as _distribution
from os import PathLike
from pathlib import Path
from typing import List
from typing import Union

from verbose_version_info import SETTINGS


class NotFoundDistribution(Distribution):
    """Distribution of package which couldn't be found.

    This class is used not to repeat the try-except pattern over and
    over again.
    If a package isn't found an instance of this class is returned by
    :func:`get_distribution` and the parts of the API which are used by
    ``verbose_version_info`` are kept intact for the way they are used.

    See Also
    --------
    get_distribution
    """

    def read_text(self, filename: str) -> None:
        """Attempt to load metadata file given by the name.

        Just added to satisfy mypy, since the superclass one is
        an ``abstractmethod``.

        Parameters
        ----------
        filename : str
            Name of a file in the distribution

        Returns
        -------
        None
        """
        return None

    def locate_file(self, path: Union[PathLike, str]) -> PathLike:
        """Given a path to a file in this distribution, return a path to it.

        Just added to satisfy mypy, since the superclass one is
        an ``abstractmethod``.

        Parameters
        ----------
        path: PathLike | str
            Path to a file.

        Returns
        -------
        PathLike
            Just the initial ``path`` ensure to be type ``PathLike``.
        """
        return Path(path) if isinstance(path, str) else path

    @property
    def version(self) -> str:
        """User set string if no version was found.

        Default "Unknown".

        Returns
        -------
        str
            SETTINGS["not_found_version_str"]
        """
        return SETTINGS["not_found_version_str"]  # type: ignore[return-value]

    @property
    def files(self) -> list:
        """List of files in this distribution.

        Not having found a distribution is (in this usecase)
        equivalent to it not having any files.

        Returns
        -------
        list
            Empty list
        """
        return []

    @property
    def requires(self) -> list:
        """List of generated requirements specified for this Distribution.

        Not having found a distribution is (in this usecase)
        equivalent to it not having any requirements.

        Returns
        -------
        list
            Empty list
        """
        return []


@lru_cache()
def distribution(
    distribution_name: str,
) -> Distribution:
    """Get the ``Distribution`` instance for the named package.

    Parameters
    ----------
    distribution_name : str
        The name of the package as a string.

    Returns
    -------
    Distribution
        Distribution instance of the package
    """
    try:
        return _distribution(distribution_name)
    except PackageNotFoundError:
        return NotFoundDistribution()


def dist_files(
    distribution_name: str,
) -> List[PackagePath]:
    """List of PackagePaths even if the package is broken.

    This is a convenience function since Distribution.files
    could be None.
    I.e. if RECORD for dist-info or SOURCES.txt for egg-info.

    See: importlib.metadata.Distribution.files

    Parameters
    ----------
    distribution_name : str
        The name of the package as a string.

    Returns
    -------
    List[PackagePath]
        Paths of files used by the package.
    """
    dist_files = distribution(distribution_name).files
    return dist_files if dist_files is not None else []


def _datetime_now() -> datetime:
    """Wrap ``datetime.now`` to easily mock it for testing.

    Returns
    -------
    datetime
        Current datetime.
    """
    return datetime.now()
