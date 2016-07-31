# !/usr/bin/python
# -*- coding: utf-8 -*- 
#
##########################################################
#    
#    Filename:       darwin.py
#    Application:    Sentinel
#    App Version:    v0.1 (Alpha)
#    Description:    Mac OSX functions file
#    Author:         Matt Jouques
#    File Version:   0.1
#
##########################################################

# Dependencies
from core import dbQuery, hasher
import hashlib
import logging
import os

# Main Function
def Main():
    #Suid = hashlib.sha256(str(os.getuid() + uuid.getnode())).hexdigest()
    userlist = dbQuery("SELECT * FROM Users")
    for user in userlist:
        print user
    
    #checkUsers()
        
    return;










# Read Users
def readUsers():
    userListFile = '/etc/passwd'
    userFile = open(userListFile, 'r')
    userList = userFile.readlines()
    userFile.close()
    return userList;


# Update Users
def updateUsers():
    logging.debug("Update Users Function initiated")
    userListFile = '/etc/passwd'
    userList = readUsers()
    for line in userList: 
        if ":" in line:
            userHash = hasher(line)
            userDetail = line.split(":")
            sql = "INSERT OR REPLACE INTO Users (uid, gid, user, hash) VALUES ('%s', '%s', '%s', '%s')" % (str(userDetail[2]), str(userDetail[3]), userDetail[0], str(userHash))
            print sql
            dbQuery(sql)
    usersFileHash = hasher(userListFile)
    sql = "UPDATE Checks SET Key = 'Users', Value = '%s' WHERE Key = 'Users'" % (usersFileHash)
    dbQuery(sql)
    
    return;

# Check Users
def checkUsers():
    # Check if hash is populated
    userListFile = '/etc/passwd'
    dbUsersHash = core.dbQuery("SELECT Value FROM Checks WHERE Key = 'Users'")
    if not dbUsersHash:                                                                       # Not Populated
        logging.info("No User information held")
        tamperCheck()
        updateUsers()
    else:
        usersHash = core.hasher(userListFile)                               # TODO - CHECK THIS IS FILE
        if usersHash != dbUsersHash:                                                        # Check for change to Hash
            logging.warning("System Users have changed, initiating check for differences")
            with open(userListFile, 'rb') as userFile:
                userList = userFile.readlines()
                for line in userList:                                                              # Loop though the contents of the list
                    userHash = core.hasher(line)
                    query = "SELECT uid FROM user WHERE hash IS '%s'" % userHash
                    result = core.dbQuery(query)
                    if result == 0:
                        logging.critical("New User added to system")
                        
                    print query       
            userFile.close()                                                                           
    return;



# Check for application Tampering
def tamperCheck():
    logging.info("Tamper Check initiated")
    
    return;

























# Function to get the details of the system
def getUID():
    user = os.getuid()
    system = uuid.getnode()
    output = hashlib.sha1(user + system)
    return output;





# User Accounts - Have new user accounts been added?




#user = hashlib.sha1(pwd.getpwuid( os.getuid() )[ 0 ] + str(uuid())
#ky = user.hexdigest()



#print ky
# Check the current Hash
#BLOCKSIZE = 65536
#hasher = hashlib.sha1()
#with open('/Users/Matt/renamedFile', 'rb') as afile:
#    buf = afile.read(BLOCKSIZE)
#    while len(buf) > 0:
#        hasher.update(buf)
#        buf = afile.read(BLOCKSIZE)
#print(hasher.hexdigest())





# Programs listening on open ports - Is there a new program or process listening on a port

# Certificates - Has a new certificate been installed on your system?

# Firewall - Have new firewall rules been added to your system?


# Javascript execution checks - Are javascript files allowed to run on your machine? 