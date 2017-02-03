""" Scripnix find-grep command unit tests
"""

# This file is part of Scripnix. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import subprocess

from click.testing import CliRunner

from scripnix.pybin.whereis_scripnix import PACKAGE_PATH


def test_find_grep():
    here = os.path.abspath(os.path.dirname(__file__))
    shbin_path = os.path.join(PACKAGE_PATH, "shbin/find-grep")

    # Use the GPL licence text as the sample file contents.
    with open(os.path.join(here, "../LICENSE"), 'r') as f:
        text_a = f.read()

    text_b = text_a.replace("GNU", "WILDEBEEST")

    with CliRunner().isolated_filesystem():
        with open("aaa", 'w') as f:
            f.write(text_a)

        os.makedirs("fff/ggg/hhh")

        with open("fff/ggg/hhh/bbb", 'w') as f:
            f.write(text_b)

        found_text = subprocess.check_output([shbin_path, "GNU.GPL"]).decode("utf-8")
        assert len(found_text.strip().split("\n")) == 2
        assert "aaa:40:" in found_text
        assert "aaa:666:" in found_text

        found_text = subprocess.check_output([shbin_path, "WILDEBEEST.GPL"]).decode("utf-8")
        assert len(found_text.strip().split("\n")) == 2
        assert "fff/ggg/hhh/bbb:40:" in found_text
        assert "fff/ggg/hhh/bbb:666:" in found_text

        found_text = subprocess.check_output([shbin_path, "(G|W)[A-Z]{2,9} GPL"]).decode("utf-8")
        assert len(found_text.strip().split("\n")) == 4

        found_text = subprocess.check_output([shbin_path, "fff/ggg", "provision"]).decode("utf-8")
        assert len(found_text.strip().split("\n")) == 4
        assert "fff/ggg/hhh/bbb:58:" in found_text
        assert "fff/ggg/hhh/bbb:361:" in found_text
        assert "fff/ggg/hhh/bbb:417:" in found_text
        assert "fff/ggg/hhh/bbb:554:" in found_text
