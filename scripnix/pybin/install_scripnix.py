""" Scripnix install-scripnix command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import grp
import os
import pwd
import stat
import subprocess

import click

from scripnix import __version__
from scripnix.util.command import common_command_and_options
from scripnix.util.common import hostname, is_root_user, operating_system, USER_CONFIG_DIR, ROOT_CONFIG_DIR


COMMAND_NAME = "install-scripnix"

RC_PATH_CHOICES = ("~/.bashrc", "~/.bash_profile", "~/.profile") if operating_system() == "macos" else ("~/.profile", "~/.bashrc")
RC_PATHS = list(map(os.path.expanduser, RC_PATH_CHOICES))


def install_global(execute, config_path, os_name):
    """ Install global Scripnix configuration settings.
    """
    # mkdir /etc/scripnix
    if not os.path.isdir(config_path):
        execute(os.mkdir, config_path, echo="mkdir {}".format(config_path))

    execute(os.chmod, config_path,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID | stat.S_IROTH | stat.S_IXOTH,
            echo="chmod u=rwx,g=rxs,o=rx {}".format(config_path))

    # Create /etc/scripnix/README
    readme_path = os.path.join(config_path, "README")

    if not os.path.isfile(readme_path):
        content = "Global Scripnix configuration settings.\n"
        content += "[https://github.com/yukondude/Scripnix]\n"
        execute(write_file, readme_path, content, echo="#create# {}".format(readme_path))

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

    if not os.path.isfile(conf_bash_path):
        content = "# Global configuration setting overrides for conf.bash.\n"
        content += "# User-specific setting overrides can be made in {}/conf.bash.\n".format(USER_CONFIG_DIR)
        execute(write_file, conf_bash_path, content, echo="#create# {}".format(conf_bash_path))

    execute(os.chmod, conf_bash_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH,
            echo="chmod u=rw,go=r {}".format(conf_bash_path))

    # Create /etc/scripnix/sconf.bash
    sconf_bash_path = os.path.join(config_path, "sconf.bash")

    if not os.path.isfile(sconf_bash_path):
        content = "# Global configuration setting overrides for sconf.bash.\n"
        content += "# Root- or sudoer-specific setting overrides can be made in {}/sconf.bash.\n".format(USER_CONFIG_DIR)
        content += "MYSQL_DUMP_FILE='{}-pgsql-dump.tar'\n".format(hostname())
        content += "PGSQL_DUMP_FILE='{}-pgsql-dump.tar'\n".format(hostname())
        execute(write_file, sconf_bash_path, content, echo="#create# {}".format(sconf_bash_path))

    execute(os.chmod, sconf_bash_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP, echo="chmod u=rw,g=r,o= {}".format(sconf_bash_path))

    # Create /etc/scripnix/archive-exclusions
    archive_exclusions_path = os.path.join(config_path, "archive-exclusions")

    if not os.path.isfile(archive_exclusions_path):
        content = "/var/archive\n"
        execute(write_file, archive_exclusions_path, content, echo="#create# {}".format(archive_exclusions_path))

    execute(os.chmod, archive_exclusions_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP,
            echo="chmod u=rw,g=r,o= {}".format(archive_exclusions_path))

    # mkdir /etc/scripnix/archive-paths
    archive_paths_path = os.path.join(config_path, "archive-paths")

    if not os.path.isdir(archive_paths_path):
        execute(os.mkdir, archive_paths_path, echo="mkdir {}".format(archive_paths_path))

    execute(os.chmod, archive_paths_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID,
            echo="chmod u=rwx,g=rxs,o= {}".format(archive_paths_path))

    # ln -s /*/ /etc/scripnix/archive-paths/#host#-*
    backup_paths = ["etc", "var/log", "var/mail", "var/spool", "var/www"]

    if os_name == "macos":
        backup_paths.extend(["Users", "var/root"])
    else:
        backup_paths.extend(["home", "root"])

    for symlink_dir in backup_paths:
        archive_symlink_path = os.path.join(archive_paths_path, "{}-{}".format(hostname(), symlink_dir.replace("/", "-")))
        symlink_dir_path = "/{}/".format(symlink_dir)

        if os.path.isdir(symlink_dir_path) and not os.path.islink(archive_symlink_path):
            execute(os.symlink, symlink_dir_path, archive_symlink_path, True,
                    echo="ln -s {} {}".format(symlink_dir_path, archive_symlink_path))


def install_per_user(execute, config_path):
    """ Install per-user Scripnix configuration settings.
    """
    def execute_chown(path):
        """ If installed via sudo, reset the owner of ~/.scripnix and its contents to the normal non-root user. If installed as the
            root user, this won't have any effect.
        """
        if is_root_user():
            stat_info = os.stat(os.path.join(path, ".."))
            execute(os.chown, path, stat_info.st_uid, stat_info.st_gid,
                    echo="chown {}:{} {}".format(pwd.getpwuid(stat_info.st_uid)[0], grp.getgrgid(stat_info.st_gid)[0], path))

    # mkdir ~/.scripnix
    if not os.path.isdir(config_path):
        execute(os.mkdir, config_path, echo="mkdir {}".format(config_path))

    execute_chown(config_path)
    execute(os.chmod, config_path,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID,
            echo="chmod u=rwx,g=rxs,o= {}".format(config_path))

    # Create ~/.scripnix/README
    readme_path = os.path.join(config_path, "README")

    if not os.path.isfile(readme_path):
        content = "User Scripnix configuration settings.\n"
        content += "[https://github.com/yukondude/Scripnix]\n"
        content += "Override the global Scripnix ({}/*.conf) settings here.\n".format(ROOT_CONFIG_DIR)
        execute(write_file, readme_path, content, echo="#create# {}".format(readme_path))

    execute_chown(readme_path)
    execute(os.chmod, readme_path, stat.S_IRUSR | stat.S_IRGRP, echo="chmod ug=r,o= {}".format(readme_path))

    # Display manual post-installation instructions.
    rc_paths = [p for p in RC_PATHS if os.path.isfile(p)]
    rc_exists = rc_paths != []
    rc_path = rc_paths[0] if rc_exists else RC_PATHS[0]

    click.echo("\nTo complete the Scripnix installation, perform the following steps.")
    step_no = 1

    if not rc_exists:
        click.echo("{}. Create {}".format(step_no, rc_path))
        step_no += 1

    click.echo("\n{}. Append these two lines to the end of of '{}':".format(step_no, rc_path))
    step_no += 1

    bin_path = os.path.dirname(subprocess.check_output(["which", COMMAND_NAME]).decode("utf-8").strip())
    click.echo("   PATH=\"{}:${{PATH}}\"".format(bin_path))

    scripnix_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "conf", "rc.bash"))
    click.echo("   source {}".format(scripnix_config_path))

    click.echo("\n{}. (Optional) Use visudo to insert the following path at the end of the".format(step_no))
    click.echo("   `Defaults secure_path` setting (if it exists):")
    click.echo("   {}".format(bin_path))


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

    if is_root_user():
        install_global(execute, config_path=ROOT_CONFIG_DIR, os_name=operating_system())

    install_per_user(execute, config_path=USER_CONFIG_DIR)


def write_file(path, content):
    """ Open a new file with the given path and write the content into it.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
