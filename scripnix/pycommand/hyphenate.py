""" Scripnix hyphenate command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import re
import sys

import click

from scripnix.util.command import common_command_and_options


COMMAND_NAME = "hyphenate"

# Matches one or more non-word (not including underscore or period) characters.
NON_WORD_REGEX = re.compile(r"[^\w.]+")


def hyphenate(lines, delimiter):
    """ Return the list of lines with all non-word characters replaced by the given delimiter.
    """
    # Replace non-word characters by splitting the string at sequences of them and then joining the non-empty fragments together using the
    # delimiter.
    return [delimiter.join(w for w in NON_WORD_REGEX.split(l) if w) for l in lines]


@common_command_and_options(command_name=COMMAND_NAME)
@click.option('--delimiter', '-d', default='-', show_default=True, help="Word delimiter character(s).")
@click.argument('text', nargs=-1)
def main(delimiter, text):
    """ Translate the given text argument(s) (or use the input lines from STDIN) into the equivalent, filesystem-safe, hyphenated versions.

        The hyphenate command is part of Scripnix.
    """
    if text:
        lines = text
    else:
        lines = sys.stdin

    for line in hyphenate(lines=lines, delimiter=delimiter):
        click.echo(line.strip())
