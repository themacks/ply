import web
import hdhomerun as hdhr
import db
from os import listdir

render = web.template.render('templates/')

urls = (
    '/channels', 'channels',
    '/channels/favorites', 'favorites',
    '/channels/logo', 'logo',
    '/channels/(.*)/tune', 'tune',
    '/channels/(.*)/status', 'status',
    '/channels/(.*)/stop', 'stop',
    '/channels/(.*)', 'stream',
    '/setup', 'setup',
    '/update', 'update',
    '/', 'index'
)

class index:
    ''' Displays channel list allowing for setting favorites and logos '''
    def GET(self):
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        files = listdir("static/logos/")
        logos = [ f for f in files if f.endswith(".png") ]
        return render.index(dbase.select("channels"), logos)

class channels:
    ''' Retrieves channel lineup in json format for display by roku channel '''
    def GET(self):
        get_data = web.input(type="all")
        
        # connect to database
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        
        #find all channels
        channels = db.getChannels(dbase, get_data.type)
        return channels
        
class favorites:
    ''' Handles adding and deleting favorite channels '''
    def PUT(self):
        get_data = web.input(channel="")
        print "Adding: "+get_data.channel
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        db.setFavorite(dbase, get_data.channel, True)
        return
    def DELETE(self):
        get_data = web.input(channel="")
        print "Deleting: "+get_data.channel
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        db.setFavorite(dbase, get_data.channel, False)
        return
        
class logo:
    ''' Handles changing channel logo '''
    def PUT(self):
        get_data = web.input(channel="", logo="")
        print "Setting: "+get_data.channel+" logo to "+get_data.logo
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        db.setLogo(dbase, get_data.channel, get_data.logo[:-4])
        return
        
class tune:
    ''' Tunes HDHR and starts ffmpeg hls process '''
    def POST(self, channel):
        pid = hdhr.stream.startStream(channel)
        print "Tunning to "+channel+", pid: "+str(pid)
        
class status:
    ''' Reports status of HDHR tuning and HLS process '''
    def GET(self, channel):
        status = hdhr.stream.getStatus(channel)
        print "Status of "+channel
        print status
        
class stop:
    ''' Cleans up streaming files and releases tuner '''
    def POST(self, channel):
        hdhr.stream.stopStream(channel)
        print "Stopping "+channel
        
class stream:
    ''' redirects to ffmpeg generated .m3u8 file '''
    def GET(self, channel):
        print "Streaming "+channel
        raise web.seeother('/static/streams/'+channel)
        
class setup:
    ''' Initial setup. Should only be called once or to reset database. '''
    def GET(self):
        # connect to database
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        
        # initialize config table
        db.initConfig(dbase)
        
        # update configuration
        config = db.updateConfig(dbase)
        
        # initialize channels table
        db.initChannels(dbase)
        
        # update channels
        channels = db.updateChannels(dbase)
        
        # print out the status page
        
class update:
    def GET(self):
        # update configuration
        config = db.updateConfig(dbase)
        
        # update channels
        channels = db.updateChannels(dbase)

if __name__ == "__main__":
    # Verify valid database
    # Verify presence of hdhomerun_config
    hdhr.cfg.hasHdHrCfg()
    # Verify presence of ffmpeg
    hdhr.stream.hasFFMPEG()
    
    app = web.application(urls, globals())
    app.run()
