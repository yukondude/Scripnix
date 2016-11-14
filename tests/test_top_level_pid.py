""" Scripnix top-level-pid command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

import click
from click.testing import CliRunner
import psutil
# noinspection PyPackageRequirements
import pytest

from scripnix.pybin.top_level_pid import COMMAND_NAME, main, penultimate_pid

from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_invalid_negative_penultimate_pid():
    with pytest.raises(click.ClickException) as excinfo:
        penultimate_pid(-1)

    assert str(excinfo).endswith("must be a positive integer.")


def test_invalid_pid_penultimate_pid():
    with pytest.raises(click.ClickException) as excinfo:
        penultimate_pid(999999)

    assert str(excinfo).endswith("does not exist.")


def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    pid = int(result.output.strip())
    assert psutil.Process(pid).ppid() in (0, 1)


def test_valid_penultimate_pid():
    pid = penultimate_pid(0)
    assert psutil.Process(pid).ppid() in (0, 1)

    pid = penultimate_pid(os.getpid())
    assert psutil.Process(pid).ppid() in (0, 1)

    assert penultimate_pid(1) in (0, 1)


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
