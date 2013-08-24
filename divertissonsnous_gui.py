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

def wget(lbl,bar,url,filename):
	try:
		u = urllib.urlopen(url)
		f = open(filename, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		#print "Downloading: %s Bytes: %s" % (filename, file_size)
		file_size_dl = 0
		block_sz = 1024*1024
		txt= "Parse url : " + url+"\nSave file as : "+filename
		lbl.config(text=txt)
		lbl.update_idletasks()
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break
			file_size_dl += len(buffer)
			f.write(buffer)
			status = file_size_dl / float(file_size)
			if noTix_flag:
				strz = str(file_size_dl) +"/" + str(file_size) +"\t( " + str(int(status*100)) + "% )"
				
				bar.config(text=strz)
				bar.update_idletasks()
			else:
				bar.config(value=status)
				bar.update()
		f.close()
	except IOError as e:
		print e
	
def get_filename(url):
	 m = re.search('video*.*/(.*.mp4)', url)
	 if m is None:
		print "Warning : no found filename from url"
		print "filename will be : empty.mp4"
		return "empty.mp4"
	 else:
		filename = m.group(1)
		#print 'filename =', filename
		return filename
		
def get_video_url(url):
	data = urllib.urlopen(url).read();
	new= data.split('<div class="entry-content">',1)
	new= new[1].split('<div class="undervid">',1)
	new= new[0].split('http://www.divertissonsnous.com/player/player/playerdn.swf',1)
	m = re.search('\"file\":\"(http://www.divertissonsnous.com*.*.mp4)', new[1])
	if m is None:
		return None
	else:
		url = m.group(1)
		print 'url =',url
		return url

def onClick():
	init_url=entry.get()
	url = get_video_url(init_url)
	
	if url is None:
		print "Erreur : video url not found"
		sys.exit(0)
	else:
		filename = get_filename(url)
		
	win.destroy()
	
	mainwin= Tix.Tk()
	mainwin.title("Divertissonsnous.com !")
	container= Tix.Frame(mainwin)
	container.pack()
	
	#lbl = Tix.Label(container,text=filename, width=70)
	lbl = Tix.Label(container,text=filename)
	lbl.pack()
	if noTix_flag:
		#bar = Tix.Label(container,text="" , width=70)
		bar = Tix.Label(container,text="")
		
	else:
		bar=Tix.Meter(container, value=0.0)
	bar.pack()
	wget(lbl,bar,url,filename)
	#mainwin.destroy() # uncomment to close after complete download
	
win = Tix.Tk()
win.title("Divertissonsnous.com !")
frame = Tix.Frame(win, width=768, height=576, borderwidth=1)
frame.pack()

lbl = Tix.Label(frame,text="post DN url !")
lbl.pack() #attach label to window 
urlz = "http://www.divertissonsnous.com/2013/08/08/lechauffement-sexy-de-la-surfeuse-anastasia-ashley/"

entry = Tix.Entry(frame , width=90)
entry.pack() 
entry.focus_set()
entry.insert(0, urlz)

bouton= Tix.Button(frame, text="Valid", command=onClick)
bouton.pack() 
win.mainloop()
