import web
import hdhomerun as hdhr
import db

render = web.template.render('templates/')

urls = (
    '/channels/(.*)', 'channels',
    '/setup', 'setup',
    '/', 'index'
)

class index:
    def GET(self):
        return render.index()

class channels:
    def GET(self):
        return "Channel List"
        
class setup:
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

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
