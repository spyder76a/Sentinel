# !/usr/bin/python
# -*- coding: utf-8 -*- 
#
##########################################################
#    
#    Filename:       core.py
#    Application:    Sentinel
#    App Version:    v0.1 (Alpha)
#    Description:    Core functions file
#    Author:         Matt Jouques
#    File Version:   0.1
#
##########################################################

import hashlib
import logging
import os
import sqlite3
import time

# Globals
global dbServer, dbConn, dbCursor

# Configuration Items
dbServer = os.path.join(os.path.dirname(__file__), '.sentinelData')
dbConn = ""
dbCursor = ""

# Database Connection
def dbConnect():
    if os.path.isfile(dbServer) == False:                                           # Check if database already exists
        logging.warning("Database not found, initialising Setup")
        from setup import dbCreate
        dbCreate()                                                                  # Initialise Database
    try:
        dbConn = sqlite3.connect(dbServer)
        dbCursor = dbConn.cursor()
        logging.info("Database connection established")
    except:
        logging.error("CD001 - Unable to establish database connection")
        quit()
    return;

# Database query
def dbQuery(sql):
    try:    
        dbCursor.execute(sql)
        dbResult = dbCursor.fetchall()
        logging.debug(sql)
        logging.debug("dbQuery affected rows = {}".format(dbCursor.rowcount))
        return dbResult;
    except sqlite3.Error, e:
        logging.error("CD003 - Database query failed to execute")
        logging.error("Error %s:" % e.args[0])
        logging.debug(sql)
    try:
        dbConn.commit()
    except sqlite3.Error, e:
        dbConn.rollback()
        logging.error("CD004 - Database Commit failure")
        logging.error("Error %s:" % e.args[0])
    return;

# Database close Connection
def dbClose():
    try:
        dbCursor.close()
        dbConn.close()
        logging.info("Database Connection Closed")
    except sqlite3.Error, e:
        logging.error("CD002 - Failed to close Database connection")
        logging.error("Error %s:" % e.args[0])
    return;

#  Alerts Framework
def alert(trigger):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    alertText = ("%t - %s have changed!!!") % (timestamp, trigger)
    logging.critical(alertText)
    query = "INSERT INTO Alerts VALUES ('%t', '%s', '$s')" % (timestamp, trigger, alertText)
    dbQuery(query)
    return;

# Hashing
def hasher(raw):
    logging.debug("Hasher executed with input of: " + raw)
    hashResult = hashlib.sha256(raw).hexdigest()
    logging.debug("Hasher generated a hash of: " + hashResult)
    return hashResult;
    


