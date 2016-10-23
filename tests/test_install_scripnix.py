""" Scripnix install_scripnix command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click.testing import CliRunner
import os
from scripnix import __version__
from scripnix.pycommand.command import hostname, operating_system
from scripnix.pycommand.install_scripnix import install_global


def test_install_scripnix_install_global():
    def execute(fn, *args, echo):
        fn(*args)
        _ = echo

    with CliRunner().isolated_filesystem():
        install_global(execute, config_path="./test", os_name=operating_system())
        tree = []

        for path, dir_names, file_names in os.walk("."):
            tree += [os.path.join(path, d) for d in dir_names]
            tree += [os.path.join(path, f) for f in file_names]

        tree_attributes = [(t, os.stat(t).st_mode) for t in tree]

        expected = (("./test/archive-paths", 0o42750),
                    ("./test/archive-exclusions", 0o100640),
                    ("./test/conf.bash", 0o100644),
                    ("./test/README", 0o100444),
                    ("./test/sconf.bash", 0o100640),
                    ("./test/scripnix-" + __version__, 0o100000))

        for name_mode in expected:
            assert name_mode in tree_attributes

        archive_paths_path = "./test/archive-paths"

        for name in os.listdir(archive_paths_path):
            assert name.startswith(hostname())
            assert os.path.islink(os.path.join(archive_paths_path, name))