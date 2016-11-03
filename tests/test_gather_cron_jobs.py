""" Scripnix gather-cron-jobs command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand.gather_cron_jobs import COMMAND_NAME, CronRule, main, parse_cron_rule, parse_crontab
from .common_options import common_help_option, common_version_option


def line2args(line):
    return line.split()


SAMPLE_SYSTEM_CRONTAB = """# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
07 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
17 0	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
37 0	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
47 0	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#"""

SAMPLE_SYSTEM_CRON_RULES = [
    CronRule(*line2args("07 * * * * root"), command="cd / && run-parts --report /etc/cron.hourly"),
    CronRule(*line2args("17 0 * * * root"), command="test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )"),
    CronRule(*line2args("37 0 * * 7 root"), command="test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )"),
    CronRule(*line2args("47 0 1 * * root"), command="test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )"),
]

SAMPLE_USER_CRONTAB = """MAIL:
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/home/me
 @daily /usr/bin/wget -O - -q -t 1 http://localhost/cron.php
* * * * * /bin/all-the-time --you-bet 2>/dev/null

# Early morning kludge
  5 10,22 * * * /home/me/do-it-daily --yes -Q

30 4         * * * /bin/backup
5  0,4,10,16 * * * /bin/now --and --again >/tmp/log
@midnight nightly-routine --need >doing

"""

SAMPLE_USER_CRON_RULES = [
    CronRule(*line2args("0 0 * * *"), user="user3", command="/usr/bin/wget -O - -q -t 1 http://localhost/cron.php"),
    CronRule(*line2args("* * * * *"), user="user3", command="/bin/all-the-time --you-bet 2>/dev/null"),
    CronRule(*line2args("5 10,22 * * *"), user="user3", command="/home/me/do-it-daily --yes -Q"),
    CronRule(*line2args("30 4 * * *"), user="user3", command="/bin/backup"),
    CronRule(*line2args("5 0,4,10,16 * * *"), user="user3", command="/bin/now --and --again >/tmp/log"),
    CronRule(*line2args("0 0 * * *"), user="user3", command="nightly-routine --need >doing"),
]


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


@pytest.mark.parametrize('rule,user,expected', [
    ("", None, None),
    ("  # Comment", None, None),
    ("* * * * false >/dev/null", None, None),
    ("PATH=/usr/local/bin:/home/user1/bin", None, None),
    ("", "user2", None),
    ("  # Comment", "user2", None),
    ("* * * false >/dev/null", "user2", None),
    ("PATH=/usr/local/bin:/home/user1/bin", "user2", None),
    ("* * * * * /bin/all -the >time", "user1", CronRule(*line2args("* * * * * user1"), command="/bin/all -the >time")),
    ("*    *     *  * *   /bin/every-minute", "user1", CronRule(*line2args("* * * * * user1 /bin/every-minute"))),
    ("*/10 *     *  * *   /bin/every-10-minutes", "user1", CronRule(*line2args("*/10 * * * * user1 /bin/every-10-minutes"))),
    ("35   0     16 6 *   /bin/june-16", "user1", CronRule(*line2args("35 0 16 6 * user1 /bin/june-16"))),
    ("00   11,16 *  * *   /bin/twice-per-day", "user1", CronRule(*line2args("00 11,16 * * * user1 /bin/twice-per-day"))),
    ("00   09-17 *  * *   /bin/work-hours", "user1", CronRule(*line2args("00 09-17 * * * user1 /bin/work-hours"))),
    ("00   13    *  * 1-5 /bin/weekdays", "user1", CronRule(*line2args("00 13 * * 1-5 user1 /bin/weekdays"))),
    ("00   14    1  1 *   /bin/january-1", "user1", CronRule(*line2args("00 14 1 1 * user1 /bin/january-1"))),
    ("      @reboot /bin/reboot", "user1", None),
    ("@every_minute /bin/every-minute", "user1", CronRule(*line2args("* * * * * user1 /bin/every-minute"))),
    ("      @weekly /bin/weekly", "user1", CronRule(*line2args("0 0 * * 0 user1 /bin/weekly"))),
    ("     @monthly /bin/monthly", "user1", CronRule(*line2args("0 0 1 * * user1 /bin/monthly"))),
    ("      @yearly /bin/yearly", "user1", CronRule(*line2args("0 0 1 1 * user1 /bin/yearly"))),
    ("*    *     *  * *   user2 /bin/all -the >time", None, CronRule(*line2args("* * * * * user2"), command="/bin/all -the >time")),
    ("*    *     *  * *   user2 /bin/every-minute", None, CronRule(*line2args("* * * * * user2 /bin/every-minute"))),
    ("*/10 *     *  * *   user2 /bin/every-10-minutes", None, CronRule(*line2args("*/10 * * * * user2 /bin/every-10-minutes"))),
    ("35   0     16 6 *   user2 /bin/june-16", None, CronRule(*line2args("35 0 16 6 * user2 /bin/june-16"))),
    ("00   11,16 *  * *   user2 /bin/twice-per-day", None, CronRule(*line2args("00 11,16 * * * user2 /bin/twice-per-day"))),
    ("00   09-17 *  * *   user2 /bin/work-hours", None, CronRule(*line2args("00 09-17 * * * user2 /bin/work-hours"))),
    ("00   13    *  * 1-5 user2 /bin/weekdays", None, CronRule(*line2args("00 13 * * 1-5 user2 /bin/weekdays"))),
    ("00   14    1  1 *   user2 /bin/january-1", None, CronRule(*line2args("00 14 1 1 * user2 /bin/january-1"))),
    ("      @reboot user2 /bin/reboot", None, None),
    ("@every_minute user2 /bin/every-minute", None, CronRule(*line2args("* * * * * user2 /bin/every-minute"))),
    ("      @weekly user2 /bin/weekly", None, CronRule(*line2args("0 0 * * 0 user2 /bin/weekly"))),
    ("     @monthly user2 /bin/monthly", None, CronRule(*line2args("0 0 1 * * user2 /bin/monthly"))),
    ("      @yearly user2 /bin/yearly", None, CronRule(*line2args("0 0 1 1 * user2 /bin/yearly"))),
])
def test_parse_cron_rule(rule, user, expected):
    assert parse_cron_rule(rule, user) == expected


@pytest.mark.parametrize('crontab,user,expected', [
    ("", None, []),
    ("", "user3", []),
    (SAMPLE_SYSTEM_CRONTAB, None, SAMPLE_SYSTEM_CRON_RULES),
    (SAMPLE_USER_CRONTAB, "user3", SAMPLE_USER_CRON_RULES),
])
def test_parse_crontab(crontab, user, expected):
    assert parse_crontab(crontab, user) == expected


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)