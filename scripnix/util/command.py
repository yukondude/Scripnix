""" Scripnix shared command processing
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click


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
