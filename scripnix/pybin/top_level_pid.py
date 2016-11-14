""" Scripnix top-level-pid command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

import click
import psutil

from scripnix.util.command import common_command_and_options


COMMAND_NAME = "top-level-pid"


def penultimate_pid(pid):
    """ Recursively look up the parent PID and return the last PID found before pid==1 (init or launchd) is encountered.
    """
    if not pid:
        pid = os.getpid()

    if pid == 1:
        return pid

    try:
        ppid = psutil.Process(pid).ppid()
    except ValueError:
        raise click.ClickException("Process ID '{}' must be a positive integer".format(pid))
    except psutil.NoSuchProcess:
        raise click.ClickException("Process ID '{}' does not exist.".format(pid))

    if ppid == 1:
        return pid
    else:
        return penultimate_pid(ppid)


@common_command_and_options(command_name=COMMAND_NAME)
@click.option('--pid', '-p', default=0, help="Process ID (PID) to look up.")
def main(pid):
    """ Return the top-level parent Process ID (PID) for the given PID (below the init or launchd process). If a PID is not specified, use
        the current process.

        The top-level-pid command is part of Scripnix.
    """
    click.echo(penultimate_pid(pid))
