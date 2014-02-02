import webpy.web as web
import hdhomerun as hdhr
import time

def initConfig(db):
    ''' Initialize the config table. If exists drop and recreate '''
    sql_query = "CREATE TABLE config (id integer primary key, name text, value text);"
    try:
        db.query(sql_query)
    except:
        sql_query2 = "DROP TABLE config;"
        db.query(sql_query2)
        db.query(sql_query)

def getConfig(db):
    try:
        configs = db.select("config")
    except:
        return None
    
    config = {}
    for cfg in configs:
        config[cfg.name] = cfg.value
    return config
    
def updateConfig(db):
    '''Finds the HDHomerun on the network and updates database'''
    
    # find hdhomerun
    hdhr_dev = hdhr.cfg.getDevice()
    
    # add hdhomerun to config table
    db.multiple_insert("config", values=hdhr_dev)
    return getConfig(db)
    
def initChannels(db):
    ''' Initialize the channels table. If exists drop and recreate '''
    sql_query = "CREATE TABLE channels (id integer primary key, name text, number text, favorite boolean, icon text);"
    try:
        db.query(sql_query)
    except:
        #sql_query2 = "DROP TABLE channels;"
        #db.query(sql_query2)
        #db.query(sql_query)
        pass
        
def getChannels(db):
    try:
        channels = db.select("channels")
    except:
        return None
    
    return channels
    
def updateChannels(db):
    '''Retrieves channel listing from the hdhomerun'''
    # get hdhomerun ip from database
    config = getConfig(db)
    
    # get channels from hdhomerun
    channels = hdhr.chan.getChannels(config['ip'])
    
    # add channels to table
    db.multiple_insert("channels", values=channels)
    
    return getChannels(db)
    