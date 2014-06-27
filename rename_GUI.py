#!/usr/bin/env python
"""
TODO
exception for windows long path
os.sep == '\\' # windows platform
if os.sep == '\\' and '\\\\?\\' not in path:
"""
import os
import re
import sys
import string
import time
import shutil
import stat
import Tkinter as tk
import tkFileDialog

topz=""

video_ext = ['mpeg','mpg','mp4','m4v','mkv','m2t','m2ts','ts','avi','mov','qt','ogm','wm', 'wmv','asf']
subttile_ext = ['srt','vtt','idx','ssa','sub','ttxt','rt','ssf','usf']
file_type= tuple( video_ext + map(string.upper, video_ext) )
sub_type= tuple( subttile_ext + map(string.upper, subttile_ext))

def get_parent_folder(file_path):
	dirz = os.path.dirname(file_path)
	#dir = os.path.abspath(os.path.join(f_path, os.pardir))
	return os.path.basename(os.path.normpath(dirz))

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
			if not name.endswith( file_type + sub_type ) :
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
	global topz
	fileName =  os.path.splitext(get_fileName(file_path))[0] #remove extension
	folderName = get_parent_folder(file_path)
	print "fileName",fileName
	print "folderName",folderName
	if topz != os.path.dirname(os.path.abspath(file_path)): #if file is directly in top folder
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


def list_folder(top):
	"""
		arg:
			top = top path directory
		function:
			list files in a folder
			and for each file
	"""
	global topz
	topz=top
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			if name.endswith(file_type):
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

def select_dir():
	global win
	win2 = tk.Tk()
	win2.withdraw()
	dirname = tkFileDialog.askdirectory(parent=win2,initialdir="/",title='Please select a directory')
	if os.path.exists(dirname):
		if os.path.isdir(dirname):			
			list_folder(dirname)
	entry.delete(0, tk.END)
	entry.insert(0, dirname)	
	win.deiconify() # show again

def onClick():
	top=os.path.abspath(entry.get())
	if top is None:
		print "Error : path not found"
		sys.exit(0)
	else:
		if os.path.exists(top):
			if os.path.isdir(top):
				list_folder(top)
		
	#win.destroy() # uncomment to close after complete


if __name__ == "__main__":
	win = tk.Tk()
	win.title("rename files by subfolders !")
	frame = tk.Frame(win, width=768, height=576, borderwidth=1)
	frame.pack()
	lbl = tk.Label(frame,text="Select root folder !")
	lbl.pack() #attach label to window

	entry = tk.Entry(frame , width=90)
	entry.pack()
	entry.focus_set()
	path = "D:\Revenge.S01.FRENCH.DVDRiP.XViD-EPZ"
	entry.insert(0, path)
	tk.Button(frame,text='Select Folder',command=select_dir).pack(side=tk.RIGHT)
	
	tk.Button(frame, text="Valid", command=onClick).pack(fill=tk.BOTH,expand=tk.YES)
	win.mainloop()
