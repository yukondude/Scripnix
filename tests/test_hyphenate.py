""" Scripnix hyphenate command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.


# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand.hyphenate import COMMAND_NAME, hyphenate, main
from .common_options import common_version_option


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
def test_hyphenate_hyphenate(lines, delimiter, expected):
    assert hyphenate(lines=lines, delimiter=delimiter) == expected


def test_hyphenate_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
