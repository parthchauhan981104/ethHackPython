#!/usr/bin/python

import scapy.all as scapy

# Well defined method to do the arp resquest respond work with a single line
def scan(ip):
    scapy.arping(ip)


scan("10.0.2.1/24")
