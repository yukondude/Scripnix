""" Scripnix os_name command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click.testing import CliRunner
import os
from scripnix.pycommand.os_name import COMMAND_NAME, main, operating_system
from .common_options import common_help_option, common_version_option


def platform_name():
    # noinspection PyUnresolvedReferences
    return os.uname().sysname.lower()  # A different method from that used by operating_system().


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_main_arguments():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0

    this_os = platform_name()
    assert result.output.strip() == ("macos" if this_os == "darwin" else this_os)


def test_operating_system():
    this_os = platform_name()

    os_with_translate = operating_system(translate=True)
    assert len(os_with_translate) > 0
    assert os_with_translate == ("macos" if this_os == "darwin" else this_os)

    os_without_translate = operating_system(translate=False)
    assert len(os_without_translate) > 0
    assert os_without_translate == this_os


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
