#!/usr/bin/python

# command line program

import scapy.all as scapy
import optparse  # this is deprecated, newer alternative is argparse


def get_ip():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="ipadrr", help="Specify an IP Address or a range of IP Address")
    (options, argument) = parser.parse_args()
    # (values,options) = ("192.168.43.1",-ip)

    if not options.ipadrr:
        parser.error("[-] Specify an IP Address or a range of IP Address --help for more details")

    return options


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

    clients_list = []
    # declaring a list to store a dict values of ip and mac in it
    # nice way of storing a data and use for later use

    for elements in answered_list:
        client_dict = {"ip": elements[1].psrc, "mac": elements[1].hwsrc}
        # declare a dict to get ip and mac
        clients_list.append(client_dict)

    return clients_list


def print_result(result_list):
    print("IpAdrr\t\t\tMacAddr")
    print("------------------------------------------")
    for client in result_list:
        print(client['ip'], "\t\t", client['mac'])


ip = get_ip()
# get the ip range to ip variable

scan_result = scan(ip.ipadrr)
# use the ipaddr instance to use input ip to scan function

print_result(scan_result)
# represent the scan result in another function name print_result
