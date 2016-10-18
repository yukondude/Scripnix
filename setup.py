""" Scripnix setuptools configuration.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
from setuptools import setup
import scripnix


HERE = os.path.abspath(os.path.dirname(__file__))

REQUIREMENTS = [pkg.strip() for pkg in open(os.path.join(HERE, "requirements.txt"), 'r').readlines()]


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
    description=scripnix.__doc__,
    entry_points={
        'console_scripts': [
            'backup-file=scripnix.pycommand.backup_file:main',
        ],
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="GPLv3",
    long_description="See README.md.",
    name="Scripnix",
    packages=['scripnix'],
    platforms=["MacOS", "Linux"],
    url="https://yukondude.github.io/Scripnix/",
    version=scripnix.__version__
)
