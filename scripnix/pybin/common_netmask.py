""" Scripnix common-netmask command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click

from scripnix.util.command import common_command_and_options


COMMAND_NAME = "common-netmask"


def bits_from_quads(quads):
    return "".join(["{:08b}".format(q) for q in quads])


def find_common_netmask_and_length(ip_addresses):
    ips = [quads_from_dotted_ip(i) for i in ip_addresses]

    netmask_bits = []
    ip_count = len(ips)

    bin_ips = [bits_from_quads(ip) for ip in ips]

    for bit in range(32):
        bits = [b[bit] for b in bin_ips]

        if bits.count(bits[0]) == ip_count:
            netmask_bits.append(bits[0])
        else:
            break

    netmask = "".join(netmask_bits).ljust(32, "0")
    return quads_from_bits(netmask), len(netmask_bits)


def quads_from_bits(bits):
    return [int(bits[:8], 2), int(bits[8:16], 2), int(bits[16:24], 2), int(bits[24:], 2)]


def quads_from_dotted_ip(ip_address):
    """ Return a 4-tuple of integer quads from a dotted-quad IP address string.
    """
    try:
        quads = [int(q) for q in ip_address.strip().rstrip('.').split('.')]
    except ValueError:
        raise click.ClickException("Non-integer quad found in IP address '{}'.".format(ip_address))

    if len(quads) > 4:
        raise click.ClickException("More than four quads in IP address '{}'.".format(ip_address))

    for quad in quads:
        if not (0 <= quad <= 255):
            raise click.ClickException("Invalid quad value '{}' in IP address '{}'. Must be in the range 0 - 255.".format(quad, ip_address))

    # Pad incomplete dotted quads with .255[.255]...
    quads = (quads + [255] * 4)[:4]

    return tuple(quads)


@common_command_and_options(command_name=COMMAND_NAME)
@click.argument("ipaddr", nargs=-1)
def main(ipaddr):
    """ Given any number of full or partial dotted-quad IPv4 addresses, display the netmask (and bit length) that matches all of the
        addresses.

        The common-netmask command is part of Scripnix.
    """
    if ipaddr:
        click.echo(find_common_netmask_and_length(ip_addresses=ipaddr))
