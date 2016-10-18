""" Scripnix hyphenate command
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import sys
from .command import common_command_and_options


COMMAND_NAME = "hyphenate"


@common_command_and_options(command_name=COMMAND_NAME, add_dry_run=False)
def main():
    """ Translate the given filenames (via stdin) into their equivalent, filesystem-safe, hyphenated versions.

        The hyphenate command is part of Scripnix.
    """
    for line in sys.stdin:
        click.echo(line.strip())


if __name__ == '__main__':
    main()
