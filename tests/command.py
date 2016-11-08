""" Scripnix command options unit testing functions
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import re

from click.testing import CliRunner

from scripnix import __version__


HELP_OPTION_REGEX = re.compile(r"Usage:.+The (\S+) command.+Scripnix\..+Show this message and exit\.$")


def common_help_option(command_entry, command_name):
    """ Test help message for both standard option switches."""
    def version_option_switch(option_switch):
        runner = CliRunner()
        result = runner.invoke(command_entry, [option_switch])
        assert result.exit_code == 0
        match = HELP_OPTION_REGEX.match(result.output.replace("\n", ""))
        assert match.group(1) == command_name

    version_option_switch("-h")
    version_option_switch("--help")


VERSION_OPTION_REGEX = re.compile(r"The (\S+).+Scripnix.+(\d+\.\d+\.\d+)\.Copyright.+\.$")


def common_version_option(command_entry, command_name):
    """ Test version message for both standard option switches."""
    def version_option_switch(option_switch):
        runner = CliRunner()
        result = runner.invoke(command_entry, [option_switch])
        assert result.exit_code == 0
        match = VERSION_OPTION_REGEX.match(result.output.replace("\n", ""))
        assert match.group(1) == command_name
        assert match.group(2) == __version__

    version_option_switch("-V")
    version_option_switch("--version")
