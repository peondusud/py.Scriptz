#!/usr/bin/env python
#--*--coding:UTF-8 --*--

import re
import sys
import os
import codecs
import pickle
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
from gs_web import *

"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="fr" xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">
    <head></head>
    <body id="body">
        <div id="global">
            <div id="entete"></div>
            <div id="centre">
                <div id="navigation"></div>
                <div id="contenu">
                    <p class="separate"></p>
                    <div id="head_notice_left"></div>
                    <div id="wiki_article"></div>
                    <div id="wiki_footer"></div>
"""

class GKS_Wiki:
	def __init__(self,idz,html):
		self.full_soup=None
		self.page_title=""
		self.wiki_title=""
		self.idz=idz
		self.html=html
		self.content=""
		self.wiki_html=""

		self.extract_content()
		self.extract_titles()
		if self.wiki_title.find("Erreur - 404 -  Article inexistant") == -1:
			self.extract_wiki()
			#self.check_links()
			#self.check_imgs()
			self.modify_img_links()
		
	def extract_content(self):
		soup = BeautifulSoup(self.html, from_encoding="utf-8")
		self.full_soup = soup
		content = soup.find("div", {"id" : "contenu"})

		#content.parent # full page
		if content is not None:
			#self.content = EntitySubstitution.substitute_html(unicode(content)
			#self.content = unicode(content.prettify(formatter="html"))
			self.content = unicode(content)
			
			#with open("wiki_content.html", "wb") as fp:
				#fp.write(self.content.encode("UTF-8"))

	def extract_titles(self):
		
		self.page_title = self.full_soup.head.title.string
		#print "page title", self.page_title
		
		content_soup = BeautifulSoup(self.content, from_encoding="utf-8")
		contentz = content_soup.find("p", {"class" : "separate"})
		if contentz is not None:
			self.wiki_title = contentz.string.lstrip()
			try:
			
				print "wiki title -> ["+unicode(self.idz)+"]", unicode(self.wiki_title)
			except UnicodeEncodeError:
				print "wiki id -> ["+unicode(self.idz)+"]"
			
	def extract_wiki(self):
		soup = BeautifulSoup(self.content, from_encoding="utf-8")
		wiki_content = soup.find("div", {"id" : "wiki_article"})
		if wiki_content is not None:		
			self.wiki_html = unicode(wiki_content)

	def check_links(self):
		wiki_soup = BeautifulSoup(self.wiki_html)
		#for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
		for link in wiki_soup.findAll('a',href=True):
			print "href" ,link.get('href')
	
	def modify_img_links(self):
		global folder2SavePic, fqdn_img , g
		
		soup = BeautifulSoup(self.wiki_html)
		for link in soup.findAll('img',src=True):
			#print "\nimg before " ,link.get('src')
			orig_url = str(link.get('src'))
			if orig_url.find("gks.gs") != -1:
				#print orig_url
				url = orig_url.replace("https://s.gks.gs/img/","")
				url = orig_url.replace("https://s.gks.gs/","")
				url = url.rsplit('/img/')[-1]
				url = url.rsplit('img/')[-1]
				url = url.rsplit('.php')[-1]	
				url = url.rsplit('?')[-1]
				url = url.rsplit('=')[-1]
				url = url.rsplit('http:')[-1]
				url = url.rsplit('https:')[-1]
				path = reduce(os.path.join, url.split('/') )
				url = fqdn_img + url
				link.attrs["src"]=url #modify img src
				
				path = os.path.join(folder2SavePic,path)
				if not os.path.exists(path):
					folders = os.path.dirname(path)
					if not os.path.exists(folders):
						os.makedirs(folders)
					g.wget(orig_url,path)				
			#print "timg after" ,link.get('src')

	
	def check_imgs(self):
		soup = BeautifulSoup(self.wiki_html)
		for link in soup.findAll('img',src=True):
			print "img" ,link.get('src')
	
	def printz(self):
		print "\n\t\tWiki Title ", self.titre
		print "\n\t\toriginal html", self.html
		print "\n\t\twiki html", self.wiki_html
	
	def getDict(self):
		dic = {}
		if self.wiki_title.find("Erreur - 404 -  Article inexistant") == -1:
			
			#dic["page_title"]=self.page_title		
			dic["wiki_title"]=self.wiki_title
			dic["orig_html"]=self.html
			#dic["wiki_html"]=self.wiki_html		
		return dic

		
def dirz(content):
	for x in dir(content):
		print "\t", x.title() ,type(getattr(content, x))



if __name__ == "__main__":
	wiki_url = "https://gks.gs/wiki/"
	user = "xnl"
	passwd = "ertyuiop"
	fqdn_img = "http://www.peondusud.org/img/"
	folder2SavePic = "C:\\Users\\Xnl\\Desktop\\img"
	
		
	g = GKS( user, passwd)
	fp = open("wikis.pickle", "wb")
	for idz in range(1,600):
		url = wiki_url+"?id="+str(idz)
		html = g.get_Page(url)
		wiki_article = GKS_Wiki(idz,html)
		
		dic = {idz: wiki_article.getDict() }
		
		pickle.dump(dic,fp)
	fp.close
			
	"""
	fp = open("wikis.pickle", "rb")
	data = pickle.load(fp)
	fp.close
	"""
	


