import urllib
import os
import re
import sys
import time
import argparse

def wget(url,filename):
    try:
        u = urllib.urlopen(url)
        f = open(filename, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (filename, file_size)

        file_size_dl = 0
        block_sz = 1024*1024*10
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
            sys.stdout.flush();

        f.close()
    except IOError as e:
        print e
    
def get_filename(url):
     m = re.search('video*.*/(.*.mp4)', url)
     if m is None:
         print "Warning : no found filename from url"
         print "filename will be : empty.tmp"
         return "empty.tmp"
     else:
         filename = m.group(1)
         print 'filename =', filename
         return filename
         
def get_video_url(url):
    
      data = urllib.urlopen(url).read();      
      new= data.split('<div class="entry-content">',1)
      new=new[1].split('<div class="undervid">',1)
      new=new[0].split('http://www.divertissonsnous.com/player/player/playerdn.swf',1)
      m = re.search('\"file\":\"(http://www.divertissonsnous.com*.*.mp4)', new[1])
      if m is None:
          return None
      else:
          url = m.group(1)
          print 'url =',url
          return url
          
           
if __name__ == '__main__':
    
    init_url = "http://www.divertissonsnous.com/2013/06/27/une-francaise-se-crashe-en-tyrolienne/";
    
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument('url', metavar='url'  , type=str, help='Divertissonsnous.com URL')
    arg = arg_parse.parse_args()
    
    #comment line below to try static url
    init_url = arg.url
    
    url = get_video_url(init_url)
    
    if url is None:
        print "Erreur : video url not found"
        sys.exit(0)
    else:
        filename = get_filename(url)  
        wget(url,filename)
        raw_input
