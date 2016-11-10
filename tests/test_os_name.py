""" Scripnix os-name command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click.testing import CliRunner

from scripnix.pybin.os_name import COMMAND_NAME, main

from .common import platform_name
from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_main_arguments():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0

    this_os = platform_name()
    assert result.output.strip() == ("macos" if this_os == "darwin" else this_os)


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
