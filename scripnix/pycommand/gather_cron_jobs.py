""" Scripnix gather-cron-jobs command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import collections
import pwd
from .command import check_root_user, common_command_and_options, read_configuration


COMMAND_NAME = "gather-cron-jobs"
Crontab = collections.namedtuple("Crontab", "minute hour day_of_the_month month day_of_the_week user command")


def format_crontab_table(crontabs, delimiter=None, header=False):
    _, _, _ = crontabs, delimiter, header
    return ""


def gather_single_user_crontabs():
    return []


def gather_system_crontabs():
    return []


def gather_user_crontabs(users):
    _ = users
    return []


@common_command_and_options(command_name=COMMAND_NAME)
@click.option("--delimiter", "-d", help="Column delimiter character(s). If omitted, the output is space-aligned.")
@click.option("--header", "-h", is_flag=True, help="Display the table header row.")
def main(delimiter, header):
    """ Gather all of the system and user crontab schedules and display them in a consolidated table (space-aligned by default, or delimited
        if so specified: minute (m), hour (h), day of the month (dom), month (mon), day of the week (dow), user, and command.

        Must be run as the root user.

        The gather-cron-jobs command is part of Scripnix.
    """
    check_root_user(command_name=COMMAND_NAME)
    config = read_configuration()
    print(config)

    consolidated_crontab = gather_system_crontabs()
    consolidated_crontab.extend(gather_user_crontabs(users=[p.pw_name for p in pwd.getpwall()]))
    click.echo(format_crontab_table(consolidated_crontab, delimiter, header))
