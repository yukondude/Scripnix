""" Scripnix install-scripnix command
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
from .command import common_command_and_options, is_root_user, USER_CONFIG_DIR, ROOT_CONFIG_DIR
import os
import socket
import stat


COMMAND_NAME = "install-scripnix"


def install_global(execute):
    """ Install global Scripnix configuration settings.
    """
    if not is_root_user():
        return

    hostname = socket.gethostname().split('.')[0].lower()
    config_path = os.path.abspath(ROOT_CONFIG_DIR)

    if not os.path.isdir(config_path):
        execute(os.mkdir, config_path, echo="mkdir {}".format(config_path))

    execute(os.chmod, config_path,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID | stat.S_IROTH | stat.S_IXOTH,
            echo="chmod a=rwx,g=rxs,o=rx {}".format(config_path))


# def install_per_user(execute):
#     """ Install per-user Scripnix configuration settings.
#     """
#     config_path = os.path.abspath(USER_CONFIG_DIR)


@common_command_and_options(command_name=COMMAND_NAME, add_dry_run=True)
@click.confirmation_option(prompt='Are you sure you want to install Scripnix?')
@click.option("--verbose", "-v", is_flag=True, help="Display the commands as they are being executed.")
def main(dry_run, verbose):
    """ Install Scripnix for the current user. Global configuration settings (once installed by the root user) are stored under the
        /etc/scripnix/ directory. Per-user configuration settings, including for the root user, are stored under the ~/.scripnix/ directory
        and override the global settings. The installation can be re-run repeatedly, but will not overwrite existing configuration settings
        (however file and directory permissions will be reset).

        The install-scripnix command is part of Scripnix.
    """
    def execute(fn, *args, echo):
        """ Call the given function with its arguments if this is not a dry run. If it is a dry run, or the verbose flag is set, echo the
            given text to STDOUT. By closing over these two flags within this function, the install functions are much less complicated.
        """
        if not dry_run:
            fn(*args)

        if dry_run or verbose:
            click.echo(echo)

    if dry_run:
        click.echo("{} would do the following:".format(COMMAND_NAME))
    elif verbose:
        click.echo("{} is performing the following:".format(COMMAND_NAME))

    install_global(execute)
    # install_per_user(execute)
