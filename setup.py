# !/usr/bin/python
# -*- coding: utf-8 -*- 
#
##########################################################
#    
#    Filename:       setup.py
#    Application:    Sentinel
#    App Version:    v0.1 (Alpha)
#    Description:    Setup file
#    Author:         Matt Jouques
#    File Version:   0.1
#
##########################################################

# Dependencies
import logging
import os
import sqlite3
import sys
import time

# Configuration Items
logging.basicConfig(filename='Sentinel.log',level=logging.DEBUG)
logging.info("\n\nSentinel Setup Initiated at %s" % time.strftime('%Y-%m-%d %H:%M:%S'))           # Start the Log

# Create Database
def dbCreate():
    global dbServer, dbConn, dbCursor
    dbServer = os.path.join(os.path.dirname(__file__), '.sentinelData')
    if os.path.isfile(dbServer) == True:
        print "WARNING: Database already exists. If you wish to re-initialise this application:"
        print "1) Delete or Rename " + dbServer
        print "2) Re-run this setup script"
        print "Otherwise continue? {Y/n)"
        choice = raw_input().lower()
        if choice in yes:
            return;
        else:
            quit()
    else:
        print "INFO: Creating Database: " + dbServer
        try:
            dbConn = sqlite3.connect(dbServer)
            dbCursor = dbConn.cursor()
        except sqlite3.Error, e:
            print "ERROR SD001 - Database connection failed"
            print ("Error %s:" % e.args[0])
            quit()
        try:
            dbCursor.execute("CREATE TABLE `Checks` (`Key` TEXT UNIQUE,`Value` TEXT);")
            dbCursor.execute("CREATE TABLE `Alerts` (`Timestamp` DATETIME, `Type` TEXT,`Alert` TEXT);")
            dbCursor.execute("CREATE TABLE `Users` (`uid` TEXT NOT NULL, `gid` TEXT, `user` TEXT, `hash` TEXT, PRIMARY KEY(uid));")
            print "Database created"
        except sqlite3.Error, e:
            print "ERROR SD002 - Database table creation failed"
            print ("Error %s:" % e.args[0])
            quit()
        try:
            dbConn.commit()
            dbConn.close()
        except sqlite3.Error, e:
            print "ERROR SD003 - Database commit failure"
            print ("Error %s:" % e.args[0])
            quit()
        return;

# Configuration Items
yes = set(['yes','y', ''])
no = set(['no','n'])

# Establish Setup
print "Welcome to the Setup script for the Sentinel Application"
print "The majority of this script is automated, however you will have the option for interactive setup for certain elements"

# Establish OS
osDetails = os.uname()                                                                      # Check the system details
osPlatform = osDetails[0]                                                                   # Get the OS
if osPlatform == 'Darwin':                                                                  # Setup for Mac OS X
    print "Mac OS X detected. Is this correct? (Y/n)"
    choice = raw_input().lower()
    if choice in yes:
        import darwin
        dbCreate()                                                                          # Create the Database
        darwin.updateUsers()                                                                # Populate the user db
        # TODO - the rest!
    else:
        print "Apologies, but this application has failed to detect a supported operating system"
        print "Please contact the developer and report a defect providing the following output:\n"
        print "Error in Setup detecting OS from: " 
        print osDetails
        quit()
elif osPlatform == 'Linux':                                                                 # Setup for Linux
    from linux import Main
    logging.debug("Linux OS Detected")
elif osPlatform == 'Windows':                                                               # Setup for Windows
    from windows import Main
    logging.debug("Windows OS Detected")
else:                                                                                       # Trap for incompatible OS
    logging.error("S001 - OS not detected or incompatible with this version")
    quit()

print "Setup completed successfully"













