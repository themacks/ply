import subprocess as sub
''' ffmpeg -i stream.ts -map 0:0 -map 0:1 -vcodec copy -acodec copy -f segment -segment_list_flags live -segment_wrap 10 -segment_time 10.0 -segment_format mpegts -segment_list_size 10 -segment_list stream.m3u8 "segment%04d.ts" '''

def hasFFMPEG():
    ''' Checks for presence of ffmpeg '''
    try:
        status = sub.check_output(["which", "ffmpeg"])
    except:
        raise OSError("ffmpeg not found!")
