# !/usr/bin/python
# -*- coding: utf-8 -*- 
#===============================================================================
#
#    Filename:       core.py
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

import hashlib
import logging
import os
import sqlite3
import time

#===============================================================================
#                     Configuration items
#===============================================================================



#===============================================================================
#                     Database Functions
#===============================================================================

# Connect to the Database

def dbConnect():
    logging.debug("dbConnect Function Initiated")
    global dbServer, dbConn, dbCursor
    dbServer = os.path.join(os.path.dirname(__file__), 'SentinelData')              # Set Database location
    logging.info("Database in use is: " +  dbServer)                                # Update log
    # Check for & establish db Connection
    try:    
        dbConn = sqlite3.connect(dbServer)                                          # Connect to the database
        dbCursor = dbConn.cursor()                                                  # Set the Cursor
    except sqlite3.Error, e:                                                        # Trap for errors
        logging.error("CD001 - Database connection failure - %s" % e.args[0])       # Update log
        quit()                                                                      # Exit the application
    # Check Database state
    try: 
        lsql = "SELECT name FROM sqlite_master WHERE TYPE = 'table'"                # Query database tables
        dbCursor.execute(lsql)                                                      # Execute the Query
        dbResult = dbCursor.fetchall()                                              # Get the results
        if not dbResult:                                                            # Check Tables are set (not new DB)
            logging.info("Database not initialised")                                # Update log
            dbCreate()                                                              # Build the database 
    except sqlite3.Error, e:                                                        # Trap for errors
        logging.error("CD002 - Database missing or damaged")                        # Update log
        logging.error("Error %s:" % e.args[0])                                      # Update log
        dbCreate()                                                                  # Build the Database
    return;

# Database query

def dbQuery(sql):
    global dbServer, dbConn, dbCursor
    logging.debug("dbQuery started with input of: " + sql)                          # Update log
    # Run the requested Query
    try:
        dbCursor.execute(sql)                                                       # Execute the Query    
        dbResult = dbCursor.fetchall()                                              # Get the results
        logging.debug("dbQuery affected rows = {}".format(dbCursor.rowcount))       # Update log - number of rows
    except sqlite3.Error, e:                                                        # Trap for errors
        logging.error("CD003 - Database query failed to execute - %s" % e.args[0])  # Update log
    try:
        dbConn.commit()                                                             # Commit changes to db
    except sqlite3.Error, e:                                                        # Trap for errors
        logging.error("CD004 - Database Commit failure - %s" % e.args[0])           # Update log
        try:
            dbConn.rollback()                                                       # Rollback changes
        except sqlite3.Error, e:                                                    # Trap for errors
            logging.error("CD005 - Database rollback failed - %s" % e.args[0])      # Update log
    return dbResult;                                                                # return the result

# Close Database connections

def dbClose():
    logging.debug("dbClose Function Initiated")
    global dbServer, dbConn, dbCursor
    try:
        dbCursor.close()                                                            # Close the cursor
        dbConn.close()                                                              # Close the database
    except sqlite3.Error, e:                                                        # Trap for errors
        try:
            dbConn.rollback()                                                       # Rollback changes
        except sqlite3.Error, e:                                                    # Trap for errors
            logging.error("CD005 - Database rollback failed")                       # Update log
            logging.error("Error %s:" % e.args[0])                                  # Update log
    return;

# Build the Database

def dbCreate():
    logging.debug("dbCreate Function Initiated")
    global dbServer, dbConn, dbCursor
    # Create the Database
    if not dbConn:
        logging.debug("Database connection in dbCreate lost")                       # Update log
    try:
        dbCursor.execute("CREATE TABLE `Checks` (`Key` TEXT UNIQUE,`Value` TEXT);")
        dbCursor.execute("CREATE TABLE `Alerts` (`Timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP, `Object` TEXT, `Type` TEXT,`Alert` TEXT, `State` TEXT);")
        dbCursor.execute("CREATE TABLE `Users` (`uid` TEXT NOT NULL, `gid` TEXT, `user` TEXT, `hash` TEXT, `State` TEXT, PRIMARY KEY(uid));")
        logging.info("Database created")                                            # Update log
    except sqlite3.Error, e:                                                        # Trap for errors
        logging.error("CD002 - Database table creation failed - %s" % e.args[0])    # Update log
    try:
        dbConn.commit()                                                             # Commit changes
    except sqlite3.Error, e:
        logging.error("CD003 - Database commit failure - %s" % e.args[0])           # Update log
        try:
            dbConn.rollback()                                                       # Rollback changes
        except sqlite3.Error, e:                                                    # Trap for errors
            logging.error("CD005 - Database rollback failed - %s" % e.args[0])      # Update log
    # Perform initial Database population
    
    return;

#===============================================================================
#                        Application Functions
#===============================================================================

# Hashing function

def hasher(raw):
    logging.debug("hasher Function Initiated")
    #logging.debug("Hasher executed with input of: " + raw)
    hashResult = hashlib.sha256(raw).hexdigest()
    logging.debug("Hasher generated a hash of: " + hashResult)
    return hashResult;

# Unique ID setup

def setUID():
    logging.debug("setUID Function Initiated")
    import uuid
    user = str(os.getuid())
    system = str(uuid.getnode())
    output = hasher(user + system)
    return output;

