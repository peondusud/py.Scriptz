#!/usr/bin/env python
#--*--coding:UTF-8 --*--

#import Tkinter as Tk
import Tix
import tkFileDialog
import warez
import mongo

main = Tix.Tk()
main.withdraw() # we don't want a full GUI, so keep the root window from appearing
dirz = tkFileDialog.askdirectory(parent=main,initialdir="/media/",title="Please select a directory")
print "dir :",dirz

if dirz is not "":
	listz = warez.list_folder(dirz)	#list files in a folder and for each create a warez object
	warez.listz2xml(listz)	#save list of warez object 
	
	
	
	#recover_old_filename(listz)	#change the filename by the original value for each warez object in list

	#listz = extract_list_from_xml( str( os.getcwd() ) + "/backup.xml" )	#recover a list of warez objects from a xml file

	listz = warez.listz2diclist(listz)
	
	disk ="disk_test"
	mongo.add_database(disk ,listz)
	mongo.show_database_disk(disk)
