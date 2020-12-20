#!/usr/bin/python

import scapy.all as scapy


def scan(ip):
    # scapy.ls(scapy.ARP())  # ls() gives list of all fields we can set and their description

    arp_request = scapy.ARP(pdst=ip)  # creating arp_request object with dst_ip=user_input_ip

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # create a broadcast object to have Ethernet frame property with dst_mac as broadcast mac ff:ff:ff:ff:ff:ff
    # so this will be sent to all clients on same network. Ethernet frame is needed as data is sent using mac addr and
    # not ip addr, and mac addr is physical addr engraved on each network card. src mac and dest mac is set on
    # ethernet part of each packet, so we need to create a ethernet frame and append our ARP request to it.

    arp_request_broadcast = broadcast / arp_request
    # combine the 2 packets using / -> Ether frame to arp_request - creates a new packet

    # show details about packets
    arp_request.show()
    broadcast.show()
    arp_request_broadcast.show()

    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    # scapy.srp returns couple of two lists - answered, unanswered packets. use 1st list which is a
    # list of couples (packet sent, answer).

    print("IpAdrr\t\t\tMacAddr")
    print("------------------------------------------")
    for elements in answered_list:
        print(elements[1].psrc, "\t\t", elements[1].hwsrc)


scan("10.0.2.1/24")
