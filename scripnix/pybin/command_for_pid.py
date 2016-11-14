""" Scripnix command-for-pid command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

import click
import psutil

from scripnix.util.command import common_command_and_options


COMMAND_NAME = "command-for-pid"


def command_name(pid):
    """ Return the command name for the given Process ID (PID).
    """
    if not pid:
        pid = os.getpid()

    try:
        return psutil.Process(pid).name()
    except ValueError:
        raise click.ClickException("Process ID '{}' must be a positive integer.".format(pid))
    except psutil.NoSuchProcess:
        raise click.ClickException("Process ID '{}' does not exist.".format(pid))


@common_command_and_options(command_name=COMMAND_NAME)
@click.argument('pid', default=0)
def main(pid):
    """ Return the command name for the given Process ID (PID). If a PID is not specified, use the current process.

        The command-for-pid command is part of Scripnix.
    """
    click.echo(command_name(pid))
