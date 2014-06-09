#!/usr/bin/env python
#--*--coding:UTF-8 --*--

import re
import sys
import os
import codecs
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution



class Wiki_article:
	def __init__(self,id,html):
		self.titre=""
		self.id=""
		self.html=html
		self.content=""
		self.wiki_html=""
		self.extract_content()
		#self.extract_title()
		#self.extract_wiki()
		#self.check_links()
		
	def extract_content(self):
		soup = BeautifulSoup(self.html, from_encoding="utf-8")
		content = soup.find("div", {"id" : "contenu"})
		#print dir(content)
		#print help(content)
		for x in dir(content):
			print "\t", x.title() ,type(getattr(content, x))
		print content.parent
		#print type(content)
		if content is not None:
			#todo test all function to find the best
			#print content.string
			#print content.contents
			#print content.getText()
			#print content.get_text() #Get all child strings, concatenated using the given separator.
			#print content.getText()
			#print content.Text()
			#print content.Name()
			#print content.strings # Get all child strings, concatenated using the given separator.
			
			print "title", soup.title.string
			
			with open("wiki_content.html", "wb") as myfile:
				
				myfile.write(EntitySubstitution.substitute_html(unicode(content)).encode("UTF-8"))
				#myfile.write(EntitySubstitution.substitute_html(unicode(content)).encode("UTF-8"))
				#myfile.write(unicode(content.prettify(formatter="html")).encode("UTF-8"))
				"""
				for elem in content.contents:
					print type(elem)
					myfile.write(elem.encode("UTF-8"))
				"""
			print "content",type(content)
			#self.content = content.string
			self.content = content.contents
			print type(self.content)
			print len(self.content)
			
	def extract_title(self):
		#print self.content
		soup = BeautifulSoup(self.content)
		print soup.title.string
		#contentz = soup.find("p", {"class_" : "separate"})
		contentz = soup.find("p", {"class" : "separate"})
		if contentz is not None:
			print "title ", contentz.string
			self.title = contentz.string
			
	def extract_wiki(self):
		soup = BeautifulSoup(self.content)
		#content = soup.find("div", {"id" : "wiki_footer"})
		#content = soup.find("div", {"id" : "head_notice_left"})
		content = soup.find("div", {"id" : "wiki_article"})
		if content is not None:
			print  content.string
			self.wiki_html = content.string

	def check_links(self):
		soup = BeautifulSoup(self.wiki_html)
		#links starting with http://
		#soup.findAll('a', attrs={'href': re.compile("^http://")})
		for link in soup.findAll('a'):
			print "href" ,link.get('href')
	
	def modify_links(self):
		soup = BeautifulSoup(self.wiki_html)
		#links starting with http://
		#soup.findAll('a', attrs={'href': re.compile("^http://")})
		for link in soup.findAll('a'):
			print "href" ,link.get('href')
			newTag = Tag(soup, "a", link_tag.attrs)
			newTag.insert(0, ''.join(link_tag.contents))
			link_tag.replaceWith(newTag)
	
	def check_imgs(self):
		soup = BeautifulSoup(self.wiki_html)
		#soup.findAll('img', attrs={'src': re.compile("^https://")})
		for link in soup.findAll('img'):
			print "img" ,link.get('src')
	
	def printz(self):
		print "\n\t\tWiki Title ", self.titre
		print "\n\t\toriginal html", self.html
		print "\n\t\twiki html", self.wiki_html


if __name__ == "__main__":
	try:
		fd = open("C:\\Users\\Xnl\\Desktop\\wiki.html", 'rb')
		html = fd.read()
		fd.close()
		#print html
		Wiki_article(1,html)
		
	except IOError :
		print "error"
