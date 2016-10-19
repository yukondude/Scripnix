#!/usr/bin/env python
""" Scripnix setuptools configuration.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import scripnix


HERE = os.path.abspath(os.path.dirname(__file__))


def gather_console_scripts():
    """ Return the list of the project's console script entry points.
    """
    console_scripts = []
    command_path = 'scripnix/pycommand'
    full_command_path = os.path.join(HERE, command_path)
    package_path = command_path.replace('/', '.')

    for file_name in [f for f in os.listdir(full_command_path) if os.path.isfile(os.path.join(full_command_path, f))]:
        if file_name in ('__init__.py', 'command.py'):
            continue

        command_module = os.path.splitext(file_name)[0]
        command_name = command_module.replace('_', '-')
        console_scripts.append("{}={}.{}:main".format(command_name, package_path, command_module))

    return console_scripts


def gather_requirements():
    """ Return the list of required packages and versions from requirements.txt.
    """
    return [pkg.strip() for pkg in open(os.path.join(HERE, "requirements.txt"), 'r').readlines()]


# noinspection PyAttributeOutsideInit
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["--cov=scripnix.pycommand", "--cov-report=term-missing"]
        self.test_suite = True

    def run_tests(self):
        # noinspection PyPackageRequirements
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


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
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Unix Shell",
        "Topic :: System",
        "Topic :: System :: Archiving",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    cmdclass={'test': PyTest},
    description=scripnix.__doc__,
    entry_points={
        'console_scripts': gather_console_scripts(),
    },
    extras_require={
        'testing': ["pytest"],
    },
    include_package_data=True,
    install_requires=gather_requirements(),
    license="GPLv3",
    long_description="See README.md.",
    name="Scripnix",
    packages=["scripnix"],
    platforms=["MacOS", "Linux"],
    tests_require=["pytest", "pytest-cov"],
    url="https://yukondude.github.io/Scripnix/",
    version=scripnix.__version__
)
