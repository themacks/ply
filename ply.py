import web
import hdhomerun as hdhr
import db
import json
import sqlite3
from os import listdir

render = web.template.render('templates/')
dbase = web.database(dbn="sqlite", db="hdtc.db")
dbInit = False

urls = (
    '/channels', 'channels',
    '/channels/favorites', 'favorites',
    '/channels/logo', 'logo',
    '/channels/(.*)/tune', 'tune',
    '/channels/(.*)/status', 'status',
    '/channels/(.*)/stop', 'stop',
    '/channels/(.*)', 'stream',
    '/device/(.*)', 'device',
    '/setup', 'setup',
    '/init', 'init',
    '/', 'index'
)

class index:
    ''' Displays channel list allowing for setting favorites and logos '''
    def GET(self):
        files = listdir("static/logos/")
        logos = [ f for f in files if f.endswith(".png") ]
        try:
            channels = dbase.select("channels")
        except sqlite3.OperationalError:
            channels = None
        return render.index(channels, logos)

class channels:
    ''' Retrieves channel lineup in json format for display by roku channel '''
    def GET(self):
        get_data = web.input(type="all")
        return json.dumps(db.getChannels(dbase, get_data.type))
        
class favorites:
    ''' Handles adding and deleting favorite channels '''
    def PUT(self):
        get_data = web.input(channel="")
        db.setFavorite(dbase, get_data.channel, True)
        return
    def DELETE(self):
        get_data = web.input(channel="")
        db.setFavorite(dbase, get_data.channel, False)
        return
        
class logo:
    ''' Handles changing channel logo '''
    def PUT(self):
        get_data = web.input(channel="", logo="")
        db.setLogo(dbase, get_data.channel, get_data.logo[:-4])
        return
        
class tune:
    ''' Tunes HDHR and starts ffmpeg hls process '''
    def POST(self, channel):
        get_data = web.input(quality="heavy")
        devices = db.getDevices(dbase)
        hdhr.stream.startStream(channel,devices,get_data.quality)
        
class status:
    ''' Reports status of HDHR tuning and HLS process '''
    def GET(self, channel):
        return hdhr.stream.getStatus(channel)
        
class stop:
    ''' Cleans up streaming files and releases tuner '''
    def POST(self, channel):
        hdhr.stream.stopStream(channel)
        
class stream:
    ''' redirects to ffmpeg generated .m3u8 file '''
    def GET(self, channel):
        raise web.seeother('/static/streams/'+channel)

class device:
    ''' Manages devices in database '''
    def PUT(self,devId):
        db.addDevice(dbase,devId)
    def DELETE(self,devId):
        db.deleteDevice(dbase,devId)
    def GET(self,devId):
        db.updateChannels(dbase,devId)

class setup:
    def GET(self):
        netDevices = hdhr.cfg.getDevices()
        dbDevices = db.getDevices(dbase)
        return render.setup(netDevices,dbDevices)
        
class init:
    ''' Initial setup of database. Should only be called once or to reset database. '''
    def GET(self):
        # initialize channels table
        db.initChannels(dbase)
        
        # initialize device table
        db.initDevices(dbase)
        
        # redirect to setup page
        raise web.seeother('/setup')

if __name__ == "__main__":
    # Verify presence of hdhomerun_config
    hdhr.cfg.hasHdHrCfg()
    # Verify presence of ffmpeg
    hdhr.stream.hasFFMPEG()
    
    app = web.application(urls, globals())
    app.run()
