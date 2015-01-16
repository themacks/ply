import urllib2 as url
import json

def getChannels(ipaddr):
    data = url.urlopen("http://"+ipaddr+"/lineup.json")
    response = data.read()
    data.close()
    channels = json.loads(response)
    
    values = []
    
    for channel in channels:
        try:
            if channel["Favorite"]:
                fav = True
            else: 
                fav = False
        except KeyError:
            fav = False
        values.append({"name":channel["GuideName"], "number":channel["GuideNumber"], "favorite":fav, "visible":True, "icon":""})
    return values
    