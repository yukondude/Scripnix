#!/usr/bin/env python
""" Scripnix setuptools configuration.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import stat
import sys

import scripnix


if sys.version_info < (3, 3):
    sys.stderr.write("Scripnix requires Python 3.3 or higher.\n")
    sys.exit(1)


HERE = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(HERE, "README.rst"), encoding='utf-8') as f:
    long_description = f.read().strip()


def gather_console_scripts():
    """ Return the list of the project's console script entry points.
    """
    console_scripts = []
    command_path = "scripnix/pybin"
    full_command_path = os.path.join(HERE, command_path)
    package_path = command_path.replace("/", ".")

    for file_name in [fn for fn in os.listdir(full_command_path) if os.path.isfile(os.path.join(full_command_path, fn))]:
        if file_name in scripnix.NON_COMMANDS['pybin']:
            continue

        command_module = os.path.splitext(file_name)[0]
        command_name = command_module.replace("_", "-")
        console_scripts.append("{}={}.{}:main".format(command_name, package_path, command_module))

    return console_scripts


def gather_requirements(requirements_file_name):
    """ Return the list of required packages and versions from requirements.txt.
    """
    return [pkg.strip() for pkg in open(os.path.join(HERE, requirements_file_name), "r").readlines()]


def gather_scripts():
    """ Return the list of the project's shell scripts.
    """
    scripts = []
    script_path = "scripnix/shbin"
    full_script_path = os.path.join(HERE, script_path)

    for file_name in [fn for fn in os.listdir(full_script_path) if os.path.isfile(os.path.join(full_script_path, fn))]:
        if file_name in scripnix.NON_COMMANDS['shbin']:
            continue

        # Exclude non-executable files.
        if not stat.S_IXUSR & os.stat(os.path.join(full_script_path, file_name))[stat.ST_MODE]:
            continue

        scripts.append(os.path.join(script_path, file_name))

    return scripts


# noinspection PyAttributeOutsideInit
class PyTest(TestCommand):
    test_args = ["--cov=scripnix/pybin", "--cov=tests", "--cov-report=term-missing", "--cov-fail-under=80", "--flake8"]
    test_suite = True

    def finalize_options(self):
        TestCommand.finalize_options(self)

    def run_tests(self):
        # noinspection PyPackageRequirements
        import pytest
        sys.exit(pytest.main(self.test_args))


# noinspection PyAttributeOutsideInit
class PyCleanTest(PyTest):
    """ Same as PyTest, but clear the cache first.
    """
    test_args = ["--verbose", "--cache-clear", "--cov=scripnix/pybin", "--cov=tests", "--cov-report=term-missing",
                 "--cov-fail-under=80", "--flake8"]


setup(
    author="Dave Rogers",
    author_email="thedude@yukondude.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Unix Shell",
        "Topic :: System",
        "Topic :: System :: Archiving",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    cmdclass={
        'test': PyTest,
        'cleantest': PyCleanTest,
    },
    description=scripnix.__doc__.strip(),
    entry_points={
        'console_scripts': gather_console_scripts(),
    },
    extras_require={
        'testing': gather_requirements("requirements-test.txt"),
    },
    include_package_data=True,
    install_requires=gather_requirements("requirements.txt"),
    license="GPLv3",
    long_description=long_description,
    name="scripnix",
    packages=find_packages(),
    platforms=["MacOS", "Linux"],
    scripts=gather_scripts(),
    tests_require=gather_requirements("requirements-test.txt"),
    url="https://yukondude.github.io/Scripnix/",
    version=scripnix.__version__,
    zip_safe=False
)
