""" Scripnix os-name command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import platform
from .command import common_command_and_options


COMMAND_NAME = "os-name"


def operating_system(translate=True):
    """ Return the operating system platform name (e.g., linux, macos, windows).
    """
    os_name = platform.system().lower()

    if translate and os_name == "darwin":
        return "macos"

    return os_name


@common_command_and_options(command_name=COMMAND_NAME)
@click.option("--no-translate", "-T", is_flag=True, help="Do not translate the original operating system string to its more familiar name.")
def main(no_translate):
    """ Return the operating system platform name.

        The os-name command is part of Scripnix.
    """
    click.echo(operating_system(not no_translate))
