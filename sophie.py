import urllib
import os
import re 
import sys 
import time

noTix_flag=0
try:
	import Tix
	root = Tix.Tcl()
	del(root)
	
except Exception as e:
	print e
	import Tkinter as Tix
	noTix_flag=1
	print "Warning : Next time install \"tix\" package"

def wget(lbl,url,filename):
	try:
		u = urllib.urlopen(url)
		f = open(filename, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		#print "Downloading: %s Bytes: %s" % (filename, file_size)
		file_size_dl = 0
		block_sz = 1024*1024
		txt= "Parse url : " + url+"\nSave file as : "+filename
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break
			file_size_dl += len(buffer)
			f.write(buffer)
			status = file_size_dl / float(file_size)
		f.close()
	except IOError as e:
		print e
	
def get_filename(url):
	 m = re.search('http*.*/(.*.jpg)', url,re.IGNORECASE)
	 if m is None:
		print "Warning : no found filename from url"
		print "filename will be : empty.mp4"
		return "empty.jpg"
	 else:
		filename = m.group(1)
		#print 'filename =', filename
		return filename
		
def get_video_url(url):
	data = urllib.urlopen(url).read();
	#m = re.findall('(http://img.over-blog.com[\S]*.jpg)', data,re.IGNORECASE)
	m = re.findall('(http://img.over-blog.com[\S]*broderie[\S]*.jpg)', data,re.IGNORECASE)
	if m is None:
		print "warning : no found filename from url"
		print "filename will be : empty.mp4"
		return "empty.jpg"
	else:
		#print m
		return m

def onClick():
	init_url=entry.get()
	urls = get_video_url(init_url)
	if urls is None:
		print "Erreur : video url not found"
		sys.exit(0)
	else:
		for url in urls:
			print url
			filename = get_filename(url)
			wget(lbl,url,filename)
		win.destroy()
win = Tix.Tk()
win.title("bonheursophie !")
frame = Tix.Frame(win, width=768, height=576, borderwidth=1)
frame.pack()

lbl = Tix.Label(frame,text="post  url !")
lbl.pack() #attach label to window 
urlz = "http://bonheursophie.over-blog.com/"

entry = Tix.Entry(frame , width=90)
entry.pack() 
entry.focus_set()
entry.insert(0, urlz)

bouton= Tix.Button(frame, text="Valid", command=onClick)
bouton.pack() 
win.mainloop()
