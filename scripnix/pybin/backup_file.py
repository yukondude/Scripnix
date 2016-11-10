""" Scripnix backup-file command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from collections import namedtuple
from datetime import datetime
import os
import shutil
import stat

import click

from scripnix.util.command import common_command_and_options
from scripnix.util.common import join_exceptions


COMMAND_NAME = "backup-file"
BACKUP_DATE_FORMAT = "%Y%m%d"
Backup = namedtuple("Backup", "from_path to_path is_exec_or_suid")


def assemble_dry_run_message(backups):
    """ Return a message showing the equivalent command-line operations that would be performed for the given list of Backup namedtuples.
    """
    message_lines = ["{} would do the following:".format(COMMAND_NAME)]

    for backup in backups:
        message_lines.append("cp {} {}".format(backup.from_path, backup.to_path))

        if backup.is_exec_or_suid:
            message_lines.append("chmod -x,u-s {}".format(backup.to_path))

    return "\n".join(message_lines)


def collect_backups(file_paths):
    """ For each of the given file paths, find the appropriate backup file name and also whether any executable or SUID bits are set.
        Return the results as a list of Backup namedtuples.
    """
    backups = []

    for file_path in file_paths:
        source_path = os.path.abspath(file_path)
        dir_path = os.path.abspath(os.path.dirname(file_path))
        file_name = os.path.basename(file_path)
        modification_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(BACKUP_DATE_FORMAT)

        duplicate_no = 0
        backup_path = base_backup_path = "{}.{}".format(os.path.join(dir_path, file_name), modification_date)

        while os.path.exists(backup_path):
            duplicate_no += 1
            backup_path = "{}.{}".format(base_backup_path, duplicate_no)

        is_exec_or_suid = os.access(source_path, os.X_OK) or (os.stat(source_path).st_mode & stat.S_ISUID > 0)
        backups.append(Backup(from_path=source_path, to_path=backup_path, is_exec_or_suid=is_exec_or_suid))

    return backups


def execute_backups(backups):
    """ Execute the given list of Backup namedtuple operations on the filesystem. Ignore I/O errors until complete and then raise them all
        at once as a single ClickException.
    """
    exceptions = []

    for backup in backups:
        try:
            shutil.copy2(backup.from_path, backup.to_path)
        except IOError:
            exceptions.append("Unable to copy '{}' to '{}'.".format(backup.from_path, backup.to_path))
            continue

        if backup.is_exec_or_suid:
            try:
                # Reset any SUID or executable bits.
                mode_mask = 0o7777 ^ (stat.S_ISUID | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                mode = os.stat(backup.to_path).st_mode
                os.chmod(backup[1], mode & mode_mask)
            except IOError:
                exceptions.append("Unable to set permissions for '{}'.".format(backup.to_path))
                continue

    if exceptions:
        raise click.ClickException(join_exceptions(exceptions))


@common_command_and_options(command_name=COMMAND_NAME, add_dry_run=True)
@click.argument('file', nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=False))
def main(file, dry_run):
    """ Backup the given file(s) by making a copy of each with an appended modification date (yyyymmdd). Append a number if the backup file
        name already exists. Remove any SUID or executable permissions from the backup file.

        The backup-file command is part of Scripnix.
    """
    backups = collect_backups(file_paths=file)

    if backups:
        if dry_run:
            click.echo(assemble_dry_run_message(backups))
        else:
            execute_backups(backups)
