#!/usr/bin/env python
"""
command line program
python macChanger3.py --interface eth0 --mac 08:00:27:0a:8d:5b
python macChanger3.py --help to print help
"""

import subprocess
import optparse
import re


def mac_changer(interface, mac_address):
    print("\n[+] Changing Mac Address of Interface %s to %s\n" % (interface, mac_address))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig"])


def get_argument():
    cparser = optparse.OptionParser()  # init the parser object
    cparser.add_option("-i", "--interface", dest="interface", help="Interface to change the mac address")
    # adding the options like -i or --interface, dest is where the passed values get saved and help displays help msg
    cparser.add_option("-m", "--mac", dest="new_mac", help="Add new mac address")
    (options, arguments) = cparser.parse_args()
    # print(arguments)
    # options is an object containing values for all options- {'interface': 'eth0', 'new_mac': '00:11:22:33:44:77'}
    # arguments is the list of positional arguments leftover after parsing options so here it is []
    if not options.interface:
        cparser.error("[-] Specify an Interface. Use python macChanger3.py --help for more details")
    elif not options.new_mac:
        cparser.error("[-] Specify an MacAddr. Use python macChanger3.py --help for more details")
    return options


def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if current_mac:
        return current_mac.group(0)
    else:
        return None


opts = get_argument()
mac_changer(opts.interface, opts.new_mac)
final_mac = get_mac(opts.interface)

if final_mac == opts.new_mac:
    print("Mac Address Successfully Changed with new one %r" % final_mac)
else:
    print("Error while changing mac. Fix It")
