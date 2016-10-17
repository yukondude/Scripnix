""" Scripnix: backup-file
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3 (GPLv3). Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# noinspection PyUnusedLocal
def show_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    from scripnix import __version__
    click.echo("{} version {}".format(__doc__.strip(), __version__))
    click.echo("Copyright 2016 Dave Rogers. Licensed under the GPLv3. See LICENSE.")
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--dry-run', '-D', is_flag=True, help="Show what would happen without actually doing it.")
@click.option('--version', '-V', is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")
@click.argument('file_paths', nargs=-1, type=click.Path(exists=True))
def main(file_paths):
    """ Back-up the named file or files by making copies of them using each file's last modified date (yyyymmdd) as the extension.
    """
    for file_path in file_paths:
        click.echo(file_path)


if __name__ == '__main__':
    main()
