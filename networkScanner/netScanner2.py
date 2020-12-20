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
    # / operator has been used as a composition operator between two layers. When doing so, the lower layer can have
    # one or more of its defaults fields overloaded according to the upper layer.

    # show details about packets
    arp_request.show()
    broadcast.show()
    arp_request_broadcast.show()

    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1)
    # srp() to send the packet (and receive response) in layer2 with custom Ether frame to dest set in frame
    # returns 2 values answered packets and unanswered packets.
    # timeout=1 specify wait for 1 sec, if no response in 1sec -> move on, don't wait

    print(answered.summary())
    # print only the summary of answered packets
    # If there is no response, a None value will be assigned instead when the timeout is reached.



scan("10.0.2.1/24")
