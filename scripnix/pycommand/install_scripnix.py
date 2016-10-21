""" Scripnix install-scripnix command
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
from .command import common_command_and_options, is_root_user, USER_CONFIG_DIR, ROOT_CONFIG_DIR
import os
import socket
import stat
from scripnix import __version__


COMMAND_NAME = "install-scripnix"


def install_global(execute):
    """ Install global Scripnix configuration settings.
    """
    if not is_root_user():
        return

    # mkdir /etc/scripnix
    config_path = os.path.abspath(ROOT_CONFIG_DIR)

    if not os.path.isdir(config_path):
        execute(os.mkdir, config_path, echo="mkdir {}".format(config_path))

    execute(os.chmod, config_path,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID | stat.S_IROTH | stat.S_IXOTH,
            echo="chmod u=rwx,g=rxs,o=rx {}".format(config_path))

    # Create /etc/scripnix/README
    readme_path = os.path.join(config_path, "README")

    def write_readme():
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("Global Scripnix configuration settings.\n")
            f.write("[https://github.com/yukondude/Scripnix]\n")

    if not os.path.isfile(readme_path):
        execute(write_readme, echo="#create# {}".format(readme_path))

    execute(os.chmod, readme_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH, echo="chmod ugo=r {}".format(readme_path))

    # touch /etc/scripnix/scripnix-#version#
    version_path = os.path.join(config_path, "scripnix-{}".format(__version__))

    def touch_version():
        open(version_path, "w").close()

    if not os.path.isfile(version_path):
        execute(touch_version, echo="touch {}".format(version_path))

    execute(os.chmod, version_path, 0, echo="chmod ugo= {}".format(version_path))

    # Create /etc/scripnix/conf.bash
    conf_bash_path = os.path.join(config_path, "conf.bash")

    def write_conf_bash():
        with open(conf_bash_path, "w", encoding="utf-8") as f:
            f.write("# Global configuration setting overrides for conf.bash.\n")
            f.write("# User-specific setting overrides can be made in {}/conf.bash.\n".format(USER_CONFIG_DIR))

    if not os.path.isfile(conf_bash_path):
        execute(write_conf_bash, echo="#create# {}".format(conf_bash_path))

    execute(os.chmod, conf_bash_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH,
            echo="chmod u=rw,go=r {}".format(conf_bash_path))

    # Create /etc/scripnix/sconf.bash
    sconf_bash_path = os.path.join(config_path, "sconf.bash")
    hostname = socket.gethostname().split('.')[0].lower()

    def write_sconf_bash():
        with open(sconf_bash_path, "w", encoding="utf-8") as f:
            f.write("# Global configuration setting overrides for sconf.bash.\n")
            f.write("# Root- or sudoer-specific setting overrides can be made in {}/sconf.bash.\n".format(USER_CONFIG_DIR))
            f.write("MYSQL_DUMP_FILE='{}-pgsql-dump.tar'\n".format(hostname))
            f.write("PGSQL_DUMP_FILE='{}-pgsql-dump.tar'\n".format(hostname))

    if not os.path.isfile(sconf_bash_path):
        execute(write_sconf_bash, echo="#create# {}".format(sconf_bash_path))

    execute(os.chmod, sconf_bash_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP, echo="chmod u=rw,g=r,o= {}".format(sconf_bash_path))

    # Create /etc/scripnix/archive-exclusions
    archive_exclusions_path = os.path.join(config_path, "archive-exclusions")

    def write_archive_exclusions():
        with open(archive_exclusions_path, "w", encoding="utf-8") as f:
            f.write("/var/archive\n")

    if not os.path.isfile(archive_exclusions_path):
        execute(write_archive_exclusions, echo="#create# {}".format(archive_exclusions_path))

    execute(os.chmod, archive_exclusions_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP,
            echo="chmod u=rw,g=r,o= {}".format(archive_exclusions_path))

    # mkdir /etc/scripnix/archive-paths
    archive_paths_path = os.path.join(config_path, "archive-paths")

    if not os.path.isdir(archive_paths_path):
        execute(os.mkdir, archive_paths_path, echo="mkdir {}".format(archive_paths_path))

    execute(os.chmod, archive_paths_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID,
            echo="chmod u=rwx,g=rxs,o= {}".format(archive_paths_path))

    # ln -s /*/ /etc/scripnix/archive-paths/#host#-*
    for symlink_dir in ("etc", "home", "root", "var/log", "var/mail", "var/spool", "var/www"):
        archive_symlink_path = os.path.join(archive_paths_path, "{}-{}".format(hostname, symlink_dir.replace("/", "-")))
        symlink_dir_path = "/{}/".format(symlink_dir)

        if os.path.isdir(symlink_dir_path) and not os.path.islink(archive_symlink_path):
            execute(os.symlink, symlink_dir_path, archive_symlink_path, True,
                    echo="ln -s {} {}".format(symlink_dir_path, archive_symlink_path))


# def install_per_user(execute):
#     """ Install per-user Scripnix configuration settings.
#     """
#     config_path = os.path.abspath(USER_CONFIG_DIR)


@common_command_and_options(command_name=COMMAND_NAME, add_dry_run=True)
@click.confirmation_option(prompt='Are you sure you want to install Scripnix?')
@click.option("--verbose", "-v", is_flag=True, help="Display the commands as they are being executed.")
def main(dry_run, verbose):
    """ Install Scripnix for the current user. Global configuration settings (once installed by the root user) are stored under the
        /etc/scripnix/ directory. Per-user configuration settings, including for the root user, are stored under the ~/.scripnix/ directory
        and override the global settings. The installation can be re-run repeatedly, but will not overwrite existing configuration settings
        (however file and directory permissions will be reset).

        The install-scripnix command is part of Scripnix.
    """
    def execute(fn, *args, echo):
        """ Call the given function with its arguments if this is not a dry run. If it is a dry run, or the verbose flag is set, echo the
            given text to STDOUT. By closing over these two flags within this function, the install functions are much less complicated.
        """
        if not dry_run:
            fn(*args)

        if dry_run or verbose:
            click.echo(echo)

    if dry_run:
        click.echo("{} would do the following:".format(COMMAND_NAME))
    elif verbose:
        click.echo("{} is performing the following:".format(COMMAND_NAME))

    install_global(execute)
    # install_per_user(execute)
