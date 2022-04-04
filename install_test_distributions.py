"""Helper script to install the dummy test packages.

The problematic one being: ``tests/dummy_packages/local_install with spaces in path``
which I can't get to be installed with ``requirements_dev.txt`` alone.

The ones that could be installed via ``requirements_dev.txt`` need to be installed here
for dependabot to work properly.
"""
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from textwrap import dedent

# dummy distributions for testing
test_packages = dedent(
    """\
    git+https://github.com/s-weigand/git-install-test-distribution.git
    -e tests/dummy_packages/editable_install_setup_cfg
    -e tests/dummy_packages/editable_install_setup_py
    -e tests/dummy_packages/editable_install_src_pattern
    -e tests/dummy_packages/editable_install_with_dotgit
    tests/dummy_packages/local_install
    tests/dummy_packages/local_install_src_pattern
    tests/dummy_packages/local_install_with_dotgit
    https://github.com/s-weigand/tarball-test-distribution/archive/main.zip
    """
)

with NamedTemporaryFile("w+") as tmp_file:
    subprocess.run(["pip", "install", "-r", Path(tmp_file.name).as_posix()])

subprocess.run(["pip", "install", "tests/dummy_packages/local_install with spaces in path"])
