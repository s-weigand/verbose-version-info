# Those dummy packages are only used for testing

The installation description assumes that your current path is the repo root.

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
- commit: `f2d32d41644de04122e478d6ef9639f5c2292eca`

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
