""" Scripnix describe-scripnix command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import re
import subprocess

import click

import scripnix
from scripnix.util.command import common_command_and_options


COMMAND_NAME = "describe-scripnix"

PART_OF_SCRIPNIX_REGEX = re.compile(r"\s*The .+ command is part of Scripnix.")


def collect_help_text(command):
    """ Return the output from the given command executed with the --help option switch.
    """
    help_text = subprocess.check_output([command, "--help"]).decode("utf-8")
    return PART_OF_SCRIPNIX_REGEX.sub("", help_text)


def format_command_help_text(command, help_text):
    """ Return the given command and help text formatted as GitHub-flavoured Markdown.
    """
    return "\n".join(["### `{}`".format(command), "```", help_text.rstrip("\n"), "```"])


def format_commands(paths_exclusions):
    """ Return the help text output of all commands in the given path formatted as GitHub-flavoured Markdown. The commands are sorted by
        name and exclude any from the given list of file names.
    """
    commands = gather_commands(paths_exclusions)
    command_help_texts = {command: collect_help_text(command) for command in commands}
    return "\n\n".join([format_command_help_text(c, command_help_texts[c]) for c in sorted(command_help_texts.keys())])


def gather_commands(paths_exclusions):
    """ Return the list of the commands found in the given directory path, excluding any from the given list of file names.
    """
    commands = []

    for path, exclusions in paths_exclusions:
        for file_name in [f for f in os.listdir(path) if f not in exclusions and os.path.isfile(os.path.join(path, f))]:
            commands.append(os.path.splitext(file_name)[0].replace('_', '-'))

    return commands


@common_command_and_options(command_name=COMMAND_NAME)
def main():
    """ Generate descriptions of all of the Scripnix commands in Markdown format, suitable for appending to the Scripnix project's README.md
        file.

        The describe-scripnix command is part of Scripnix.
    """
    pybin_path = os.path.abspath(os.path.dirname(__file__))
    shbin_path = os.path.abspath(os.path.join(pybin_path, "../shbin"))
    paths_exclusions = ((pybin_path, scripnix.NON_COMMANDS['pybin']), (shbin_path, scripnix.NON_COMMANDS['shbin']))
    click.echo(format_commands(paths_exclusions))
