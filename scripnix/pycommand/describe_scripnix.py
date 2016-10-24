""" Scripnix describe-scripnix command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import os
import subprocess
from .command import common_command_and_options


COMMAND_NAME = "describe-scripnix"


def collect_help_text(command):
    """ Return the output from the given command executed with the --help option switch.
    """
    return subprocess.check_output([command, "--help"]).decode("utf-8")


def format_command_help_text(command, help_text):
    """ Return the given command and help text formatted as GitHub-flavoured Markdown.
    """
    return "\n".join(["### `{}`".format(command), "```", help_text.rstrip("\n"), "```"])


def format_commands(path, exclusions):
    """ Return the help text output of all commands in the given path formatted as GitHub-flavoured Markdown. The commands are sorted by
        name and exclude any from the given list of file names.
    """
    commands = gather_commands(path, exclusions)
    command_help_texts = {command: collect_help_text(command) for command in commands}
    return "\n\n".join([format_command_help_text(c, command_help_texts[c]) for c in sorted(command_help_texts.keys())])


def gather_commands(path, exclusions):
    """ Return the list of the commands found in the given directory path, excluding any from the given list of file names.
    """
    commands = []

    for file_name in [f for f in os.listdir(path) if f not in exclusions and os.path.isfile(os.path.join(path, f))]:
        commands.append(os.path.splitext(file_name)[0].replace('_', '-'))

    return commands


@common_command_and_options(command_name=COMMAND_NAME)
def main():
    """ Generate descriptions of all of the Scripnix commands in Markdown format, suitable for appending to the Scripnix project's README.md
        file.

        The describe-scripnix command is part of Scripnix.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    click.echo(format_commands(path=here, exclusions=("__init__.py", "command.py")))
