""" Scripnix os-name command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click

from scripnix.util.command import common_command_and_options
from scripnix.util.common import operating_system


COMMAND_NAME = "os-name"


@common_command_and_options(command_name=COMMAND_NAME)
@click.option("--no-translate", "-T", is_flag=True, help="Do not translate the original operating system string to its more familiar name.")
def main(no_translate):
    """ Return the operating system platform name.

        The os-name command is part of Scripnix.
    """
    click.echo(operating_system(not no_translate))
