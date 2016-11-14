""" Scripnix describe-scripnix command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import re

from click.testing import CliRunner

import scripnix
from scripnix.pybin.describe_scripnix import COMMAND_NAME, main

from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_main():
    result = CliRunner().invoke(main)
    help_text = result.output
    assert len(help_text) > 0

    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(here, "../scripnix/pybin"))
    command_files = [f for f in os.listdir(path) if f not in scripnix.NON_COMMANDS['pybin'] and os.path.isfile(os.path.join(path, f))]
    commands = [os.path.splitext(f)[0].replace('_', '-') for f in command_files]

    for command in commands:
        assert re.search("^### `{}`$".format(command), help_text, re.MULTILINE) is not None
        assert re.search("^Usage: {}".format(command), help_text, re.MULTILINE) is not None


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
