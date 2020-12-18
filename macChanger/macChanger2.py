#!/usr/bin/env python
'''
More secure code
command is split as a list, first element is the command and python knows that.
other elements are arguments etc but not other commands.
so it wont execute any other command if passed
'''

import subprocess

interface = input("Interface> ")  # eth0
macAddr = input("Mac Address> ")

print("[+] Changing Mac Address of Interface %s to %s" % (interface, macAddr))

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", macAddr])
subprocess.call(["ifconfig", interface, "up"])
subprocess.call(["ifconfig"])
