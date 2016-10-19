""" Scripnix backup-file command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand.backup_file import assemble_dry_run_message, COMMAND_NAME, Backup, main
from .common_options import common_version_option


DRY_RUN_PREFIX = "{} would do the following:".format(COMMAND_NAME)


@pytest.mark.parametrize('backups,expected', [
    ([], DRY_RUN_PREFIX),
    ([Backup('foo', 'foo.1', False)], "\n".join([DRY_RUN_PREFIX, "cp foo foo.1"])),
    ([Backup('bar', 'bar.1', True)], "\n".join([DRY_RUN_PREFIX, "cp bar bar.1", "chmod -x,u-s bar.1"])),
    ([Backup('foo', 'foo.1', False), Backup('bar', 'bar.1', True)], "\n".join([DRY_RUN_PREFIX, "cp foo foo.1", "cp bar bar.1", "chmod -x,u-s bar.1"])),
])
def test_backup_file_assemble_dry_run_message(backups, expected):
    assert assemble_dry_run_message(backups=backups) == expected


def test_backup_file_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
