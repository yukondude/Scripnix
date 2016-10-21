""" Scripnix install-scripnix command
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
from .command import common_command_and_options


COMMAND_NAME = "install-scripnix"


@common_command_and_options(command_name=COMMAND_NAME, add_dry_run=True)
@click.option("--verbose", "-v", is_flag=True, help="Display the commands as they are being executed.")
def main(dry_run, verbose):
    """ Install Scripnix for the current user. Global configuration settings (once installed by the root user) are stored under the
        /etc/scripnix/ directory. Per-user configuration settings, including for the root user, are stored under the ~/.scripnix/ directory
        and override the global settings. The installation can be re-run repeatedly, but will not overwrite existing configuration settings.

        The install-scripnix command is part of Scripnix.
    """
    pass
