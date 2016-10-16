""" Setuptools configuration.
    This file is part of Scripnix. See LICENSE for details.
"""
from setuptools import setup
import scripnix


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
#    entry_points={
#        'console_scripts': [
#        ],
#    },
    include_package_data=True,
    install_requires=[
        "click>=6.6",  # TODO: read from requirements.txt
    ],
    license="GPLv3",
    long_description="See README.md.",
    name="Scripnix",
    packages=['scripnix'],
    platforms=["MacOS", "Linux"],
    url="https://github.com/yukondude/Scripnix/",
    version=scripnix.__version__
)
