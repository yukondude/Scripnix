""" Scripnix shared command processing unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click import ClickException
import platform
# noinspection PyPackageRequirements
import pytest
from scripnix.pycommand import common, command


def test_check_root_user():
    with pytest.raises(ClickException) as excinfo:
        common.check_root_user("foo")

    message = str(excinfo.value)
    assert message.startswith("You must be root")
    assert message.endswith("sudo foo")


def test_common_command_and_options():
    """ Not much of a test, really. Just checks that the fn0() function is wrapped at least twice by decorators.
    """
    def fn0():
        pass  # pragma: no cover

    fn2 = command.common_command_and_options("foo", add_dry_run=True)
    assert callable(fn2)
    fn1 = fn2(fn0)
    assert callable(fn1)


def test_hostname():
    hn = common.hostname()  # A different method from that used by hostname().
    assert len(hn) > 0
    assert hn == platform.node().split('.')[0].lower()


def test_is_root_user():
    assert not common.is_root_user()


@pytest.mark.parametrize('exceptions,expected', [
    ([], ""),
    (["foo"], "foo"),
    (["foo", "bar"], "foo\n       bar"),
    (["foo", "bar", "bat"], "foo\n       bar\n       bat"),
])
def test_join_exceptions(exceptions, expected):
    assert common.join_exceptions(exceptions=exceptions) == expected


def test_read_configuration():
    """ Test assuming Scripnix isn't installed. Can't test the root-user config options in any case.
    """
    config = common.read_configuration()
    assert 'TMP_DIR' in config
    assert 'FIND_PATH_EXCLUDE' in config
