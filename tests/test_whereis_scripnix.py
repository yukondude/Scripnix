""" Scripnix whereis-scripnix command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

from click.testing import CliRunner

from scripnix.pybin.whereis_scripnix import COMMAND_NAME, main
from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0

    path = result.output.strip()
    assert os.path.isdir(path)
    assert os.path.isfile(os.path.join(path, "conf/conf.bash"))


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
