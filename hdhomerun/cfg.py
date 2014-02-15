import subprocess as sub

def hasHdHrCfg():
    ''' Checks for presence of hdhomerun_config '''
    try:
        status = sub.check_output(["which", "hdhomerun_config"])
    except:
        raise OSError("hdhomerun_config not found!")

def getDevices():
    '''Finds HDHomeRuns on network'''
    try:
        status = sub.check_output(["hdhomerun_config", "discover"])
    except:
        return None
    
    devices = status.split("\n")
    
    values = []
    for device in devices[:-1]:
        hddev = device.split(" ")[2]
        status = sub.check_output(["hdhomerun_config", hddev, "get", "/sys/features"])
        if status.find("transcode") == -1:
            trans = False
        else:
            trans = True
        values.append({"dev":hddev, "ip":device.split(" ")[5].rstrip(), "transcode":trans})
    return values
    
def getDevice(devId):
    ''' Returns IP address for specified device '''
    devices = getDevices()
    for device in devices:
        if device["dev"] == devId:
            return device
            
    return None
    
def getTunerStatus(devId):
    pass