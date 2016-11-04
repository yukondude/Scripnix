""" Scripnix common unit testing functions
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os


def platform_name():
    # noinspection PyUnresolvedReferences
    return os.uname().sysname.lower()  # A different method from that used by operating_system().
