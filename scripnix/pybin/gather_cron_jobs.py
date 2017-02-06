""" Scripnix gather-cron-jobs command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import collections
import os
import pwd
import re
import stat
import subprocess

import click

from scripnix.util.command import common_command_and_options
from scripnix.util.common import check_root_user, config_values, natural_sort_key


COMMAND_NAME = "gather-cron-jobs"

# Any crontab comment or blank line.
CRON_IGNORE_REGEX = re.compile(r"^(\s*#.*|\s*)$")

CRON_JOB_PREFIX = r"^\s*"
CRON_SHORTCUT_TERM = r"(@reboot|@every_second)\s+"
# Character set taken from https://en.wikipedia.org/wiki/Cron#CRON_expression
CRON_TIME_TERM = r"([0-9*,?LW#/-]+)\s+"
CRON_USER_TERM = r"(\S+)\s+"
CRON_JOB_SUFFIX = r"(.+?)\s*$"
SYSTEM_CRON_JOB_REGEX = re.compile(CRON_JOB_PREFIX + CRON_TIME_TERM * 5 + CRON_USER_TERM + CRON_JOB_SUFFIX)
USER_CRON_JOB_REGEX = re.compile(CRON_JOB_PREFIX + CRON_TIME_TERM * 5 + CRON_JOB_SUFFIX)
SYSTEM_SHORTCUT_CRON_JOB_REGEX = re.compile(CRON_JOB_PREFIX + CRON_SHORTCUT_TERM + CRON_USER_TERM + CRON_JOB_SUFFIX)
USER_SHORTCUT_CRON_JOB_REGEX = re.compile(CRON_JOB_PREFIX + CRON_SHORTCUT_TERM + CRON_JOB_SUFFIX)
CRON_RUN_PARTS_JOB = re.compile(r"\s*run-parts(?:\s+-{1,2}\S+)*\s+(\S+)")

NATURAL_SORT_REGEX = re.compile(r"(\d+)")

CRON_SHORTCUTS = {
    '@annually': "0 0 1 1 *",
    '@daily': "0 0 * * *",
    '@every_minute': "* * * * *",
    '@hourly': "0 * * * *",
    '@midnight': "0 0 * * *",
    '@monthly': "0 0 1 * *",
    '@weekly': "0 0 * * 0",
    '@yearly': "0 0 1 1 *",
}

USER_CRON_CMD = "crontab -u {user} -l"

# Structure for a single cron job.
CronJob = collections.namedtuple("CronJob", "minute hour day_of_the_month month day_of_the_week user command")

CRONTAB_HEADER = CronJob("m", "h", "dom", "mon", "dow", "user", "command")


def file_paths_in_dir(dir_path, only_executable):
    """ Return the list of executable files (with complete paths) found directly under the given directory path.
    """
    file_paths = []

    if os.path.isdir(dir_path):
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            if not only_executable or (only_executable and stat.S_IXUSR & os.stat(file_path)[stat.ST_MODE]):
                file_paths.append(file_path)

    return file_paths


def format_cron_jobs_table(cron_jobs, header, delimiter, do_sort):
    """ Return the given list of CronJob entries formatted as delimited lines of text, with an optional initial header line. Sort the lines
        by the hour and minute elements if do_sort is True.
    """
    # Shallow-copy to avoid propagating in-place changes.
    jobs = cron_jobs[:]

    if do_sort:
        jobs.sort(key=lambda e: (natural_sort_key(e.hour), natural_sort_key(e.minute), natural_sort_key(e.user)))

    if header:
        jobs.insert(0, CRONTAB_HEADER)

    return "\n".join([delimiter.join(c) for c in jobs])


def gather_single_user_cron_jobs(user, do_unpack):
    """ Return a list of parsed CronJob entries for the given user using the `crontab` shell command to do the work.
    """
    try:
        crontab = subprocess.check_output([USER_CRON_CMD.format(user=user)], shell=True, stderr=subprocess.DEVNULL).decode('utf-8')
    except subprocess.CalledProcessError:
        crontab = ""

    return parse_crontab(crontab, user, do_unpack)


def gather_system_cron_jobs(crontab_path, cron_dir_path, do_unpack):
    """ Return a list of gathered CronJob entries from the given system crontab file and cron directory paths.
    """
    paths = [crontab_path]
    paths.extend(file_paths_in_dir(cron_dir_path, only_executable=False))
    cron_jobs = []

    for path in paths:
        try:
            with open(path, "r") as f:
                crontab = f.read()
        except OSError:
            continue

        cron_jobs.extend(parse_crontab(crontab, user=None, do_unpack=do_unpack))

    return cron_jobs


def gather_user_cron_jobs(users, do_unpack):
    """ Return a list of gathered CronJob entries for all of the users given.
    """
    user_jobs = [gather_single_user_cron_jobs(user, do_unpack) for user in users]
    return [job for jobs in user_jobs for job in jobs]


def parse_cron_job(job, user, do_unpack):
    """ Parse a single line from a crontab file and return it as a list of CronJob namedtuples. If user is given, assume the line doesn't
        contain a user column. Replace shortcuts with time fields (@reboot and @every_second are left more or less as-is). Separately list
        commands from a run-parts target directory if do_unpack is True. Return an empty list if the line is empty, a comment, or can't be
        parsed.
    """
    if CRON_IGNORE_REGEX.match(job) is not None:
        return []

    # For simplicity's sake, replace '@' schedule shortcuts with their corresponding time fields.
    for shortcut in CRON_SHORTCUTS.keys():
        if re.match(r"^\s*{}".format(shortcut), job) is not None:
            job = job.replace(shortcut, CRON_SHORTCUTS[shortcut])
            break

    is_shortcut_job = False
    job_regex = USER_CRON_JOB_REGEX if user else SYSTEM_CRON_JOB_REGEX
    match = job_regex.match(job)

    if not match:
        shortcut_regex = USER_SHORTCUT_CRON_JOB_REGEX if user else SYSTEM_SHORTCUT_CRON_JOB_REGEX
        match = shortcut_regex.match(job)

        if match:
            is_shortcut_job = True
        else:
            return []

    job_fields = list(match.groups()[:])

    if is_shortcut_job:
        # Insert four missing time fields for shortcut jobs. Use a space character so that the field delimiters aren't contiguous (and
        # therefore susceptible to being collapsed by the `column` command.
        job_fields[1:1] = [" "] * 4

    if user:
        job_fields.insert(5, user)

    jobs = unpack_job_command(do_unpack, job_fields)

    if not jobs:
        # If nothing could be unpacked, just emit the command as given.
        jobs = [CronJob(*job_fields)]

    return jobs


def parse_crontab(crontab, user, do_unpack):
    """ Return a list of parsed, non-empty, CronJob entries for the given crontab text file contents.
    """
    parsed_jobs = [parse_cron_job(job, user, do_unpack) for job in crontab.split("\n")]
    return list(filter(None, [job for jobs in parsed_jobs for job in jobs]))


@common_command_and_options(command_name=COMMAND_NAME)
@click.option("--delimiter", "-d", help="Column delimiter character(s).  [default: tab]")
@click.option("--no-header", "-H", is_flag=True, help="Don't display the table header row.")
@click.option("--run-parts", "-r", is_flag=True,
              help="Display commands in a run-parts target directory as if they were individually scheduled.")
@click.option("--sort", "-s", is_flag=True, help="Sort table (approximately) by scheduled time.")
def main(delimiter, no_header, run_parts, sort):
    """ Gather all of the system and user crontab scheduled jobs and display them in a consolidated table (tab-delimited by default):
        minute (m), hour (h), day of the month (dom), month (mon), day of the week (dow), user, and command. Optionally, the results may be
        sorted (as well as possible) by the scheduled hour and minute.

        Must be run as the root user.

        The gather-cron-jobs command is part of Scripnix.
    """
    check_root_user(command_name=COMMAND_NAME)

    system_cron_tab, system_cron_dir = config_values('SYSTEM_CRONTAB', 'SYSTEM_CRON_DIR')
    consolidated_cron_jobs = gather_system_cron_jobs(crontab_path=system_cron_tab, cron_dir_path=system_cron_dir, do_unpack=run_parts)
    consolidated_cron_jobs.extend(gather_user_cron_jobs(users={p.pw_name for p in pwd.getpwall()}, do_unpack=run_parts))
    click.echo(format_cron_jobs_table(consolidated_cron_jobs, not no_header, "\t" if not delimiter else delimiter, sort))


def unpack_job_command(do_unpack, job_fields):
    """ Unpack a run-parts target directory and return the commands as a list of CronJob namedtuples using the same schedule as the original
        job iff: do_unpack is True, "run-parts" and a valid directory appears in the command, and there is at least one executable file in
        that directory.
    """
    jobs = []
    schedule = job_fields[:-1]
    command = job_fields[-1]

    if do_unpack:
        run_parts_match = CRON_RUN_PARTS_JOB.search(command)

        if run_parts_match:
            path = run_parts_match.group(1)
            file_paths = file_paths_in_dir(path, only_executable=True)

            for file_path in file_paths:
                unpacked_job_fields = schedule + [file_path]
                jobs.append(CronJob(*unpacked_job_fields))

    return jobs
