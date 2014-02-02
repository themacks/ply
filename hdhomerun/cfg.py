import subprocess as sub

def getDevice():
    '''Finds HDHomeRuns on network'''
    status = sub.check_output(["hdhomerun_config", "discover"])
    hdhrid = status.split(" ")[2]
    hdhrip = status.split(" ")[5].rstrip()
    
    values = [{"name": "dev", "value": hdhrid}, {"name": "ip", "value": hdhrip}]
    return values