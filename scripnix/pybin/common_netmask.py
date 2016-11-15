""" Scripnix common-netmask command. See the main() function's docstring for details.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import click

from scripnix.util.command import common_command_and_options


COMMAND_NAME = "common-netmask"

IP_ADDRESS_BIT_WIDTH = 32


def bits_from_quads(quads):
    """ Return a string of 32 1/0 bits from the given 4-tuple of integer quads.
    """
    assert len(quads) == 4
    return "".join("{:08b}".format(q) for q in quads)


def find_common_netmask_and_length(ip_addresses):
    """ Return a tuple of the 4-tuple netmask and mask length that most completely matches the given list of dotted-quad IPv4 address
        strings.
    """
    quad_addresses = [quads_from_dotted_ip(ia) for ia in ip_addresses]
    bit_addresses = [bits_from_quads(qa) for qa in quad_addresses]
    netmask_bits = []

    for bit_posn in range(IP_ADDRESS_BIT_WIDTH):
        bit_set = {ba[bit_posn] for ba in bit_addresses}

        if len(bit_set) == 1:
            # All of the bits at position bit_posn are identical, so add that bit to the netmask.
            netmask_bits.append(bit_set.pop())
        else:
            break

    netmask = "".join(netmask_bits).ljust(IP_ADDRESS_BIT_WIDTH, "0")
    return quads_from_bits(netmask), len(netmask_bits)


def format_netmask_and_length(netmask, length):
    """ Return a string of the form a.b.c.d/e for the given 4-tuple netmask (a,b,c,d) and mask length (e).
    """
    return "{}/{}".format(".".join(str(n) for n in netmask), length)


def quads_from_bits(bits):
    """ Return a 4-tuple of integer quads from the given string of 32 1/0 bits.
    """
    assert len(bits) == IP_ADDRESS_BIT_WIDTH
    return int(bits[:8], 2), int(bits[8:16], 2), int(bits[16:24], 2), int(bits[24:], 2)


def quads_from_dotted_ip(ip_address):
    """ Return a 4-tuple of integer quads from the given dotted-quad IPv4 address string.
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
    return tuple((quads + [255] * 4)[:4])


@common_command_and_options(command_name=COMMAND_NAME)
@click.argument("ipaddr", nargs=-1)
def main(ipaddr):
    """ Given any number of full or partial dotted-quad IPv4 addresses, display the netmask (and bit length) that matches all of the
        addresses.

        The common-netmask command is part of Scripnix.
    """
    if ipaddr:
        click.echo(format_netmask_and_length(*find_common_netmask_and_length(ip_addresses=ipaddr)))
