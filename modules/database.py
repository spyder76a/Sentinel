# !/usr/bin/python
# -*- coding: utf-8 -*- 
#
#    Sentinel - Database Functions
#
#    @author: Matt Jouques
#


# Dependencies
import os
import sqlite3
from _sqlite3 import Cursor


# Config
db = os.path.join(os.path.dirname(__file__), '../data/sentinel')

def dbCreate():
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
    except:
        print "Create Database function failed"
    try:
        c.execute("CREATE TABLE `Checks` (`Key` TEXT UNIQUE,`Value` TEXT);")
        c.execute("CREATE TABLE `Alerts` (`Timestamp` DATETIME, `Key` TEXT,`Value` TEXT);")
        c.execute("CREATE TABLE `Users` (`uid` INTEGER NOT NULL, `gid` INTEGER NOT NULL, `user` TEXT NOT NULL, `hash` TEXT, PRIMARY KEY(uid));")
        print "Database created"
    except:
        print "Database table creation failed"
        quit()
    try:
        conn.commit()
        conn.close()
    except:
        print "Database commit failure"
        quit() 

    return True;

# Database Connection
def dbConnect():
    if os.path.isfile(db) == False:                                         # Check if database already exists
        print "Database not found, creating database in %s" % db
        dbCreate()                                                          # Initialise Database
    global conn, cursor 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    print "Database connection established"
   
# Close open DB connections
def dbClose():
    try:
        global conn, cursor
        conn.close()
        print "Database Connection Closed"
        return True;
    except:
        print "Database failed to close"
        return False;

def query(query):
    global conn, cursor
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result;
    except:
        return "Query Failed %s" % query;



def result(query):
    global conn, cursor
    cursor.execute(query)
    return cursor.rowcount;
    
# Setup Database


