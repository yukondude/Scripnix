""" Scripnix top-level-pid command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

import click
from click.testing import CliRunner
# noinspection PyPackageRequirements
import pytest

from scripnix.pybin.command_for_pid import COMMAND_NAME, command_name, main
from scripnix.util.common import operating_system

from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_invalid_negative_command_name():
    with pytest.raises(click.ClickException) as excinfo:
        command_name(-1)

    assert str(excinfo).endswith("must be a positive integer.")


def test_invalid_pid_command_name():
    with pytest.raises(click.ClickException) as excinfo:
        command_name(999999)

    assert str(excinfo).endswith("does not exist.")


def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    command = result.output.strip()
    assert len(command) > 0
    assert "python" in command or "py.test" in command


def test_valid_command_name():
    command = command_name(0)
    assert "python" in command or "py.test" in command

    command = command_name(os.getpid())
    assert "python" in command or "py.test" in command

    command = command_name(1)
    assert command in (["launchd"] if operating_system() == "macos" else ["init", "systemd"])


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
