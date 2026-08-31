"""Helper script to install the dummy test packages.

The problematic one being: ``tests/dummy_packages/local_install with spaces in path``
which I can't get to be installed with ``requirements_dev.txt`` alone.

The ones that could be installed via ``requirements_dev.txt`` need to be installed here
for dependabot to work properly.
"""

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
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

with TemporaryDirectory() as tmpdirname:
    tmp_file = Path(tmpdirname).resolve() / "vv-info-test-requirements.txt"
    tmp_file.write_text(test_packages)
    subprocess.run(["pip", "install", "-r", tmp_file.as_posix()], check=True)

subprocess.run(
    ["pip", "install", "tests/dummy_packages/local_install with spaces in path"], check=True
)
