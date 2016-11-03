""" Scripnix gather-cron-jobs command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand.gather_cron_jobs import COMMAND_NAME, CronRule, main, parse_cron_rule
from .common_options import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def args_from_split_line(line):
    return line.split()


@pytest.mark.parametrize('rule,user,expected', [
    ("", None, None),
    ("  # Comment", None, None),
    ("* * * * false >/dev/null", None, None),
    ("PATH=/usr/local/bin:/home/user1/bin", None, None),
    ("* * * * * /bin/all -the >time", "user1", CronRule(*args_from_split_line("* * * * * user1"), command="/bin/all -the >time")),
    ("*    *     *  * *   /bin/every-minute", "user1", CronRule(*args_from_split_line("* * * * * user1 /bin/every-minute"))),
    ("*/10 *     *  * *   /bin/every-10-minutes", "user1", CronRule(*args_from_split_line("*/10 * * * * user1 /bin/every-10-minutes"))),
    ("35   0     16 6 *   /bin/june-16", "user1", CronRule(*args_from_split_line("35 0 16 6 * user1 /bin/june-16"))),
    ("00   11,16 *  * *   /bin/twice-per-day", "user1", CronRule(*args_from_split_line("00 11,16 * * * user1 /bin/twice-per-day"))),
    ("00   09-17 *  * *   /bin/work-hours", "user1", CronRule(*args_from_split_line("00 09-17 * * * user1 /bin/work-hours"))),
    ("00   13    *  * 1-5 /bin/weekdays", "user1", CronRule(*args_from_split_line("00 13 * * 1-5 user1 /bin/weekdays"))),
    ("00   14    1  1 *   /bin/january-1", "user1", CronRule(*args_from_split_line("00 14 1 1 * user1 /bin/january-1"))),
    ("*    *     *  * *   user2 /bin/all -the >time", None, CronRule(*args_from_split_line("* * * * * user2"),
                                                                     command="/bin/all -the >time")),
    ("*    *     *  * *   user2 /bin/every-minute", None, CronRule(*args_from_split_line("* * * * * user2 /bin/every-minute"))),
    ("*/10 *     *  * *   user2 /bin/every-10-minutes", None, CronRule(*args_from_split_line("*/10 * * * * user2 /bin/every-10-minutes"))),
    ("35   0     16 6 *   user2 /bin/june-16", None, CronRule(*args_from_split_line("35 0 16 6 * user2 /bin/june-16"))),
    ("00   11,16 *  * *   user2 /bin/twice-per-day", None, CronRule(*args_from_split_line("00 11,16 * * * user2 /bin/twice-per-day"))),
    ("00   09-17 *  * *   user2 /bin/work-hours", None, CronRule(*args_from_split_line("00 09-17 * * * user2 /bin/work-hours"))),
    ("00   13    *  * 1-5 user2 /bin/weekdays", None, CronRule(*args_from_split_line("00 13 * * 1-5 user2 /bin/weekdays"))),
    ("00   14    1  1 *   user2 /bin/january-1", None, CronRule(*args_from_split_line("00 14 1 1 * user2 /bin/january-1"))),
])
def test_parse_cron_rule(rule, user, expected):
    assert parse_cron_rule(rule, user) == expected


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
