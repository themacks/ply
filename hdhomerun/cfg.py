import subprocess as sub

def hasHdHrCfg():
    ''' Checks for presence of hdhomerun_config '''
    try:
        status = sub.check_output(["which", "hdhomerun_config"])
    except:
        raise OSError("hdhomerun_config not found!")

def getDevice():
    '''Finds HDHomeRuns on network'''
    status = sub.check_output(["hdhomerun_config", "discover"])
    hdhrid = status.split(" ")[2]
    hdhrip = status.split(" ")[5].rstrip()
    
    values = [{"name": "dev", "value": hdhrid}, {"name": "ip", "value": hdhrip}]
    return values