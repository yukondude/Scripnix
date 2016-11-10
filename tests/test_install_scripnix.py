""" Scripnix install_scripnix command unit tests
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import re

from click.testing import CliRunner

from scripnix import __version__
from scripnix.pybin.install_scripnix import COMMAND_NAME, install_global, install_per_user, main
from scripnix.util.common import hostname, operating_system

from .command import common_help_option, common_version_option


def _check_exists_with_mode(*expected):
    """ Test for expected files/directories with the correct permissions.
    """
    tree = []

    for path, dir_names, file_names in os.walk("."):
        tree += [os.path.join(path, d) for d in dir_names]
        tree += [os.path.join(path, f) for f in file_names]

    tree_attributes = [(t, os.stat(t).st_mode) for t in tree]

    for name_mode in expected:
        assert name_mode in tree_attributes


def _check_file_contents(*expected):
    """ Test for selected file contents matching a line-long regex.
    """
    for path, regex in expected:
        with open(path, "r") as f:
            whole_file = f.read()
            assert re.match(regex, whole_file, re.MULTILINE) is not None


def test_help_option():
    common_help_option(command_entry=main, command_name=COMMAND_NAME)


def test_install_global():
    def execute(fn, *args, echo):
        fn(*args)
        _ = echo  # noqa: F841

    with CliRunner().isolated_filesystem():
        # Run twice to exercise both paths of the file existence check.
        install_global(execute, config_path="./test", os_name=operating_system())
        install_global(execute, config_path="./test", os_name=operating_system())

        _check_exists_with_mode(("./test", 0o42755),
                                ("./test/archive-paths", 0o42750),
                                ("./test/archive-exclusions", 0o100640),
                                ("./test/conf.bash", 0o100644),
                                ("./test/README", 0o100444),
                                ("./test/sconf.bash", 0o100640),
                                ("./test/scripnix-" + __version__, 0o100000))

        # Test for presence of archive-paths/ symlinks.
        archive_paths_path = "./test/archive-paths"
        assert len(os.listdir(archive_paths_path)) >= 6

        for name in os.listdir(archive_paths_path):
            assert name.startswith(hostname())
            assert os.path.islink(os.path.join(archive_paths_path, name))

        _check_file_contents(("./test/archive-exclusions", r"^\/var\/archive$"),
                             ("./test/conf.bash", r"^# Global configuration setting overrides for conf\.bash\.$"),
                             ("./test/README", r"^Global Scripnix configuration settings\.$"),
                             ("./test/sconf.bash", r"^# Global configuration setting overrides for sconf\.bash\.$"))


def test_install_per_user():
    def execute(fn, *args, echo):
        fn(*args)
        _ = echo  # noqa: F841

    with CliRunner().isolated_filesystem():
        # Run twice to exercise both paths of the file existence check.
        install_per_user(execute, config_path="./.test")
        install_per_user(execute, config_path="./.test")

        _check_exists_with_mode(("./.test", 0o42750),
                                ("./.test/README", 0o100440))

        _check_file_contents(("./.test/README", r"^User Scripnix configuration settings\.$"))


def test_main_dry_run():
    runner = CliRunner()

    with CliRunner().isolated_filesystem():
        arguments = ["--yes", "--dry-run"]
        arguments_copy = arguments[:]
        result = runner.invoke(main, arguments)
        assert arguments_copy == arguments
        assert result.exit_code == 0
        assert re.match(r"^{} would do the following:$".format(COMMAND_NAME), result.output, re.MULTILINE) is not None
        assert len(result.output.split("\n")) >= 3


def test_version_option():
    common_version_option(command_entry=main, command_name=COMMAND_NAME)
