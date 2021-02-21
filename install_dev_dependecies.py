"""Helper script to install all dev dependencies.

The problematic one being: ``tests/dummy_packages/local_install with spaces in path``
which I can't get to be installed with ``requirements_dev.txt`` alone.
"""
import subprocess

subprocess.run(["pip", "install", "-r", "requirements_dev.txt"])
subprocess.run(["pip", "install", "tests/dummy_packages/local_install with spaces in path"])
