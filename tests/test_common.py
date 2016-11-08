""" Scripnix common utility functions unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import platform

from click import ClickException
# noinspection PyPackageRequirements
import pytest

from scripnix.util import common

from .common import platform_name


def test_check_root_user():
    with pytest.raises(ClickException) as excinfo:
        common.check_root_user("foo")

    message = str(excinfo.value)
    assert message.startswith("You must be root")
    assert message.endswith("sudo foo")


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
    exceptions_copy = exceptions[:]
    assert common.join_exceptions(exceptions=exceptions) == expected
    assert exceptions_copy == exceptions


@pytest.mark.parametrize('key,expected', [
    ("", (-1, "")),
    ("0", (0, "")),
    ("1", (1, "")),
    ("foo", (-1, "foo")),
    ("0bar", (0, "bar")),
    ("2bar", (2, "bar")),
    ("bat3", (-1, "bat3")),
    ("47baz", (47, "baz")),
    ("101.325kp", (101, ".325kp")),
])
def test_natural_sort_key(key, expected):
    assert common.natural_sort_key(key) == expected


def test_operating_system():
    this_os = platform_name()

    os_with_translate = common.operating_system(translate=True)
    assert len(os_with_translate) > 0
    assert os_with_translate == ("macos" if this_os == "darwin" else this_os)

    os_without_translate = common.operating_system(translate=False)
    assert len(os_without_translate) > 0
    assert os_without_translate == this_os


def test_read_configuration():
    """ Test assuming Scripnix isn't installed. Can't test the root-user config options in any case.
    """
    assert common.config_values() == ()

    tmp_dir = common.config_values('TMP_DIR')
    assert tmp_dir is not None

    tmp_dir, find_path_exclude, nope = common.config_values('TMP_DIR', 'FIND_PATH_EXCLUDE', 'NOPE')
    assert tmp_dir is not None
    assert find_path_exclude is not None
    assert nope is None
