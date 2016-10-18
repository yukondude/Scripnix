""" backup-file
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3 (GPLv3). Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
from collections import namedtuple
from datetime import datetime
import os
import shutil
import stat
from .command import common_command_and_options


Operation = namedtuple("Operation", "from_path to_path is_exec_or_suid")


@common_command_and_options(command_name=__doc__)
@click.argument('file', nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=False))
def main(file, dry_run):
    """ Backup the given file(s) by making a copy of each with an appended modification date (yyyymmdd). Append a number if the backup file name already exists.
        Remove any SUID or executable permissions from the backup file.
    """
    operations = []

    for file_path in file:
        source_path = os.path.abspath(file_path)
        dir_path = os.path.abspath(os.path.dirname(file_path))
        file_name = os.path.basename(file_path)
        modification_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y%m%d")

        duplicate_no = 0
        backup_path = base_backup_path = "{}.{}".format(os.path.join(dir_path, file_name), modification_date)

        while os.path.isfile(backup_path):
            duplicate_no += 1
            backup_path = "{}.{}".format(base_backup_path, duplicate_no)

        is_exec_or_suid = os.access(source_path, os.X_OK) or os.stat(source_path).st_mode & stat.S_ISUID > 0
        operations.append(Operation(from_path=source_path, to_path=backup_path, is_exec_or_suid=is_exec_or_suid))

    if dry_run:
        click.echo("{} would do the following:".format(__doc__.strip()))

        for operation in operations:
            click.echo("cp {} {}".format(operation.from_path, operation.to_path))

            if operation.is_exec_or_suid:
                click.echo("chmod -x,u-s {}".format(operation.to_path))
    else:
        for operation in operations:
            try:
                shutil.copy2(operation.from_path, operation.to_path)
            except IOError:
                raise click.ClickException("Unable to copy {} to {}.".format(operation.from_path, operation.to_path))

            try:
                # Ignore operation.is_exec_or_suid and strip out any SUID or executable bits.
                mode = os.stat(operation.to_path).st_mode
                mode &= 0o7777 ^ (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_ISUID)
                os.chmod(operation[1], mode)
            except IOError:
                raise click.ClickException("Unable to set permissions for {}.".format(operation.to_path))


if __name__ == '__main__':
    main()
