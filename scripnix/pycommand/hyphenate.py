""" Scripnix hyphenate command
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import re
import sys
from .command import common_command_and_options


COMMAND_NAME = "hyphenate"

# Matches one or more non-word (not including underscore or period) characters.
NON_WORD_REGEX = re.compile(r"[^\w.]+")


def hyphenate(lines, delimiter):
    """ Return the list of lines with all non-word characters replaced by the given delimiter.
    """
    # Replace non-word characters by splitting the string at sequences of them and then joining the non-empty ones back using the delimiter.
    return [delimiter.join(w for w in NON_WORD_REGEX.split(l) if w) for l in lines]


@common_command_and_options(command_name=COMMAND_NAME, add_dry_run=False)
@click.option('--delimiter', '-d', default='-', show_default=True, help="Word delimiter character(s).")
def main(delimiter):
    """ Translate the given input (via STDIN) into its equivalent, filesystem-safe, hyphenated version.

        The hyphenate command is part of Scripnix.
    """
    for line in hyphenate(lines=sys.stdin, delimiter=delimiter):
        click.echo(line.strip())


if __name__ == '__main__':
    main()
