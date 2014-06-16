#!/usr/bin/env python
#--*--coding:UTF-8 --*--
import os
from re import match,compile,search
import sys
import time
import string
import shutil
import stat
import Tkinter as tk

file_type=['mp4','mkv','m2t','m2ts','ts','avi']
str2remove = ["BY DIGITAL PARADISE", "BY RazerPtigot", "upbyhamoudaxp for wawa mania", "by.ustoman.startimes2.com", "Up By Xlnzz", "AlFleNi-TeaM", "www.planet-series.tv", "ZLVR", "Mrx@prod", "arno122", "[Team-CompleX]","for wawa mania","[tvu.org.ru]"]
noTix_flag=0

class Gui(tk.Tk):
	def __init__(self, parent):
		#tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		
		self.frame = tk.Frame(self, width=900, height=576, borderwidth=1)
		self.frame.pack()
		
		self.label_entry_folder = tk.Label(self.frame,text="Serie folder !")
		#self.label_entry_folder.pack(anchor = tk.W )
		self.label_entry_folder.grid(column=0,row=0,sticky='E')
		
		self.entry_fold_var = tk.StringVar()
		#self.entry_fold_var.set("D:\Revenge.S01.FRENCH.DVDRiP.XViD-EPZ")
		self.entry_fold_var.set("K:\Magnum  saison 1  DVDRip XviD FR")
		self.entry_fold = tk.Entry(self.frame,textvariable=self.entry_fold_var, width=120)
		#self.entry_fold.pack(anchor = tk.E )
		self.entry_fold.grid(column=1,row=0,columnspan=2,sticky='W')
		
		
		self.lbl_entry_name = tk.Label(self.frame,text="Serie Name")
		#self.lbl_entry_name.pack(in_=self.frame,anchor = tk.W )
		self.lbl_entry_name.grid(column=0,row=1,sticky='E')
		
		self.name_var = tk.StringVar()
		self.name_var.set("Magnum")
		self.entry_name = tk.Entry(self.frame,textvariable=self.name_var , width=80)
		#self.entry_name.pack(in_=self.frame,anchor = tk.E )
		self.entry_name.grid(column=1,row=1,columnspan=2,sticky='W')
		
		
		self.radio_var = tk.StringVar()
		self.combined = tk.Radiobutton(self.frame, text="Season/Episode Combined RegEx", variable=self.radio_var, value="combined", command=self.selec_radio)
		self.splited = tk.Radiobutton(self.frame, text="Season/Episode Splited RegEx", variable=self.radio_var, value="splited", command=self.selec_radio)
		self.combined.select()
		#self.combined.pack(in_=self.frame,anchor = tk.W )
		#self.splited.pack(in_=self.frame,anchor = tk.W )
		
		self.combined.grid(column=0,row=2,rowspan=2,sticky='W')
		self.splited.grid(column=0,row=3,rowspan=3,sticky='W')
		
		
		self.lbl_entry_combined_regex = tk.Label(self.frame,text="Combined RegEx :")
		#self.lbl_entry_combined_regex.pack( anchor = tk.W)
		self.lbl_entry_combined_regex.grid(column=1,row=2,sticky='W')
		
		self.combined_regex = tk.StringVar()
		self.combined_regex.set("([01])x(\d\d)")
		#self.combined_regex.set("[Ss]?([01]?\d?)[eExX]?[pP]?(\d\d)")
		self.entry_combined_regex = tk.Entry(self.frame,textvariable=self.combined_regex , width=50)
		#self.entry_combined_regex.pack( anchor = tk.E)
		self.entry_combined_regex.grid(column=1,row=2,columnspan=2)
		
		self.lbl_entry_season_regex = tk.Label(self.frame,text="Season RegEx :")
		#self.lbl_entry_season_regex.pack(anchor = tk.W)
		self.lbl_entry_season_regex.grid(column=1,row=3,sticky='W')
		
		self.season_regex = tk.StringVar()
		self.season_regex.set("[Ss]?([01]?\d)")
		self.entry_season_regex = tk.Entry(self.frame,textvariable=self.season_regex , width=30)
		#self.entry_season_regex.pack(anchor = tk.E)
		self.entry_season_regex.grid(column=1,row=3,columnspan=2)
		
		self.lbl_entry_episode_regex = tk.Label(self.frame,text="Episode RegEx :")
		#self.lbl_entry_episode_regex.pack( anchor = tk.W)
		self.lbl_entry_episode_regex.grid(column=1,row=4,sticky='W')
		
		self.episode_regex = tk.StringVar()
		self.episode_regex.set("[eExX]?[pP]?(\d\d)")
		self.entry_episode_regex = tk.Entry(self.frame,textvariable=self.episode_regex , width=30)
		#self.entry_episode_regex.pack(anchor = tk.E)
		self.entry_episode_regex.grid(column=1,row=4,columnspan=2)
		
		self.selec_radio() #update entry from radio choice
		
		self.lbl_entry_info = tk.Label(self.frame,text="Other Info :")
		#self.lbl_entry_info.pack(anchor = tk.W)
		self.lbl_entry_info.grid(column=1,row=5,sticky='W')
		
		self.info_var = tk.StringVar()
		self.info_var.set("FRENCH DVDRip XviD")
		self.entry_info = tk.Entry(self.frame,textvariable=self.info_var , width=50)
		#self.entry_info.pack(anchor = tk.E)
		self.entry_info.grid(column=1,row=5,columnspan=2)
		
		
		self.lbl_entry_team = tk.Label(self.frame,text="Team :")
		#self.lbl_entry_team.pack(anchor = tk.W)
		self.lbl_entry_team.grid(column=0,row=6,sticky='E')
		
		self.team_var = tk.StringVar()
		self.team_var.set("EPZ,GKS,JMT,MiND,AUTHORiTY,HYBRiS,FYR,PAiN,JRabbit,HDZ,HTO,BAWLS,2T,PANZeR,BoO,F4ST,PROTEiGON")
		self.entry_team = tk.Entry(self.frame,textvariable=self.team_var , width=130)
		#self.entry_team.pack(anchor = tk.E)
		self.entry_team.grid(column=1,row=6,columnspan=2)
		
		
		self.check_var = tk.IntVar()
		self.check = tk.Checkbutton(self.frame, text="Check in Filename", variable=self.check_var,  onvalue = 1, offvalue = 0)
		self.check.select()
		#self.check.pack(anchor = tk.E )
		self.check.grid(column=2,row=6,sticky='E')
		
		self.bouton= tk.Button(self.frame, text="Valid", command=self.onValid)
		#self.bouton.bind( '<Return>' , self.onValid) #Nothing appends
		self.bouton.grid(column=1,row=7,columnspan=2)
		
		
	def selec_radio(self):
		if self.radio_var.get() == "combined":
			#print "combined true"
			self.lbl_entry_combined_regex.grid(column=1,row=2,sticky='W')
			self.entry_combined_regex.grid(column=1,row=2,columnspan=2)
			
			#self.season_regex=""
			#self.episode_regex=""
			self.lbl_entry_season_regex.grid_forget()
			self.entry_season_regex.grid_forget()
			self.lbl_entry_episode_regex.grid_forget()
			self.entry_episode_regex.grid_forget()
			
		elif self.radio_var.get() == "splited":
			#print "splited true"
			self.lbl_entry_combined_regex.grid_forget()
			self.entry_combined_regex.grid_forget()
			
			#self.combined_regex=""
			self.lbl_entry_season_regex.grid(column=1,row=3,sticky='W')
			self.entry_season_regex.grid(column=1,row=3,columnspan=2)
			self.lbl_entry_episode_regex.grid(column=1,row=4,sticky='W')
			self.entry_episode_regex.grid(column=1,row=4,columnspan=2)
	
	def print_status(self):
		print "process to call"
		print "Folder", self.entry_fold_var.get()
		print "Type Regex", self.radio_var.get()
		print "Serie Name", self.name_var.get()
		print "Combined RegEx",self.combined_regex.get()
		print "Season RegEx",self.season_regex.get()
		print "Episode RegEx",self.episode_regex.get()
		print "Other Info",self.info_var.get()
		print "Team Encoder",self.team_var.get()
		print "Check box",self.check_var.get()
		print

	def onValid(self):
		top=self.entry_fold_var.get()
		if top is None:
			print "Erreur : path not found"
			sys.exit(0)
		else:
			#self.print_status()
			for root, dirs, files in os.walk(top, topdown=False):
				for name in files:
					if name.endswith(tuple(file_type)):
						path = os.path.join(root, name)
						if os.path.getsize(path) > 40*1024*1024: #to remove sample file
							
							if self.radio_var.get() == "combined":
								self.season, self.episode = combined_algo(path ,self.combined_regex.get())
							elif self.radio_var.get() == "splited":
								self.season, self.episode = splited_algo(path ,self.season_regex.get(),self.episode_regex.get())
							#self.season = "%02i" % int("4")
							self.season = "%02i" % int(self.season)
							self.episode = "%02i" % int(self.episode)
							new_filename= self.name_var.get() + ".S" + self.season+ "E" + self.episode + "." + self.info_var.get().replace(" ",".") # need to add teamencoder
							if self.check_var.get() == 1:
								for team in self.team_var.get().split(","):
									if  (name.find(team) or name.find(team.lower())) != -1:
										new_filename = new_filename + "-" + team
										break
							else:
								if len(self.team_var.get().split(",")) == 1 :
									new_filename +=  "-" + self.team_var.get()
							new_filename +=  os.path.splitext(name)[1] # add extension
							new_filename = new_filename.replace("..",".")
							new_path = os.path.join(root, new_filename)
							#print "\nOriginal Filename :", name
							#print "New Filename :", new_filename
							print "Original path :", path
							print "New path \t:", new_path 
							os.rename(path,new_path)
							# last thing to do is to change filename
		#sys.exit(0) #to uncomment when no bug

