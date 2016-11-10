""" Scripnix backup-file command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import datetime
import os
import re
import time

from click import ClickException
from click.testing import CliRunner
# noinspection PyPackageRequirements
import pytest

from scripnix.pybin.backup_file import assemble_dry_run_message, Backup, collect_backups, COMMAND_NAME, execute_backups, main

from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


DRY_RUN_PREFIX = "{} would do the following:".format(COMMAND_NAME)


@pytest.mark.parametrize('backups,expected', [
    ([], DRY_RUN_PREFIX),
    ([Backup('foo', 'foo.1', False)], "\n".join([DRY_RUN_PREFIX, "cp foo foo.1"])),
    ([Backup('bar', 'bar.1', True)], "\n".join([DRY_RUN_PREFIX, "cp bar bar.1", "chmod -x,u-s bar.1"])),
    ([Backup('foo', 'foo.1', False), Backup('bar', 'bar.1', True)],
     "\n".join([DRY_RUN_PREFIX, "cp foo foo.1", "cp bar bar.1", "chmod -x,u-s bar.1"])),
])
def test_assemble_dry_run_message(backups, expected):
    backups_copy = backups
    assert assemble_dry_run_message(backups=backups) == expected
    assert backups_copy == backups


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)


def _create_files(file_name_permissions, modification_ts):
    """ For each (file_name, permissions_mode) tuple, create the file and assign its permissions. Change the modification date to the given
        timestamp. Return a tuple of the collected backups and the absolute path of the test directory.
    """
    for file_name, mode in file_name_permissions:
        with open(file_name, "a"):
            os.utime(file_name, (time.time(), modification_ts))
        os.chmod(file_name, mode)

    file_names = [f[0] for f in file_name_permissions]
    file_names_copy = file_names[:]
    backups = collect_backups(file_names)
    assert file_names_copy == file_names
    test_path = os.path.abspath(".")
    return backups, test_path


@pytest.mark.parametrize('file_name_permissions,expected', [
    ([], []),
    ([("test.tst", 0o0644)], [Backup("test.tst", "test.tst.20140702", False)]),
    ([("test.exe", 0o0755)], [Backup("test.exe", "test.exe.20140702", True)]),
    ([("test.suid", 0o4644)], [Backup("test.suid", "test.suid.20140702", True)]),
    ([("test.tst", 0o0644), ("test.exe", 0o0755)],
     [Backup("test.tst", "test.tst.20140702", False), Backup("test.exe", "test.exe.20140702", True)]),
    ([("test.tst", 0o0644), ("test.tst.20140702", 0o0644)],
     [Backup("test.tst", "test.tst.20140702.1", False), Backup("test.tst.20140702", "test.tst.20140702.20140702", False)]),
])
def test_collect_backups(file_name_permissions, expected):
    with CliRunner().isolated_filesystem():
        backups, test_path = _create_files(file_name_permissions, datetime.datetime(2014, 7, 2, 0, 0).timestamp())
        assert len(backups) == len(expected)

        for i, backup in enumerate(backups):
            assert backup.from_path == os.path.join(test_path, expected[i].from_path)
            assert backup.to_path == os.path.join(test_path, expected[i].to_path)
            assert backup.is_exec_or_suid == expected[i].is_exec_or_suid


@pytest.mark.parametrize('file_name_permissions,expected', [
    ([("test.tst", 0o0644)], [("test.tst", 0o100644)]),
    ([("test.tst", 0o0644), ("test.exe", 0o0755)], [("test.tst", 0o100644), ("test.exe", 0o100755)]),
])
def test_execute_backups_failure(file_name_permissions, expected):
    with CliRunner().isolated_filesystem():
        backups, test_path = _create_files(file_name_permissions, datetime.datetime(2013, 8, 31, 0, 0).timestamp())

        monkeyed_backups = [Backup(b.from_path + '.bad', b.to_path, b.is_exec_or_suid) for b in backups]
        monkeyed_backups_copy = monkeyed_backups[:]

        with pytest.raises(ClickException) as excinfo:
            execute_backups(monkeyed_backups)

        assert monkeyed_backups_copy == monkeyed_backups
        message = str(excinfo.value)
        assert len(message.split("\n")) == len(monkeyed_backups)
        assert message.startswith("Unable to copy")

        # Make sure unexpected files weren't somehow created.
        assert len(os.listdir(test_path)) == len(expected)

        for file_name, mode in expected:
            assert os.path.isfile(file_name)
            assert os.stat(file_name).st_mode == mode


@pytest.mark.parametrize('file_name_permissions,expected', [
    ([], []),
    ([("test.tst", 0o0644)], [("test.tst", 0o100644), ("test.tst.20120616", 0o100644)]),
    ([("test.exe", 0o0755)], [("test.exe", 0o100755), ("test.exe.20120616", 0o100644)]),
    ([("test.suid", 0o4644)], [("test.suid", 0o104644), ("test.suid.20120616", 0o100644)]),
    ([("test.suid", 0o4750)], [("test.suid", 0o104750), ("test.suid.20120616", 0o100640)]),
])
def test_execute_backups_success(file_name_permissions, expected):
    with CliRunner().isolated_filesystem():
        backups, test_path = _create_files(file_name_permissions, datetime.datetime(2012, 6, 16, 0, 0).timestamp())
        backups_copy = backups[:]
        execute_backups(backups)
        assert backups_copy == backups

        # Make sure unexpected files weren't somehow created.
        assert len(os.listdir(test_path)) == len(expected)

        for file_name, mode in expected:
            assert os.path.isfile(file_name)
            assert os.stat(file_name).st_mode == mode


@pytest.mark.parametrize('file_name_permissions,arguments,expected', [
    ([], [], ([], "")),
    ([], ["--dry-run"], ([], "")),
    ([("test.tst", 0o0644)], [], ([("test.tst", 0o100644)], "")),
    ([("test.tst", 0o0644)], ["test.tst"], ([("test.tst", 0o100644), ("test.tst.20150314", 0o100644)], "")),
    ([("test.tst", 0o0644)], ["--dry-run", "test.tst"],
     ([("test.tst", 0o100644)], DRY_RUN_PREFIX + r"\ncp .+/test\.tst .+/test\.tst\.20150314\n$")),
])
def test_main(file_name_permissions, arguments, expected):
    runner = CliRunner()

    with CliRunner().isolated_filesystem():
        backups, test_path = _create_files(file_name_permissions, datetime.datetime(2015, 3, 14, 0, 0).timestamp())
        arguments_copy = arguments[:]
        result = runner.invoke(main, arguments)
        assert arguments_copy == arguments

        expected_file_name_permissions, expected_output_re = expected
        assert len(os.listdir(test_path)) == len(expected_file_name_permissions)
        assert result.exit_code == 0
        assert re.match(expected_output_re, result.output) is not None

        for file_name, mode in expected_file_name_permissions:
            assert os.path.isfile(file_name)
            assert os.stat(file_name).st_mode == mode
