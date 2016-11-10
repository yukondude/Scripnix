""" Scripnix hyphenate command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click.testing import CliRunner
# noinspection PyPackageRequirements
import pytest

from scripnix.pybin.hyphenate import COMMAND_NAME, hyphenate, main

from .command import common_help_option, common_version_option


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


@pytest.mark.parametrize('lines,delimiter,expected', [
    ([], '-', []),
    (["foo"], '-', ["foo"]),
    (["foo bar"], '-', ["foo-bar"]),
    (["foo  bar"], '-', ["foo-bar"]),
    (["  foo  bar"], '-', ["foo-bar"]),
    (["foo  bar  "], '-', ["foo-bar"]),
    (["  foo  bar  "], '-', ["foo-bar"]),
    (["foo.bar"], '-', ["foo.bar"]),
    (["foo_bar"], '-', ["foo_bar"]),
    (["foo-bar"], '-', ["foo-bar"]),
    (["  foo  bar--quux "], '@@', ["foo@@bar@@quux"]),
    (["foo`~!@#$%^&*()+={}|[]\\:;\"\'<>?,/ \t\nbar"], '-', ["foo-bar"]),
    (["foo    bar****baz))))bat####quux"], '-', ["foo-bar-baz-bat-quux"]),
    (["foo bar", "   bar    baz   ", "baz___bat", "  _quux_  "], '-', ["foo-bar", "bar-baz", "baz___bat", "_quux_"]),
])
def test_hyphenate(lines, delimiter, expected):
    lines_copy = lines[:]
    assert hyphenate(lines=lines, delimiter=delimiter) == expected
    assert lines_copy == lines


@pytest.mark.parametrize('arguments,expected', [
    ([], ""),
    (["foo"], "foo\n"),
    (["foo bar", "   bar    baz   ", "baz___bat", "  _quux_  "], "foo-bar\nbar-baz\nbaz___bat\n_quux_\n"),
])
def test_main_arguments(arguments, expected):
    runner = CliRunner()
    arguments_copy = arguments[:]
    result = runner.invoke(main, arguments)
    assert arguments_copy == arguments
    assert result.exit_code == 0
    assert result.output == expected


@pytest.mark.parametrize('stdin,expected', [
    ("", ""),
    ("foo", "foo\n"),
    ("foo bar\n   bar    baz   \nbaz___bat\n  _quux_  ", "foo-bar\nbar-baz\nbaz___bat\n_quux_\n"),
])
def test_main_stdin(stdin, expected):
    runner = CliRunner()
    result = runner.invoke(main, input=stdin)
    assert result.exit_code == 0
    assert result.output == expected


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
