# Those dummy packages are only used for testing

The installation description assumes that your current path is the repo root.

## git_install_test_distribution

package installed directly from git

- install: `pip install git+https://github.com/s-weigand/git-install-test-distribution.git`
- version: `0.0.2`
- commit: `a7f7bf28dbe9bfceba1af8a259383e398a942ad0`

## editable_install_setup_cfg

`setup.cfg` only package

- install: `pip install -e tests/dummy_packages/editable_install_setup_cfg`
- version: `0.0.3`

## editable_install_setup_py

`setup.py` only package

- install: `pip install -e tests/dummy_packages/editable_install_setup_py`
- version: `0.0.4`

## editable_install_src_pattern

src pattern package

- install: `pip install -e tests/dummy_packages/editable_install_src_pattern`
- version: `0.0.6`

## editable_install_with_dotgit

`setup.py` only package with a `.git` next to `setup.py`

- install: `pip install -e tests/dummy_packages/editable_install_with_dotgit`
- version: `0.0.5`
- commit_id (initial): `f2d32d41644de04122e478d6ef9639f5c2292eca`
- commit_id (latest): `f3c8d36715f7cd14dc73e6b3ae76cb2669c97b5f`

## local_install

example for a local installation from source

- install: `pip install local_install`
- version: `0.0.7`

## local_install_with_spaces_in_path

example for a local installation from source

- install: `pip install 'tests/dummy_packages/local_install with spaces in path'`
- version: `0.0.8`

## local_install_src_pattern

example for a local installation from source using src pattern

- install: `pip install tests/dummy_packages/local_install_src_pattern`
- version: `0.0.9`

## local_install_with_dotgit

example for a local installation from source with a `.git` next to `setup.py`

- install: `pip install tests/dummy_packages/local_install_with_dotgit`
- version: `0.0.10`
- commit_id (initial): `df5c1e9302972fa5732a320d4cdef478cf783b8f`
- commit_id (latest): `ff76038f76fcc106885cb9f19748e989d7d862b9`

## tarball_test_distribution

package installed from tarball url

- install: `pip install https://github.com/s-weigand/tarball-test-distribution/archive/main.zip`
- version: `0.0.11`
