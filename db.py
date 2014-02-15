import web
import hdhomerun as hdhr
import time
import sqlite3

def initDevices(db):
    ''' Initialize the device table. If exists drop and recreate '''
    sql_query = "CREATE TABLE devices (id INTEGER PRIMARY KEY, dev TEXT NOT NULL UNIQUE, ip TEXT, transcode BOOLEAN);"
    try:
        db.query(sql_query)
    except:
        sql_query2 = "DROP TABLE devices;"
        db.query(sql_query2)
        db.query(sql_query)
        
def getDevices(db):
    ''' Returns all devices in database '''
    try:
        devices = db.select("devices")
    except:
        return None
        
    return devices
    
def getDevice(db, devId):
    ''' Returns device with id from database '''
    try:
        device = db.select("devices", where="dev=$devId", vars=locals())
    except:
        return None
        
    return device
    
def addDevice(db, devId):
    ''' Adds a new device to database '''
    device = hdhr.cfg.getDevice(devId)
    try:
        if getDevice(db,devId):
            db.update("devices", where="dev=$devId", ip=device["ip"], vars=locals())
        else:
            db.multiple_insert("devices", values=[device])
    except:
        print "Error adding device to database."
        
def deleteDevice(db, devId):
    ''' Delete device from the database '''
    try:
        db.delete("devices", where="dev=$devId", vars=locals())
    except:
        print "Error deleting from database."

def initChannels(db):
    ''' Initialize the channels table. If exists drop and recreate '''
    sql_query = "CREATE TABLE channels (id INTEGER PRIMARY KEY, name TEXT, number TEXT NOT NULL UNIQUE, favorite BOOLEAN, icon TEXT);"
    try:
        db.query(sql_query)
    except:
        sql_query2 = "DROP TABLE channels;"
        db.query(sql_query2)
        db.query(sql_query)
        pass
        
def getChannels(db, type):
    ''' returns all channes for roku channel '''
    try:
        if type == "favorites":
            channels = db.select("channels", where="favorite=1")
        else:
            channels = db.select("channels")
    except:
        return None
    
    addr = "http://"+web.ctx.host+"/static/logos/"
    chans = []
    for channel in channels:
        if len(channel["icon"]) > 0:
            icon = addr+channel["icon"]+".png"
        else:
            icon = addr+"default.png"
        chans.append({"GuideName":channel["name"], "GuideNumber":channel["number"], "LogoUrl":icon, "Favorite":channel["favorite"]})
    
    return {"channels":chans}
    
def updateChannels(db, devId):
    '''Retrieves channel listing from the hdhomerun'''
    # get hdhomerun ip from database
    device = hdhr.cfg.getDevice(devId)
    
    # get channels from hdhomerun
    channels = hdhr.chan.getChannels(device['ip'])
    
    # create list of new channels
    newChannels = []
    for channel in channels:
        status = db.select("channels", where="number=$channel['number']", vars=locals())
        newChannels.append(channel)
        
    # add channels to table
    if newChannels:
        db.multiple_insert("channels", values=newChannels)
    
    return
    
def setFavorite(db, channel, fav):
    db.update("channels", where="number=$channel", favorite=fav, vars=locals()) 
    
def setLogo(db, channel, logo):
    db.update("channels", where="number=$channel", icon=logo, vars=locals()) 