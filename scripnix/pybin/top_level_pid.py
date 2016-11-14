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
        raise click.ClickException("Process ID '{}' must be a positive integer.".format(pid))
    except psutil.NoSuchProcess:
        raise click.ClickException("Process ID '{}' does not exist.".format(pid))

    if ppid in (0, 1) or pid == ppid:
        return pid
    else:
        try:
            return penultimate_pid(ppid)
        except RuntimeError:
            # Recursion depth reached: give up and return the last parent PID found.
            return ppid


@common_command_and_options(command_name=COMMAND_NAME)
@click.argument('pid', default=0)
def main(pid):
    """ Return the top-level parent (below the init or launchd process) Process ID (PID) for the given PID. If a PID is not specified, use
        the current process.

        The top-level-pid command is part of Scripnix.
    """
    click.echo(penultimate_pid(pid))
