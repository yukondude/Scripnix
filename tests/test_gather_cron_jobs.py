""" Scripnix gather-cron-jobs command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand.gather_cron_jobs import COMMAND_NAME, CronJob, format_cron_jobs_table, main, parse_cron_job, parse_crontab
from .command import common_help_option, common_version_option


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

SAMPLE_SYSTEM_CRON_JOBS = [
    CronJob(*line2args("07 * * * * root"), command="cd / && run-parts --report /etc/cron.hourly"),
    CronJob(*line2args("17 0 * * * root"), command="test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )"),
    CronJob(*line2args("37 0 * * 7 root"), command="test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )"),
    CronJob(*line2args("47 0 1 * * root"), command="test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )"),
]

SAMPLE_USER_CRONTAB = """MAIL:
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/home/me
 @daily /usr/bin/wget -O - -q -t 1 http://localhost/cron.php
* * * * * /bin/all-the-time --you-bet 2>/dev/null

# Early morning kludge
  5 10,22 * * * /home/me/do-it-daily --yes -Q

  @every_second     /bin/fast fast fast

30 4         * * * /bin/backup
5  0,4,10,16 * * * /bin/now --and --again >/tmp/log
@midnight nightly-routine --need >doing
@reboot do --after --boot
"""

SAMPLE_USER_CRON_JOBS = [
    CronJob(*line2args("0 0 * * *"), user="user3", command="/usr/bin/wget -O - -q -t 1 http://localhost/cron.php"),
    CronJob(*line2args("* * * * *"), user="user3", command="/bin/all-the-time --you-bet 2>/dev/null"),
    CronJob(*line2args("5 10,22 * * *"), user="user3", command="/home/me/do-it-daily --yes -Q"),
    CronJob(minute="@every_second", hour="", day_of_the_month="", month="", day_of_the_week="", user="user3",
            command="/bin/fast fast fast"),
    CronJob(*line2args("30 4 * * *"), user="user3", command="/bin/backup"),
    CronJob(*line2args("5 0,4,10,16 * * *"), user="user3", command="/bin/now --and --again >/tmp/log"),
    CronJob(*line2args("0 0 * * *"), user="user3", command="nightly-routine --need >doing"),
    CronJob(minute="@reboot", hour="", day_of_the_month="", month="", day_of_the_week="", user="user3", command="do --after --boot"),
]

SAMPLE_USER_CRON_TABLE = """m	h	dom	mon	dow	user	command
@every_second					user3	/bin/fast fast fast
@reboot					user3	do --after --boot
*	*	*	*	*	user3	/bin/all-the-time --you-bet 2>/dev/null
0	0	*	*	*	user3	/usr/bin/wget -O - -q -t 1 http://localhost/cron.php
0	0	*	*	*	user3	nightly-routine --need >doing
5	0,4,10,16	*	*	*	user3	/bin/now --and --again >/tmp/log
5	10,22	*	*	*	user3	/home/me/do-it-daily --yes -Q
30	4	*	*	*	user3	/bin/backup"""


@pytest.mark.parametrize('header,delimiter,do_sort', [
    (True, "\t", True),
    (True, "@@", True),
    (True, " ", True),
    (False, "\t", True),
    (False, "@@", True),
    (False, " ", True),
    (True, "\t", False),
    (True, "@@", False),
    (True, " ", False),
    (False, "\t", False),
    (False, "@@", False),
    (False, " ", False),
])
def test_format_cron_jobs_table(header, delimiter, do_sort):
    sample_user_cron_jobs_copy = SAMPLE_USER_CRON_JOBS[:]
    formatted = format_cron_jobs_table(SAMPLE_USER_CRON_JOBS, header, delimiter, do_sort)
    assert sample_user_cron_jobs_copy == SAMPLE_USER_CRON_JOBS
    expected = SAMPLE_USER_CRON_TABLE.replace("\t", delimiter) if delimiter != "\t" else SAMPLE_USER_CRON_TABLE

    if not header:
        eol_pos = expected.index('\n')
        expected = expected[eol_pos + 1:]

    if do_sort:
        assert formatted == expected
    else:
        for line in expected.split("\n"):
            assert line in formatted


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


@pytest.mark.parametrize('job,user,do_unpack,expected', [
    ("", None, False, []),
    ("  # Comment", None, False, []),
    ("* * * * false >/dev/null", None, False, []),
    ("PATH=/usr/local/bin:/home/user1/bin", None, False, []),
    ("", "user2", False, []),
    ("  # Comment", "user2", False, []),
    ("* * * false >/dev/null", "user2", False, []),
    ("PATH=/usr/local/bin:/home/user1/bin", "user2", False, []),
    ("* * * * * /bin/all -the >time", "user1", False, [CronJob(*line2args("* * * * * user1"), command="/bin/all -the >time")]),
    ("*    *     *  * *   /bin/every-minute", "user1", False, [CronJob(*line2args("* * * * * user1 /bin/every-minute"))]),
    ("*/10 *     *  * *   /bin/every-10-minutes", "user1", False, [CronJob(*line2args("*/10 * * * * user1 /bin/every-10-minutes"))]),
    ("35   0     16 6 *   /bin/june-16", "user1", False, [CronJob(*line2args("35 0 16 6 * user1 /bin/june-16"))]),
    ("00   11,16 *  * *   /bin/twice-per-day", "user1", False, [CronJob(*line2args("00 11,16 * * * user1 /bin/twice-per-day"))]),
    ("00   09-17 *  * *   /bin/work-hours", "user1", False, [CronJob(*line2args("00 09-17 * * * user1 /bin/work-hours"))]),
    ("00   13    *  * 1-5 /bin/weekdays", "user1", False, [CronJob(*line2args("00 13 * * 1-5 user1 /bin/weekdays"))]),
    ("00   14    1  1 *   /bin/january-1", "user1", False, [CronJob(*line2args("00 14 1 1 * user1 /bin/january-1"))]),
    ("      @reboot /bin/reboot", "user1", False, [CronJob(minute="@reboot", hour="", day_of_the_month="", month="", day_of_the_week="",
                                                           user="user1", command="/bin/reboot")]),
    ("@every_second /bin/fast", "user1", False, [CronJob(minute="@every_second", hour="", day_of_the_month="", month="", day_of_the_week="",
                                                         user="user1", command="/bin/fast")]),
    ("@every_minute /bin/every-minute", "user1", False, [CronJob(*line2args("* * * * * user1 /bin/every-minute"))]),
    ("      @weekly /bin/weekly", "user1", False, [CronJob(*line2args("0 0 * * 0 user1 /bin/weekly"))]),
    ("     @monthly /bin/monthly", "user1", False, [CronJob(*line2args("0 0 1 * * user1 /bin/monthly"))]),
    ("      @yearly /bin/yearly", "user1", False, [CronJob(*line2args("0 0 1 1 * user1 /bin/yearly"))]),
    ("*    *     *  * *   user2 /bin/all -the >time", None, False, [CronJob(*line2args("* * * * * user2"),
                                                                            command="/bin/all -the >time")]),
    ("*    *     *  * *   user2 /bin/every-minute", None, False, [CronJob(*line2args("* * * * * user2 /bin/every-minute"))]),
    ("*/10 *     *  * *   user2 /bin/every-10-minutes", None, False, [CronJob(*line2args("*/10 * * * * user2 /bin/every-10-minutes"))]),
    ("35   0     16 6 *   user2 /bin/june-16", None, False, [CronJob(*line2args("35 0 16 6 * user2 /bin/june-16"))]),
    ("00   11,16 *  * *   user2 /bin/twice-per-day", None, False, [CronJob(*line2args("00 11,16 * * * user2 /bin/twice-per-day"))]),
    ("00   09-17 *  * *   user2 /bin/work-hours", None, False, [CronJob(*line2args("00 09-17 * * * user2 /bin/work-hours"))]),
    ("00   13    *  * 1-5 user2 /bin/weekdays", None, False, [CronJob(*line2args("00 13 * * 1-5 user2 /bin/weekdays"))]),
    ("00   14    1  1 *   user2 /bin/january-1", None, False, [CronJob(*line2args("00 14 1 1 * user2 /bin/january-1"))]),
    ("      @reboot user2 /bin/reboot", None, False, [CronJob(minute="@reboot", hour="", day_of_the_month="", month="", day_of_the_week="",
                                                              user="user2", command="/bin/reboot")]),
    ("@every_second user2 /bin/fast", None, False, [CronJob(minute="@every_second", hour="", day_of_the_month="", month="",
                                                            day_of_the_week="", user="user2", command="/bin/fast")]),
    ("@every_minute user2 /bin/every-minute", None, False, [CronJob(*line2args("* * * * * user2 /bin/every-minute"))]),
    ("      @weekly user2 /bin/weekly", None, False, [CronJob(*line2args("0 0 * * 0 user2 /bin/weekly"))]),
    ("     @monthly user2 /bin/monthly", None, False, [CronJob(*line2args("0 0 1 * * user2 /bin/monthly"))]),
    ("      @yearly user2 /bin/yearly", None, False, [CronJob(*line2args("0 0 1 1 * user2 /bin/yearly"))]),
])
def test_parse_cron_job(job, user, do_unpack, expected):
    assert parse_cron_job(job, user, do_unpack) == expected


@pytest.mark.parametrize('crontab,user,do_unpack,expected', [
    ("", None, False, []),
    ("", "user3", False, []),
    (SAMPLE_SYSTEM_CRONTAB, None, False, SAMPLE_SYSTEM_CRON_JOBS),
    (SAMPLE_USER_CRONTAB, "user3", False, SAMPLE_USER_CRON_JOBS),
])
def test_parse_crontab(crontab, user, do_unpack, expected):
    assert parse_crontab(crontab, user, do_unpack) == expected


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
