#!/usr/bin/env python
#--*--coding:UTF-8 --*--

import re
import sys
import os
from urllib2 import *
import urllib
import cookielib
import codecs
from bs4 import BeautifulSoup




class Web():
	
	def __init__(self):
		self.cj = cookielib.CookieJar()
		self.opener = build_opener(
						HTTPHandler(),
						HTTPSHandler(),
						HTTPErrorProcessor(),
						HTTPRedirectHandler(),
						HTTPCookieProcessor(self.cj) )

	def login(self, login_action_form_url , params_dic, method="POST", headers=None):
		"""
			 login method
			 params is a dict or a string formated
		""" 
		if isinstance(params_dic, dict):
			params= urllib.urlencode(params_dic)
		
		if method=="GET":
			self.get(url=login_action_form_url, params=params_dic, headers=headers)
			#self.get(url=login_action_form_url)
		elif method =="POST":
			self.post(url=login_action_form_url, params=params_dic, headers=headers)
			#self.post(url=login_action_form_url)
		else:
			pass
	
	def get(self, url, params=None, headers=None):
		if params is not None:
			url = url + params
		try:
			reponse = self.opener.open( url,None,headers)
			#print response.info()
			#print "Code", response.getcode()
			#print "headers", response.headers
			#print "msg", response.msg
			#print "new url", response.url
			if reponse.getcode() == 200 and reponse.msg == "OK":
				return reponse.read()
			else:
				print "http code" , reponse.getcode()
				return None

		except HTTPError as e:
			print e

	def post(self, url, params=None, headers=None):
		try:
			reponse = self.opener.open( url,params,headers)
			#print response.info()
			#print "Code", response.getcode()
			#print "headers", response.headers
			#print "msg", response.msg
			#print "new url", response.url
			if reponse.getcode() == 200 and reponse.msg == "OK":
				return reponse.read()
			else:
				print "http code" , reponse.getcode()
				return None
				
		except HTTPError as e:
			print e
		
	def get_Cookie(self):
		return self.cj

class GKS():

	def __init__(self, usr , passwd):
		self.web = Web()
		self.usrnm = usr
		self.passwd = passwd
		self.login()
		
	def login(self):
		auth_url = "https://gks.gs/login"
		params = urllib.urlencode(dict(username= self.usrnm ,
								password= self.passwd,
								login ="+Connexion+"))
		return self.web.login(auth_url , params, "POST", None)
		
	def get_Page(self,url):
		return self.web.get( url, params=None, headers=None)
	
	def wget(self,url,file_path):
		print "\twget url", url
		#print "\twget path", file_path
		try:
			html = self.get_Page(url)
			if html is not None:
				fd = open(file_path,"wb")
				fd.write(html)
				fd.close()
		except IOError as e:
			print 'file cannot be opened ' + file_path + str(e)
			

	def get_Cookies(self):
		cj = self.web.get_Cookie()
		uid = cj._cookies['.gks.gs']['/']['uid'].value
		pw = cj._cookies['.gks.gs']['/']['pw'].value
		print "GKS uid cookie", uid ,"\nGKS pw cookie", pw
		return uid, pw

	def get_Pic(self,url):
	
		"https://s.gks.gs/img/img/06-2013/Bien_demarrer_sur_gks.png"
		
		path = url.replace("https://s.gks.gs/img/","")
		#os.path.basename(url)
		path = reduce(os.path.join, path.split('/') )
		#path = os.path.join(os.getcwd(),wiki_img_folder,path)
		path = os.path.join(wiki_img_folder,path)
		if not os.path.exists(path):
			folders = os.path.dirname(path)
			if not os.path.exists(folders):
				os.makedirs(folders)
			self.wget(url,path)

if __name__ == "__main__":
	wiki_url = "https://gks.gs/wiki/"
	wiki_img_folder = "img"
	user = "xnl"
	passwd = "ertyuiop"
	g = GKS( user, passwd)
	#g.get_Cookies()
	g.get_Pic("https://s.gks.gs/img/img/01-2014/Wiki_GKS_2k14_final2.png")
	#g.wget("https://s.gks.gs/img/img/01-2014/Wiki_GKS_2k14_final2.png","Wiki_GKS_2k14_final2.png")
	g.wget(wiki_url,"wiki.html")
	
	
	