def combined_algo(path,pattern):
	#pattern="[Ss]?([01]?\d?)[eExX]?[pP]?(\d\d)"
	
	filename= os.path.basename(path)
	#print filename
	prog = compile(pattern)
	m = prog.search( remove_cheat(filename) )
	if m is not None:
		listz = m.groups()
		season =  listz[0]
		episode = listz[1]
		return season, episode


def splited_algo(path, pat_season, pat_episode):
	#pat_season = "[Ss]?([01]?\d)"
	#pat_episode = "[eExX]?[pP]?(\d\d)"
	#pat_season = "[Ss]([01]\d)"
	#pat_episode = "(\d\d)"
	
	season = ""
	episode = ""
	filename= os.path.basename(path)
	#print filename
	prog = compile(pat_season)
	prg = compile(pat_episode)
	tmp = remove_cheat(filename)
	#print "tmp", tmp
	m = prog.search( tmp )
	if m is not None:
		season = m.groups()[0]
		#print "Season",Season
	else:
		tmp2 = get_parent_folder(path)
		tmp2 = remove_cheat(tmp2)
		m2 = prog.search( tmp2 )
		if m2 is not None:
			season = m2.groups()[0]
			#print "season",season
	m3 = prg.search( remove_cheat(filename) )
	if m3 is not None:
		episode = m3.groups()[0]
		#print "episode", episode
	return season,episode

