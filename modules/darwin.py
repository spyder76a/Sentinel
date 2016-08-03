# !/usr/bin/python
# -*- coding: utf-8 -*- 
#
#===============================================================================
#
#    Filename:       darwin.py
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

import AppKit
import core
import datetime
import Foundation
import logging
import objc
import pwd
import sys
import time

#===============================================================================
#                     Configuration items
#===============================================================================

NSUserNotification = objc.lookUpClass('NSUserNotification')                                     # Notification method for Alerts
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')                         # Notification center method for Alerts

#===============================================================================
#                     Main Function
#===============================================================================
# Main Function
def Main():
    dbCheck()                                                                                   # Check the database is populated
    checkUsers()                                                                                # Check for changes in users
    return;

#===============================================================================
#                    Checkers - Used to check for changes
#===============================================================================

# Database checker

def dbCheck():
    logging.debug("Database Check initiated")                                                    # Update log
    SUid = core.setUID()                                                                        # Get the SUid
    try:
        popCheck = core.dbQuery("SELECT Value from `Checks` WHERE key = 'SUid'")
        if popCheck[0].encode('utf-8') != SUid:                                                 # Compare the Suid's
            logging.error("Database has been copied from another system. Delete and restart")   # Update log
            quit()                                                                              # Quit the application
    except:                                                                                     # Database appears not initialised                                                                        # Create Database
        sql = "INSERT OR REPLACE INTO Checks (Key, Value) VALUES ('SUid', '%s')" % SUid
        core.dbQuery(sql)                                                                       # Initialise SUid
        updateUsers()                                                                           # Initialise Users
        updateCertificates()                                                                    # Initialise Certificates
        updateListeners()                                                                       # Initialise Listeners
        updateFirewall()                                                                        # Initialise Firewall                                                                                       # Database appears initialised
    return;

# Check for application Tampering

def tamperCheck():
    logging.info("Tamper Check initiated")                                                      # Update log
    
    return;

# Check Users

def checkUsers():
    logging.debug("Users Check initiated")                                                       # Update log
    userList = pwd.getpwall()
    userListHash = core.hasher(str(userList))                                                   # Hash the current userlist
    sql = "SELECT Value FROM `Checks` WHERE key = 'Users'"
    userListdbHash = core.dbQuery(sql)                                                          # Get the Database Hash
    if userListdbHash[0].encode('utf-8') != userListHash:                                       # If the hashes are different                                                       
        logging.info("User list appears to have changed")                                       # Update log
        for p in userList:                                                                      # Get current users & iterate
            userHash = core.hasher(str(p))                                                      # Hash the entries
            sql = "SELECT hash from `Users` WHERE uid = '%s'" % p[2]                                
            dbHash = core.dbQuery(sql)                                                          # Query Hash for this uid
            if not dbHash:                                                                      # Check if uid not known
                logging.info("New user %s detected" % str(p[0]))                                # Update log
                alert("New User", p[0], "A new user account was added")                         # Trigger Alert
                sql = "INSERT OR REPLACE INTO `Users` VALUES ('%s', '%s', '%s', '%s', 'FALSE')" % (p[2], p[3], p[0], userHash)
                core.dbQuery(sql)                                                               # Add Entry to Database
            else:                                                                               # uid known
                if dbHash[0].encode('utf-8') != userHash:                                       # Hash has changed for uid
                    logging.info("User %s has changed" % str(p[0]))                             # Update log
                    #TODO - WHAT HAS CHANGED?
                    aMsg = "Undetermined change detected"                                       # Set the Alert Message
                    alert("User change", p[0], aMsg)                                            # Trigger Alert
                    sql = "INSERT OR REPLACE INTO `Users` VALUES ('%s', '%s', '%s', '%s', 'FALSE')" % (p[2], p[3], p[0], userHash)
                    core.dbQuery(sql)                                                           # Update the user record
            # TODO - Deleted accounts....                                                       
        sql = "INSERT OR REPLACE INTO `Checks` (Key, Value) VALUES ('Users', '%s')" % userListHash
        core.dbQuery(sql)                                                                       # Update the User List Hash         
        #
        # Info: username = p[0], uid = p[2], gid = p[3], name = p[4], dir = p[5], shell = p[6]
        #
        
    
    return;


#===============================================================================
#                    Updaters - Used to update database entries
#===============================================================================


def updateUsers():
    logging.info("Update Users initiated")                                                          # Update log
    userList = pwd.getpwall()                                                                       # Get the current userlist
    userListHash = core.hasher(str(userList))                                                       # Hash the userlist
    sql = "INSERT OR REPLACE INTO `Checks` (Key, Value) VALUES ('Users', '%s')" % userListHash
    core.dbQuery(sql)                                                                               # Query current entry
    for p in userList:                                                                              # Get current users & iterate
        hash = core.hasher(str(p))                                                                  # Hash the user entry
        sql = "INSERT OR REPLACE INTO `Users` VALUES ('%s', '%s', '%s', '%s', 'FALSE')" % (p[2], p[3], p[0], hash)
        core.dbQuery(sql)                                                                           # Write to database
    return;

def updateCertificates():
    
    
    return;

def updateListeners():
    
    
    return;


def updateFirewall():
    
    return;

#===============================================================================
#                         Alerts Framework
#===============================================================================

# Create an application alert

def alert(aTrigger, aObject, aMsg):
    aTime= time.strftime('%Y-%m-%d %H:%M:%S')
    logging.debug("Alert Function Initiated with:\n" + aTrigger + "\n" + aObject + "\n" + aMsg)
    notify("Alert: " + aTrigger + " for " + aObject, "Sentinel security has detected an alert item", aMsg, sound=False)                                  # Trigger Notification
    sql = "INSERT INTO Alerts (Object, Type, Alert, State) VALUES ('%s', '%s', '%s', '%s')" % (aObject, aTrigger, aMsg, 'False')
    core.dbQuery(sql)                                                                               # Save alert to db
    return;

# Create a system notification - Credit to: 

def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    logging.debug("Notify Function Initiated")
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    
