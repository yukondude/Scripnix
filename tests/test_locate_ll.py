""" Scripnix locate-ll command unit tests
"""

# This file is part of Scripnix. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import subprocess

from scripnix.pybin.whereis_scripnix import PACKAGE_PATH


def test_locate_ll():
    # Pretty brain-dead test, but there aren't many things about a locate database that can be assumed between Linux and macOS.
    shbin_path = os.path.join(PACKAGE_PATH, "shbin/locate-ll")
    whereis = subprocess.check_output(["which", "locate-ll"]).decode("utf-8")
    located = subprocess.check_output([shbin_path, "[Ll]ocate.ll"]).decode("utf-8")
    assert whereis in located, "If this fails, you may need to run [g]update first."
