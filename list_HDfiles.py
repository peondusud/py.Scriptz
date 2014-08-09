#!/usr/bin/env python
#--*--coding:UTF-8 --*--

import Tix
import os
import sys
import tkFileDialog

file_type=['mkv','m2t','m2ts','ts','mp4']

def list_folder(top):
	listz=[]
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			
			if name.endswith(tuple(file_type)):
				path = os.path.join(root, name)
				size = os.path.getsize(path)
				name=name.replace(" ",".")
				filz = (name.lower(), root, size)
				listz.append(filz) 
				
	return listz

def compz(v1,v2):
	if v1[0]<v2[0]:
		return -1
	elif v1[0]>v2[0]:
		return 1
	else:
		return 0

def writez(listz):
	try:
		path= "/media/backup.peon"
		#path=str( os.getcwd() ) + "/backup.peon"
		fd = open(path,'w')
		for elem in listz:
			path = os.path.join(elem[1], elem[0])
			strz=elem[0] + (100-len(elem[0]))*' ' + str(elem[2]/float(2**30)) + "\t\t "+elem[1]
			print strz
			fd.write(strz+ "\n")
			#fd.write(elem[0]+ " \t\t "+ str(elem[2]/float(2**30))+" \t\t "+elem[1] +"\n")
		fd.close()
	except Exception as e:
		print e

		
def pprintz(listz):
	strz=""
	for elem in listz:
		path = os.path.join(elem[1], elem[0])
		#strz += path + "(" + str(elem[2]/float(2**20)) +")\n"
		strz += path +"\n"
		
if __name__ == '__main__':
	"""
	main = Tix.Tk()
	main.withdraw() 
	dirz = tkFileDialog.askdirectory(parent=main,initialdir="/media/StoCk_3To/007/",title="Please select a directory")
	print "dir :",dirz
	#l = list_folder(dirz)
	"""
	l=list_folder("/media/StoCk_3To/")
	l.extend(list_folder("/media/StoCk_3To_2/"))
	l.extend(list_folder("/media/StoCk_3To_3/"))
	l.extend(list_folder("/media/StoCk_3To_4/"))
	l.sort(cmp=compz)
	
	
	#for elem in l:
		#print elem
	writez(l)
	
	#raw_input()
