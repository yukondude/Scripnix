""" Scripnix gather-cron-jobs command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import collections
import pwd
import re
import subprocess
from .command import common_command_and_options
from .common import check_root_user, read_configuration


COMMAND_NAME = "gather-cron-jobs"

# Any crontab comment or blank line.
CRON_IGNORE_REGEX = re.compile(r"^(\s*#.*|\s*)$")

CRON_RULE_PREFIX = r"^\s*"
CRON_RULE_TERM = r"(\S+)\s+"
CRON_RULE_SUFFIX = r"(.+?)\s*$"
SYSTEM_CRON_RULE_REGEX = re.compile(CRON_RULE_PREFIX + CRON_RULE_TERM * 6 + CRON_RULE_SUFFIX)
USER_CRON_RULE_REGEX = re.compile(CRON_RULE_PREFIX + CRON_RULE_TERM * 5 + CRON_RULE_SUFFIX)

USER_CRON_CMD = "crontab -u {user} -l"

# Structure for a single cron rule.
CronRule = collections.namedtuple("CronRule", "minute hour day_of_the_month month day_of_the_week user command")

CRONTAB_HEADER = CronRule("m", "h", "dom", "mon", "dow", "user", "command")


def format_cron_rules_table(cron_rules, header, delimiter, do_sort):
    """ Return the given list of CronRule entries formatted as delimited lines of text, with an optional initial header line. Sort the lines
        by the hour and minute elements if do_sort is True.
    """
    if do_sort:
        cron_rules.sort(key=lambda e: (e.hour, e.minute))

    if header:
        cron_rules.insert(0, CRONTAB_HEADER)

    return "\n".join([delimiter.join(c) for c in cron_rules])


def gather_single_user_cron_rules(user):
    """ Return a list of parsed CronRule entries for the given user using the `crontab` shell command to do the work.
    """
    try:
        crontab = subprocess.check_output([USER_CRON_CMD.format(user=user)], shell=True, stderr=subprocess.DEVNULL).decode("utf-8")
    except subprocess.CalledProcessError:
        crontab = ""

    return parse_crontab(crontab, user)


def gather_system_cron_rules():
    # TODO: do the thing it's supposed to, you know, do.
    return []


def gather_user_cron_rules(users):
    """ Return a list of gathered CronRule entries for all of the users given.
    """
    user_rules = [gather_single_user_cron_rules(user) for user in users]
    return [rule for rules in user_rules for rule in rules]


def parse_cron_rule(rule, user=None):
    """ Parse a single line from a crontab file and return it as a CronRule namedtuple. If user is given, assume the line doesn't contain a
        user column. Return None if the line is empty, a comment, or can't be parsed.
    """
    if CRON_IGNORE_REGEX.match(rule) is not None:
        return None

    crontab_regex = USER_CRON_RULE_REGEX if user else SYSTEM_CRON_RULE_REGEX
    match = crontab_regex.match(rule)

    if match is None:
        return None

    cron_user = user if user else match.group(6)
    cron_command = match.group(6) if user else match.group(7)

    return CronRule(minute=match.group(1), hour=match.group(2), day_of_the_month=match.group(3), month=match.group(4),
                    day_of_the_week=match.group(5), user=cron_user, command=cron_command)


def parse_crontab(crontab, user):
    """ Return a list of parsed, non-empty, CronRule entries for the given crontab text file contents.
    """
    return filter(None, [parse_cron_rule(rule, user) for rule in crontab.split("\n")])


@common_command_and_options(command_name=COMMAND_NAME)
@click.option("--delimiter", "-d", help="Column delimiter character(s).  [default: tab]")
@click.option("--no-header", "-H", is_flag=True, help="Don't display the table header row.")
@click.option("--sort", "-s", is_flag=True, help="Sort table (approximately) by scheduled time.")
def main(delimiter, no_header, sort):
    """ Gather all of the system and user crontab schedules and display them in a consolidated table (tab-delimited by default): minute (m),
        hour (h), day of the month (dom), month (mon), day of the week (dow), user, and command. Optionally, the results may be sorted (as
        best as possible) by the scheduled hour and minute.

        Must be run as the root user.

        The gather-cron-jobs command is part of Scripnix.
    """
    check_root_user(command_name=COMMAND_NAME)
    _ = read_configuration()  # noqa

    consolidated_cron_rules = gather_system_cron_rules()
    consolidated_cron_rules.extend(gather_user_cron_rules(users=[p.pw_name for p in pwd.getpwall()]))
    click.echo(format_cron_rules_table(consolidated_cron_rules, not no_header, "\t" if not delimiter else delimiter, sort))
