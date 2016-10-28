#!/usr/bin/env python
""" Increment the patch-level Scripnix version number in scripnix/__init__.py
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import re
import sys


if __name__ == '__main__':
    here = os.path.abspath(os.path.dirname(__file__))
    version_path = os.path.join(here, "scripnix/__init__.py")

    with open(version_path, "r") as f:
        version_text = f.read()

    patch_regex = re.compile(r"(__version__ = \"\d+\.\d+\.)(\d+)(\")")
    patch_match = patch_regex.search(version_text)

    if patch_match is None:
        sys.stderr.write("Can't find version number in {}\n".format(version_path))
        sys.exit(1)

    try:
        patch_number = int(patch_match.group(2))
    except ValueError:
        sys.stderr.write("Can't convert version number {} to integer.".format(patch_match.group(2)))
        sys.exit(1)

    version_text = patch_regex.sub(r"{}{}{}".format(patch_match.group(1), patch_number + 1, patch_match.group(3)), version_text)

    with open(version_path, "w") as f:
        f.write(version_text)

    version_match = re.search(r"__version__ = \"(\d+\.\d+\.\d+)\"", version_text)

    try:
        version_no = version_match.group(1)
    except AttributeError:
        sys.stderr.write("Can't find bumped version number.\n")
    else:
        sys.stdout.write(version_no + "\n")
