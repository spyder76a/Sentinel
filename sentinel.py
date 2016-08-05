# !/usr/bin/python
# -*- coding: utf-8 -*- 
#===============================================================================
#
#    Filename:       sentinel.py
#    Application:    Sentinel
#    App Version:    v0.1 (Alpha)
#    Description:    Main file
#    Author:         Matt Jouques
#    File Version:   0.1
#
#===============================================================================



#===============================================================================
#                     Dependencies
#===============================================================================

import modules.core as core
import logging
import platform
import time

#===============================================================================
#                     Configuration items
#===============================================================================

logging.basicConfig(filename='Sentinel.log',level=logging.DEBUG)                            # Configure the log


#===============================================================================
#                     Application Initialisation
#===============================================================================

logging.info("\n\nSentinel Initiated at %s" % time.strftime('%Y-%m-%d %H:%M:%S'))           # Start the Log
core.dbConnect()                                                                            # Connect to the Database
osDetails = platform.uname()                                                                      # Check the system details
osPlatform = osDetails[0]                                                                   # Get the OS
if osPlatform == 'Darwin':                                                                  # Mac OS X Detected
    logging.info("Darwin OS Detected")                                                      # Update log
    import modules.darwin                                                                   # Import OSX specific functions
    modules.darwin.Main()                                                                   # Run the Main execution function
elif osPlatform == 'Linux':                                                                 # Setup for Linux
    logging.info("Linux OS Detected")                                                       # Update log
    import modules.linux                                                                    # Import Linux specific functions         
    modules.linux.Main()                                                                    # Run the Main execution function
elif osPlatform == 'Windows':                                                               # Setup for Windows
    logging.info("Windows OS Detected")                                                     # Update log
    import modules.windows                                                                  # Import Windows specific functions
    modules.windows.Main()                                                                  # Run the Main execution function
else:                                                                                       # Trap for incompatible OS
    logging.error("S001 - OS not detected or incompatible with this version")               # Update log
    quit()                                                                                  # Exit Application

#===============================================================================
#                     Close the application
#===============================================================================
core.dbClose()                                                                              # Close the Database
