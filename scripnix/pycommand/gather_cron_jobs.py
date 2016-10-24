""" Scripnix gather-cron-jobs command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from .command import check_root_user, common_command_and_options


COMMAND_NAME = "gather-cron-jobs"


@common_command_and_options(command_name=COMMAND_NAME)
def main():
    """ Gather all of the system and user crontab schedules and display them in a consolidated tab-delimited table:

        mi hr dm mo dw user command

        The gather-cron-jobs command is part of Scripnix.
    """
    check_root_user(command_name=COMMAND_NAME)
