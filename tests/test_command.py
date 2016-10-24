""" Scripnix shared command processing unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click import ClickException
# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand.command import check_root_user, is_root_user, join_exceptions


def test_check_root_user():
    with pytest.raises(ClickException) as excinfo:
        check_root_user("foo")

    message = str(excinfo.value)
    assert message.startswith("You must be root")
    assert message.endswith("sudo foo")


def test_is_root_user():
    assert not is_root_user()


@pytest.mark.parametrize('exceptions,expected', [
    ([], ""),
    (["foo"], "foo"),
    (["foo", "bar"], "foo\n       bar"),
    (["foo", "bar", "bat"], "foo\n       bar\n       bat"),
])
def test_join_exceptions(exceptions, expected):
    assert join_exceptions(exceptions=exceptions) == expected
