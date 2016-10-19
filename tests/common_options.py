""" Scripnix common options unit testing functions
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click.testing import CliRunner
import re
from scripnix import __version__


def common_help_option(command_entry, command_name):
    """ Test help message for both standard option switches."""
    def version_option_switch(option_switch):
        runner = CliRunner()
        result = runner.invoke(command_entry, [option_switch])
        assert result.exit_code == 0
        match = re.match(r"Usage:.+The (\S+) command.+Scripnix\..+Show this message and exit\.$", result.output.replace("\n", ""))
        assert match.group(1) == command_name

    version_option_switch("-h")
    version_option_switch("--help")


def common_version_option(command_entry, command_name):
    """ Test version message for both standard option switches."""
    def version_option_switch(option_switch):
        runner = CliRunner()
        result = runner.invoke(command_entry, [option_switch])
        assert result.exit_code == 0
        match = re.match(r"The (\S+).+Scripnix.+(\d+\.\d+\.\d+)\.\nCopyright.+\.\n$", result.output, re.MULTILINE)
        assert match.group(1) == command_name
        assert match.group(2) == __version__

    version_option_switch("-V")
    version_option_switch("--version")
