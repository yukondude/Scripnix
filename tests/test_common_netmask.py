""" Scripnix common-netmask command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
from click.testing import CliRunner
# noinspection PyPackageRequirements
import pytest

from scripnix.pybin.common_netmask import COMMAND_NAME, find_common_netmask_and_length, format_netmask_and_length, main

from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


@pytest.mark.parametrize('ip_addresses,expected', [
    (["0"], ((0, 255, 255, 255), 32)),
    (["0.1"], ((0, 1, 255, 255), 32)),
    (["0.2.3"], ((0, 2, 3, 255), 32)),
    (["0.4.5.6"], ((0, 4, 5, 6), 32)),
    (["0.7."], ((0, 7, 255, 255), 32)),
    (["1.2.3", "1.2.3."], ((1, 2, 3, 255), 32)),
    (["128", "0"], ((0, 0, 0, 0), 0)),
    (["255", "128"], ((128, 0, 0, 0), 1)),
    (["8.8.8.8", "8.8.4.4"], ((8, 8, 0, 0), 20)),
    (["8.8.8.8", "8.8.8.9"], ((8, 8, 8, 8), 31)),
    (["8.8.8.8", "8.8.8.9", "8.8.8.10", "8.8.8.11"], ((8, 8, 8, 8), 30)),
    (["172.16.0.0", "172.31.255.255"], ((172, 16, 0, 0), 12)),
    (["192.168.20.0", "192.168.21.0"], ((192, 168, 20, 0), 23)),
    (["76.9.32.0", "76.9.63.255"], ((76, 9, 32, 0), 19)),
])
def test_common_netmask(ip_addresses, expected):
    ip_addresses_copy = ip_addresses[:]
    assert find_common_netmask_and_length(ip_addresses) == expected
    assert ip_addresses_copy == ip_addresses


@pytest.mark.parametrize('ip_addresses,expected', [
    (["0"], "0.255.255.255/32"),
    (["128", "0"], "0.0.0.0/0"),
    (["255", "128"], "128.0.0.0/1"),
    (["192.168.20.0", "192.168.21.0"], "192.168.20.0/23"),
    (["76.9.32.0", "76.9.63.255"], "76.9.32.0/19"),
])
def test_format_netmask_and_length(ip_addresses, expected):
    ip_addresses_copy = ip_addresses[:]
    assert format_netmask_and_length(*find_common_netmask_and_length(ip_addresses=ip_addresses)) == expected
    assert ip_addresses_copy == ip_addresses


def test_invalid_negative_quad_common_netmask():
    with pytest.raises(click.ClickException) as excinfo:
        find_common_netmask_and_length(["10.10.-4.10"])

    assert "Invalid quad value '-4' in IP address" in str(excinfo)


def test_invalid_non_integer_quad_common_netmask():
    with pytest.raises(click.ClickException) as excinfo:
        find_common_netmask_and_length(["10.10.lO.10"])

    assert "Non-integer quad found in IP address" in str(excinfo)


def test_invalid_quad_value_common_netmask():
    with pytest.raises(click.ClickException) as excinfo:
        find_common_netmask_and_length(["10.10.257.10"])

    assert "Invalid quad value '257' in IP address" in str(excinfo)


def test_invalid_quad_length_common_netmask():
    with pytest.raises(click.ClickException) as excinfo:
        find_common_netmask_and_length(["10.10.10.10.10"])

    assert "More than four quads in IP address" in str(excinfo)


@pytest.mark.parametrize('arguments,expected', [
    ([], ""),
    (["128", "0"], "0.0.0.0/0"),
    (["255", "128"], "128.0.0.0/1"),
    (["192.168.20.0", "192.168.21.0"], "192.168.20.0/23"),
    (["76.9.32.0", "76.9.63.255"], "76.9.32.0/19"),
])
def test_main(arguments, expected):
    runner = CliRunner()
    arguments_copy = arguments[:]
    result = runner.invoke(main, arguments)
    assert arguments_copy == arguments
    assert result.exit_code == 0
    assert result.output.strip() == expected


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
