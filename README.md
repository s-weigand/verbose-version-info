# verbose-version-info

<!-- [![PyPi Version](https://img.shields.io/pypi/v/verbose_version_info.svg)](https://pypi.org/project/verbose-version-info/) -->
<!-- [![Conda Version](https://img.shields.io/conda/vn/conda-forge/verbose-version-info.svg)](https://anaconda.org/conda-forge/verbose-version-info) -->
<!-- [![Supported Python Versions](https://img.shields.io/pypi/pyversions/verbose_version_info.svg)](https://pypi.org/project/verbose-version-info/) -->

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Actions Status](https://github.com/s-weigand/verbose-version-info/workflows/Tests/badge.svg)](https://github.com/s-weigand/verbose-version-info/actions)
[![Documentation Status](https://readthedocs.org/projects/verbose-version-info/badge/?version=latest)](https://verbose-version-info.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/s-weigand/verbose-version-info/branch/main/graph/badge.svg)](https://codecov.io/gh/s-weigand/verbose-version-info)
[![Documentation Coverage](https://raw.githubusercontent.com/s-weigand/verbose-version-info/main/docs/_static/interrogate_badge.svg)](https://github.com/s-weigand/verbose-version-info)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=s-weigand/verbose-version-info)](https://dependabot.com)

[![All Contributors](https://img.shields.io/github/all-contributors/s-weigand/verbose-version-info)](#contributors)
[![Code style Python: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Generate verbose version information for python packages

- Free software: Apache Software License 2.0
- Documentation: https://verbose-version-info.readthedocs.io.

## Features

Implemented

- Basic version retrieval
- Customizable string for not found version
- Commit_id for `pip install git+<url>`
- Split off cli to an extra
- Detect `pip install -e` installation and get path
- commit id for `pip install -e .` if `.git` exists
- commit id for `pip install .` if `.git` exists
- Determine dist time for `pip install .` (needed for better commit_id)
- get commit id for `pip install .` if `.git` exists, for the closest commit at installation time
- use find_url_info in vv_info for tarball installation

TODO

- Add dist_mtime time to VerboseVersionInfo
- Add warning if repo of editable install is dirty (`git status -s != ""` )
- Reset settings function (mostly notebook showoff)
- setting formatter: Mapping[str, format_function] (used for sha)
- extract minimal required versions (useful for CI tests, of the min version)
- export minimal requirements to file (pip or conda style)
- add conda support
- create github markdown summary

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/s-weigand"><img src="https://avatars.githubusercontent.com/u/9513634?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sebastian Weigand</b></sub></a><br /><a href="https://github.com/s-weigand/verbose-version-info/commits?author=s-weigand" title="Code">💻</a> <a href="#ideas-s-weigand" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-s-weigand" title="Maintenance">🚧</a> <a href="#projectManagement-s-weigand" title="Project Management">📆</a> <a href="#infra-s-weigand" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/s-weigand/verbose-version-info/commits?author=s-weigand" title="Tests">⚠️</a> <a href="https://github.com/s-weigand/verbose-version-info/commits?author=s-weigand" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
