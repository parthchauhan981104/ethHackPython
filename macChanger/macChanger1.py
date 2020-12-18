#!/usr/bin/env python
'''
Less secure code
user can put ; or && to execute another command
'''

import subprocess

interface = input("Interface> ")  # eth0
macAddr = input("Mac Address> ")

print("[+] Changing Mac Address of Interface %s to %s" % (interface, macAddr))

subprocess.call("ifconfig {0} down".format(interface), shell=True)
subprocess.call("ifconfig {0} hw ether {1}".format(interface, macAddr), shell=True)
subprocess.call("ifconfig {0} up".format(interface), shell=True)
subprocess.call(["ifconfig"])
