""" Scripnix shared command processing unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from scripnix.util import command


def test_common_command_and_options():
    """ Not much of a test, really. Just checks that the fn0() function is wrapped at least twice by decorators.
    """
    def fn0():
        pass  # pragma: no cover

    fn2 = command.common_command_and_options("foo", add_dry_run=True)
    assert callable(fn2)
    fn1 = fn2(fn0)
    assert callable(fn1)
