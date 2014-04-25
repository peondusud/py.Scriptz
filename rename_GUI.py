#!/usr/bin/env python
import os
import re
import sys
import time
import shutil
import stat
file_type=['mp4','mkv','m2t','m2ts','ts','avi']
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

def get_parent_folder(file_path):
	dir = os.path.dirname(file_path)
	#dir = os.path.abspath(os.path.join(f_path, os.pardir))
	return os.path.basename(os.path.normpath(dir))

def get_file_extension(file_path):
	fileExtension = os.path.splitext(file_path)[1]
	return fileExtension

def get_fileName(file_path):
	fileName = os.path.basename(file_path)
	return fileName


def rm_files_into_dir(top):
	"""
	remove all subfiles from a top directory except subtitle and video files
	"""
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:			
			if not name.endswith( tuple(file_type) + ("srt",) ) :
				path= os.path.join(root, name)
				#print "rm_files",path
				os.chmod(path, stat.S_IWUSR)
				os.remove(path)

def has_UpperCase(fileName):
	"""
		if one word start with an upper case return True
		if any word start with an upper case return False
	"""
	for word in fileName.split('.'):
		if word.istitle():
			return True
	return False

def move_file2parent_folder(file_path):
	new_path = os.path.join( os.path.dirname(os.path.dirname(file_path)), get_fileName(file_path))
	print"move", new_path
	os.rename(file_path,new_path)
	
	
def rename_filename_by_folder(file_path,move_to_parent_directory=True):
	if move_to_parent_directory:
		new_path= os.path.dirname(file_path) + get_file_extension(file_path)
	else:
		new_path=os.path.join(os.path.dirname(file_path), get_parent_folder(file_path)) + get_file_extension(file_path)
	os.rename(file_path,new_path)
	print "before",file_path
	print "after",new_path


def check_bigger_size_file_folder_name(file_path):
	fileName =  os.path.splitext(get_fileName(file_path))[0] #remove extension
	folderName = get_parent_folder(file_path)
	print "fileName",fileName
	print "folderName",folderName
	if fileName == folderName:
		print "=dont change filename"
		move_file2parent_folder(file_path)
	elif len(fileName) > len(folderName):
		if not has_UpperCase(fileName):
			print "need to change filename by folder name"
			rename_filename_by_folder(file_path)
		else:
			print "dont change filename"
			move_file2parent_folder(file_path)
	elif len(fileName) == len(folderName):
		if not has_UpperCase(fileName):
			print "need to change filename by folder name"
			rename_filename_by_folder(file_path)
		else:
			print "dont change filename"
			move_file2parent_folder(file_path)
	else :
		print "need to change filename by folder name"
		rename_filename_by_folder(file_path)


def list_folder(top,dont_ask=True):
	"""
		arg:
			top = top path directory
			dont_ask = don't ask the user to rename each file
		function:
			list files in a folder
			and for each file
	"""
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			if name.endswith(tuple(file_type)):
				path = os.path.join(root, name)
				if os.path.getsize(path) < 20*1024*1024: #to remove sample file
					os.chmod(path, stat.S_IWUSR)
					os.remove(path)
					continue
				print "\npath", path, "\nroot", root, "\nname", name
				
				check_bigger_size_file_folder_name(path)

		for dir in dirs:
			#print "\nDIR", dir
			rm_files_into_dir(top)
			os.rmdir(os.path.join(root, dir))


def onClick():
	top=entry.get()
	if top is None:
		print "Erreur : path not found"
		sys.exit(0)
	else:
		list_folder(top,False)
		
	win.destroy()
	#mainwin.destroy() # uncomment to close after complete download


if __name__ == "__main__":
	win = Tix.Tk()
	win.title("rename files by subfolders !")
	frame = Tix.Frame(win, width=768, height=576, borderwidth=1)
	frame.pack()
	lbl = Tix.Label(frame,text="root folder !")
	lbl.pack() #attach label to window


	entry = Tix.Entry(frame , width=90)
	entry.pack()
	entry.focus_set()
	path = "D:\Revenge.S01.FRENCH.DVDRiP.XViD-EPZ"
	entry.insert(0, path)

	bouton= Tix.Button(frame, text="Valid", command=onClick)
	bouton.pack()
	win.mainloop()
