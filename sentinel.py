# !/usr/bin/python
# -*- coding: utf-8 -*- 
#
##########################################################
#    
#    Filename:       sentinel.py
#    Application:    Sentinel
#    App Version:    v0.1 (Alpha)
#    Description:    Main file
#    Author:         Matt Jouques
#    File Version:   0.1
#
##########################################################

# Dependencies
import core
import logging
import os
import time

# Configuration Items
logging.basicConfig(filename='Sentinel.log',level=logging.DEBUG)

logging.info("\n\nSentinel Initiated at %s" % time.strftime('%Y-%m-%d %H:%M:%S'))           # Start the Log
core.dbConnect()                                                                            # Establish database connection
osDetails = os.uname()                                                                      # Check the system details
osPlatform = osDetails[0]                                                                   # Get the OS
if osPlatform == 'Darwin':                                                                  # Setup for Mac OS X
    from darwin import Main
    logging.debug("Darwin OS Detected")
elif osPlatform == 'Linux':                                                                 # Setup for Linux
    from linux import Main
    logging.debug("Linux OS Detected")
elif osPlatform == 'Windows':                                                               # Setup for Windows
    from windows import Main
    logging.debug("Windows OS Detected")
else:                                                                                       # Trap for incompatible OS
    logging.error("S001 - OS not detected or incompatible with this version")
    quit()

# Execution Loop
Main()
core.dbClose()                                                                              # Close Database Connection

