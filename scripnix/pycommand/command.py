""" Scripnix shared command processing
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import configparser
import itertools
import platform
import os
import socket


# Scripnix configuration directory locations.
HERE = os.path.abspath(os.path.dirname(__file__))
BASE_CONFIG_DIR = os.path.abspath(os.path.join(HERE, "../conf"))
ROOT_CONFIG_DIR = "/etc/scripnix"
USER_CONFIG_DIR = os.path.expanduser("~/.scripnix")


def check_root_user(command_name):
    """ Raise a ClickException if the current user is not root.
    """
    if not is_root_user():
        raise click.ClickException("You must be root to execute this command. Try running it as: sudo {}".format(command_name))


def common_command_and_options(command_name, add_dry_run=False):
    """ Decorator that applies all of the common Click command and options in one step:
            - command with short and long help option switches
            - dry-run option switch (enabled by default)
            - version option switch
    """
    def command_with_help_switches(fn):
        """ Specify both the short and long help option switches.
        """
        return click.command(context_settings=dict(help_option_names=["-h", "--help"]))(fn)

    def dry_run_option(fn):
        """ Add the dry-run option switch.
        """
        return click.option("--dry-run", "-D", is_flag=True, help="Show what would happen without actually doing it.")(fn)

    def version_option(fn):
        """ Add the display version option switch.
        """
        # noinspection PyUnusedLocal
        def show_version(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return  # pragma: no cover
            from scripnix import __version__
            click.echo("The {} command is part of Scripnix version {}.".format(command_name, __version__))
            click.echo("Copyright 2016 Dave Rogers. Licensed under the GPLv3. See LICENSE.")
            ctx.exit()

        return click.option("--version", "-V", is_flag=True, callback=show_version, expose_value=False, is_eager=True,
                            help="Show version and exit.")(fn)

    def command_and_options(fn):
        """ Combine the common command and options into a single function decorator.
        """
        if add_dry_run:
            return version_option(dry_run_option(command_with_help_switches(fn)))
        else:
            return version_option(command_with_help_switches(fn))

    return command_and_options


def hostname():
    """ Return the lowercase computer host name.
    """
    return socket.gethostname().split('.')[0].lower()


def is_root_user():
    """ Return True if the current user is root.
    """
    return os.getuid() == 0


EXCEPTION_INDENT = len("Error: ")


def join_exceptions(exceptions):
    """ Join the given list of exception messages into a single multi-line string, indented to line up under Click's normal error reporting
        format.
    """
    return ("\n" + " " * EXCEPTION_INDENT).join(exceptions)


def operating_system():
    """ Return the operating system platform name (e.g., linux, macos, windows).
    """
    os_name = platform.system().lower()
    return "macos" if os_name == "darwin" else os_name


def read_configuration():
    """ Return the current Scripnix configuration as a single dictionary.
    """
    config = configparser.ConfigParser()

    def read_file_configuration(path, file_name, is_required):
        file_path = os.path.join(path, file_name)

        try:
            config.read_file(itertools.chain(['[DEFAULT]'], open(file_path)))
        except FileNotFoundError:
            if is_required:
                raise click.ClickException("The required configuration file '{}' was not found. "
                                           "Please re-install Scripnix.".format(file_path))

    for config_file_name, is_root_required in (("conf.bash", False), ("sconf.bash", True)):
        if is_root_required and not is_root_user():
            continue

        for config_dir, is_file_required in ((BASE_CONFIG_DIR, True), (ROOT_CONFIG_DIR, False), (USER_CONFIG_DIR, False)):
            read_file_configuration(path=config_dir, file_name=config_file_name, is_required=is_file_required)

    # Strip out leading and trailing single quotes from the values while converting to a dictionary (with uppercase keys as in the original
    # configuration files).
    return {k.upper(): v.strip("'") for k, v in dict(config["DEFAULT"]).items()}