def get_parent_folder(file_path):
	dir = os.path.dirname(file_path)
	#dir = os.path.abspath(os.path.join(f_path, os.pardir))
	return os.path.basename(os.path.normpath(dir))



def remove_cheat(strz):
	for elem in str2remove:
		if elem in strz:
			strz = strz.replace(elem,'')
	strz = string.replace(strz,' ', '.')
	strz = string.replace(strz,'..', '.')
	strz = string.replace(strz,'_', '.')
	strz = string.replace(strz,'-', '')
	strz = string.replace(strz,'(', '')
	strz = string.replace(strz,')', '')
	return strz

def test_algo(strz):
	pattern="[Ss]?([01]?\d?)[eExX]?[pP]?(\d\d)"
	
	strz= os.path.basename(strz)
	print strz
	prog = compile(pattern)
	m = prog.search( remove_cheat(strz) )
	if m is not None:
		listz = m.groups()
		season =  listz[0]
		episode = listz[1]
		if season == "":
			print "season", season
		print "episode", episode






if __name__ == "__main__":
	strz="Science.X.1x08.27.Decembre.2008.avi"
	strz="Brain.Games.S01E02.DOC.FRENCH.SDTV.XviD-SiNX"
	strz="Young.Americans.1x01.Secrets.FR.DVB-Azerty.[tvu.org.ru]"
	strz="epz-white.collar.201.l.architecte.avi"
	strz="V.(2009) S01x12 FINAL - Vostfr - arno122 [Team-CompleX] for wawa mania.avi"
	#strz="V.2009.S01E04.Mrx@prod.VOSTF..avi"
	#strz="Mon_Oncle_Charlie_S02_EP08_ZLVR.avi"
	strz="C:\\StoCk_Series\\Mon oncle Charlie S03\\01.avi"
	
	
	gui = Gui(None)
	gui.title("Rename Serie files!")
	gui.mainloop()
