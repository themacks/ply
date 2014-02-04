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
    def PUT(self):
        get_data = web.input(channel="", logo="")
        print "Setting: "+get_data.channel+" logo to "+get_data.logo
        dbase = web.database(dbn="sqlite", db="hdtc.db")
        db.setLogo(dbase, get_data.channel, get_data.logo[:-4])
        return
        
class tune:
    def POST(self, channel):
        print "Tunning to "+channel
        return "Tuning"
        
class status:
    def GET(self, channel):
        print "Status of "+channel
        return "Status"
        
class stop:
    def POST(self, channel):
        print "Stopping "+channel
        return "Stopping"
        
class stream:
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
    app = web.application(urls, globals())
    app.run()
