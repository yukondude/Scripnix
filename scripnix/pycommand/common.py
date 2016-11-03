""" Scripnix common utility functions
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click
import configparser
import itertools
import os
import platform
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


def operating_system(translate=True):
    """ Return the operating system platform name (e.g., linux, macos, windows).
    """
    os_name = platform.system().lower()

    if translate and os_name == "darwin":
        return "macos"

    return os_name


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
