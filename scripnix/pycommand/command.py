""" Scripnix shared command processing
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3 (GPLv3). Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.


import click


def common_command_and_options(command_name):
    def command_with_help_switches(fn):
        return click.command(context_settings=dict(help_option_names=['-h', '--help']))(fn)

    def dry_run_option(fn):
        return click.option('--dry-run', '-D', is_flag=True, help="Show what would happen without actually doing it.")(fn)

    def version_option(fn):
        # noinspection PyUnusedLocal
        def show_version(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return
            from scripnix import __version__
            click.echo("The {} command is part of Scripnix version {}.".format(command_name, __version__))
            click.echo("Copyright 2016 Dave Rogers. Licensed under the GPLv3. See LICENSE.")
            ctx.exit()

        return click.option('--version', '-V', is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")(fn)

    def command_and_options(fn):
        return version_option(dry_run_option(command_with_help_switches(fn)))

    return command_and_options
