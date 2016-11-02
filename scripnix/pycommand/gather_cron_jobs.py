""" Scripnix gather-cron-jobs command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import collections
import pwd
import re
import subprocess
from .command import check_root_user, common_command_and_options, read_configuration


COMMAND_NAME = "gather-cron-jobs"

CRON_COMMENT_REGEX = re.compile(r"^(\s*#.*|\s*)$")
CRON_RULE_PREFIX = r"^\s*"
CRON_RULE_TERM = r"(\S+)\s+"
CRON_RULE_SUFFIX = r"(.+?)\s*$"
SYSTEM_CRON_RULE_REGEX = re.compile(CRON_RULE_PREFIX + CRON_RULE_TERM * 6 + CRON_RULE_SUFFIX)
USER_CRON_RULE_REGEX = re.compile(CRON_RULE_PREFIX + CRON_RULE_TERM * 5 + CRON_RULE_SUFFIX)

USER_CRON_CMD = "crontab -u {user} -l"

CronRule = collections.namedtuple("CronRule", "minute hour day_of_the_month month day_of_the_week user command")


def parse_crontab_rule(rule, user=None):
    """ Parse a single line from a crontab file and return it as a CronRule namedtuple. If user is given, assume the line doesn't contain a
        user column. Return None if the line is empty, a comment, or can't be parsed.
    """
    if CRON_COMMENT_REGEX.match(rule) is not None:
        return None

    crontab_regex = USER_CRON_RULE_REGEX if user else SYSTEM_CRON_RULE_REGEX
    match = crontab_regex.match(rule)

    if match is None:
        return None

    user = user if user else match.group(6)
    command = match.group(6) if user else match.group(7)

    return CronRule(minute=match.group(1), hour=match.group(2), day_of_the_month=match.group(3), month=match.group(4),
                    day_of_the_week=match.group(5), user=user, command=command)


def format_crontab_table(crontabs, header=True, delimiter=None):
    _, _, _ = crontabs, delimiter, header  # noqa: F841

    # crontab_rules = re.sub(r"\s+", "")

    return "\n".join([str(c) for c in crontabs])


def gather_single_user_crontabs(user):
    try:
        crontabs = subprocess.check_output([USER_CRON_CMD.format(user=user)], shell=True, stderr=subprocess.DEVNULL).decode("utf-8")
    except subprocess.CalledProcessError:
        return None

    return filter(None, [parse_crontab_rule(rule, user) for rule in crontabs.split("\n")])


def gather_system_crontabs():
    return []


def gather_user_crontabs(users):
    crontabs = []

    for user in users:
        user_crontabs = gather_single_user_crontabs(user)

        if user_crontabs:
            crontabs.extend(user_crontabs)

    return crontabs


@common_command_and_options(command_name=COMMAND_NAME)
@click.option("--delimiter", "-d", help="Column delimiter character(s). If omitted, the output is space-aligned.")
@click.option("--no-header", "-H", is_flag=True, help="Don't display the table header row.")
def main(delimiter, no_header):
    """ Gather all of the system and user crontab schedules and display them in a consolidated table (space-aligned by default, or delimited
        if so specified: minute (m), hour (h), day of the month (dom), month (mon), day of the week (dow), user, and command.

        Must be run as the root user.

        The gather-cron-jobs command is part of Scripnix.
    """
    check_root_user(command_name=COMMAND_NAME)
    config = read_configuration()

    consolidated_crontab = gather_system_crontabs()
    consolidated_crontab.extend(gather_user_crontabs(users=[p.pw_name for p in pwd.getpwall()]))
    click.echo(format_crontab_table(consolidated_crontab, not no_header, delimiter))
