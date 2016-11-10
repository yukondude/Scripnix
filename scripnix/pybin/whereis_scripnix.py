""" Scripnix whereis-scripnix command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

import click

from scripnix.util.command import common_command_and_options


COMMAND_NAME = "whereis-scripnix"
PACKAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@common_command_and_options(command_name=COMMAND_NAME)
def main():
    """ Return the full, absolute path to the Scripnix package.

        The whereis-scripnix command is part of Scripnix.
    """
    click.echo(PACKAGE_PATH)
