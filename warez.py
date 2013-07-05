#!/usr/bin/env python
#--*--coding:UTF-8 --*--
#DXVA HRA WTF!!!

import sys
import os
import string
from argparse import ArgumentParser
from hashlib import  sha512,sha256
from re import match,compile,search
from xml.dom.minidom import parse, parseString, getDOMImplementation
#from threading import Thread
from xml.dom import minidom


sources_rip=['BluRay','HDRiP','DVDRiP','AHDTV','SDTV','PDTV','DVB','HDTV','.LD.','WEBRiP','.CAM.','DVDSCR','DTheater','BD5','BD9','R5','SATRiP','WEB.DL','DVD5']
l_quality=['1080p','1080i','720p','576p','576i','480p','480i','TrueHD']
flux=['AVC','x264','h264','MPEG2','XviD','MPEG4']
languages=['MULTi','TRUEFRENCH','FRENCH','USA','VOSTFR']
audios=['AAC20','DTS.HDMA','DTS','HRA','DD5.1','AC3','5.1']
versions=['LiMiTED','FESTiVAL','STV','UNCUT','UNRATED','RATED','BONUS','SUBFORCED','PROPER','FASTSUB','SUNSHINE.EDITION','REVISITED.FiNAL.CUT','DIRECTOR.CUT','THEATRICAL.CUT','REAL','EXTENDED','REMASTERED','REPACK','REMUX','CUSTOM','COMPLETE','FiNAL','PREAiR','RERIP','RETAIL','DOC']
file_type=['mp4','mkv','m2t','m2ts','ts']
teamz=['iND','iNT','iNTERNAL','ForceBleue','NOWiNHD','FrIeNdS','GAÏA','FHD','RLD','WiKi','.SS.','EbP','HidT','RuDe','HDxT','HDBRiSe','AMIABLE','DREAM','THENiGHTMAREiNHD','FYR','Slug','Ratat','HDZ','BiT','CiNEFOX','DiGiTAL','SoSo','ULSHDULSHD','HDFRENCH','PtS','Sunspot','HDS','ESiR','TAMEREENHD','MouL1','H2.','BigF','DON.','LOST','UNiK','FMS','BestHD','CryHD','wazatt','STI.','PURE','HDicTs','iDHD','KLine','HiDeF','CtrlHD','RedLeadR','MULTiGRPS','NERDHD','Okipic','CHD','GKS','T3k','Flx','LiberTeam','FLAWL3SS','TMB','V.Eyes','TLEMA','SS','KASH','THUGLiNE','MACHD','SSL','4kHD','HayesCarter','HDMaNiAcS','Osmos','STEAL','ROUGH','HDX','HDD','FwD','Rhéia','SANSDouTE','MOMENTUM','SHORTBREHD','CTU','FAUD','Ganesh','LaGoA','HDTFTD','FREHD','Heman','MAGiCAL','ENjOi','iNFAMOUS','HOLiDAYS','GALAC','EliteT','ULSHD','MANGACiTY','EXTREME','ZEST','SLiMHD','JMT','EPZ','BAWLS','FQM','AFG','SiNX','TERRA','NANO','TASTETV','LOGIES','PIX','mSD','tNe','AiRLiNE','RELOADED','Sookie','PROTEiGON','KULTURA','TiMiDe','STuFF','Tekmatek','JRabbit','St4f','ARTEFAC','DUFF','F4ST','ABiTBOL','ATeR','MUxHD','FJF','CARPEDIEM','MiKKELSEN','JASS','RiV3R','FiDELiO','LNA3D,','DIMENSION','NeMo','SEiGHT','KAMUi','KINeMA','CHDBits','FFG','HDILLUZION','HDEAL','CMBHD','HyDe','HDaY','SBSLNA3D','HDCLUB','KievUa','PublicHD','HDWinG','HDChina','LNA3D','JKF3D','BLUEBIRD','TYMOXA','SirYo','FQT']
no_upper=['mkv','x264','h264','m2t','ts','iND','wazatt','xXx']
listz_uploader = ['UpByArG','kn0ppixs','wWw.Mega.Exclue.Com','Extreme.Down.Com']


class wrez:

  def __init__(self,pathz,name):
		self.path=pathz
		self.init_str=name
		self.hash_sha512=""
		self.src_rip=""
		self.quality=""
		self.codec=""
		self.language=""
		self.l_audio=[]
		self.audio=""
		self.encoder=""
		self.l_version=[]
		self.version=""
		self.extension=""
		self.release_year=""
		self.title=""
		self.size=int(0)
		self.hasChanged=False
		
		
		
		self.sha512()
		#tmp = Thread(None, sha512(), None, (), {})
		#tmp.daemon=True
		#tmp.start()
		
		
		self.get_size()
		self.search_title()
		self.printz()
		
		
	def search_ext(self,strz):
		for ext in file_type:
			if strz.endswith(ext):
				self.extension=ext
				return strz.replace(ext,"")
		return strz
	
	def search_encoder(self,strz):
		for team in teamz:
			if team in strz:
				self.encoder=team
				return strz.replace(team,"")
		return strz
	
	def search_quality(self,strz):
		for q in l_quality:
			if q in strz:
				self.quality=q
				return strz.replace(q,"")
		return strz
		
	def search_codec(self,strz):
		for cod in flux:
			if cod in strz:
				self.codec=cod
				return strz.replace(cod,"")
		return strz
		
	def search_lang(self,strz):
		for lang in languages:
			if lang in strz:
				self.language+='.'+lang
				strz =strz.replace(lang,"")
		return strz
		
	def search_version(self,strz):
		for ver in versions:
			if ver in strz:
				self.l_version.append(ver)
				strz = strz.replace(ver,"")
				
		return strz
		
	def search_source(self,strz):
		for src in sources_rip:
			if src in strz:
				self.src_rip=src
				return strz.replace(src,"")
		return strz
		
	def search_audio(self,strz):
		for aud in audios:
			if aud in strz:
				self.l_audio.append(aud)
				strz= strz.replace(aud,"")
		return strz
		
	def search_year(self,strz):
		
		yr_pattern = compile("(19[56789]\d|20[01]\d)")
		yr = yr_pattern.search(strz)		
		if yr is None:
			return strz	#not find
		else:
			yr= yr.group(1)
			self.release_year=yr
			return strz.replace(yr,"")
	
	
	def reorder(self):
		self.version = ".".join(tuple(self.l_version))
		self.audio = ".".join(tuple(self.l_audio))
		str=".".join((self.title+self.release_year , self.version , self.language, self.quality , self.src_rip ,self.audio , self.codec, self.encoder, self.extension))
		
		return str.replace('..','.')
			
	def printz(self):
		self.version = ".".join(tuple(self.l_version))
		self.audio = ".".join(tuple(self.l_audio))
		print "Path =",self.path
		print "Initial str =",self.init_str
		print "Title =",self.title
		print "Release year =",self.release_year
		print "Version =",self.version
		print "Language(s) =",self.language
		print "Source RiP =",self.src_rip
		print "Quality Format =",self.quality
		print "Audio codec=",self.audio
		print "Video codec =",self.codec			
		print "Encoder TEAM =",self.encoder		
		print "Extension file=",self.extension
		print "Hash sha512 =",str(self.hash_sha512)
		print "Size =", self.size/float(2**20) ,"in MiB" 
		print "Re-ordered Name =",self.reorder()
			
			
	def search_title(self):
		new_name = self.removez_all(self.init_str)
		result = self.search_ext(new_name)
		result =  self.search_encoder(result)
		result =  self.search_quality(result)
		result =  self.search_codec(result)
		result =  self.search_lang(result)
		result =  self.search_version(result)
		result =  self.search_source(result)
		result =  self.search_audio(result)
		result =  self.search_year(result)
		result = string.replace(result,'..', '.')
		self.title = string.replace(result,'..', '.')
		
	
	def upper_first_char(self,strz):
		if (len(strz) < 2) or no_upper:
			return strz
		else:
			return strz[0].upper()+strz[1:]

	def refactor_line(self,strz):
		listz=strz.split(".")
		tmp=[]
		for element in listz:
			tmp.append(self.upper_first_char(element))
		return ".".join( tmp)
		
	def remove_uploader(self,strz):	
		
		for elem in listz_uploader:
			if elem in strz:
				strz = strz.replace(elem,'')
		new_name = string.replace(strz,'..', '.')
		return new_name
		
		
	def removez_all(self,name):
		new_name = string.replace(name,' ', '.')
		new_name = self.remove_uploader(new_name)
		new_name = string.replace(new_name,'..', '.')
		#new_name = string.replace(new_name,'JKF.3D', 'JFK3D')
		#new_name = string.replace(name,'&.', '.') BUG
		
		new_name = string.replace(new_name,'-', '.')
		new_name = string.replace(new_name,'_', '.')		
		new_name = string.replace(new_name,'(', '')
		new_name = string.replace(new_name,')', '')
		new_name = string.replace(new_name,'..', '.')
					
		new_name = string.replace(new_name,'X264', 'x264')
		new_name = string.replace(new_name,'XVID', 'XviD')
		new_name = string.replace(new_name,'TRUEHD', 'TrueHD')
					
		new_name = string.replace(new_name,'multi', 'MULTi')
		new_name = string.replace(new_name,'Multi', 'MULTi')
		new_name = string.replace(new_name,'MULTI', 'MULTi')
		new_name = string.replace(new_name,'MULTiF', 'MULTi')
		new_name = string.replace(new_name,'VO.VF','MULTi')
		new_name = string.replace(new_name,'VF.VOSTFR','MULTi')
		new_name = string.replace(new_name,'VF.VO+ST','MULTi')
		
		
		new_name = string.replace(new_name,'TRUE.HD', 'TRUEHD')
		new_name = string.replace(new_name,'blueray', 'BluRay')
		new_name = string.replace(new_name,'bluray', 'BluRay')
		new_name = string.replace(new_name,'Bluray', 'BluRay')
		new_name = string.replace(new_name,'BluraY', 'BluRay')
		new_name = string.replace(new_name,'Blu-Ray', 'BluRay')
		new_name = string.replace(new_name,'Blu.Ray', 'BluRay')
		new_name = string.replace(new_name,'Blu.ray', 'BluRay')
		new_name = string.replace(new_name,'(Bluray-rip)', 'BluRay')
		new_name = string.replace(new_name,'Blu-Ray Rip', 'BluRay')
		new_name = string.replace(new_name,'BDRip', 'BluRay')
		new_name = string.replace(new_name,'BDRIP', 'BluRay')
		new_name = string.replace(new_name,'BDRiP', 'BluRay')
		new_name = string.replace(new_name,'BRDRiP', 'BluRay')
		new_name = string.replace(new_name,'BRDRip', 'BluRay')
		new_name = string.replace(new_name,'BD', 'BluRay')
		new_name = string.replace(new_name,'HD-DVDRiP', 'HDRiP')
		new_name = string.replace(new_name,'HD.DVDRiP', 'HDRiP')
		new_name = string.replace(new_name,'HDVD', 'HDRiP')
		new_name = string.replace(new_name,'HDDVD', 'HDRiP')				
		new_name = string.replace(new_name,'DVDrip','DVDRiP')
		new_name = string.replace(new_name,'DVDriP','DVDRiP')
		new_name = string.replace(new_name,'dvdrip','DVDRiP')
		#new_name = string.replace(new_name,'DVD5','DVDRiP')
		new_name = string.replace(new_name,'.DVD.','DVDRiP')
		
		
		new_name = string.replace(new_name,'.DD.5.1','DD5.1')
		new_name = string.replace(new_name,'6.Canaux','5.1')	
		new_name = string.replace(new_name,'dts', 'DTS')
		new_name = string.replace(new_name,'Dts', 'DTS')
		new_name = string.replace(new_name,'DtS', 'DTS')
		new_name = string.replace(new_name,'DTS.DTS','DTS')
		new_name = string.replace(new_name,'DTSHD.','DTS.')
		new_name = string.replace(new_name,'.HD.','.')
		
		new_name = string.replace(new_name,'hdma', 'HDMA')
		new_name = string.replace(new_name,'HD MA', 'HDMA')
		new_name = string.replace(new_name,'HD.MA', 'HDMA')
		new_name = string.replace(new_name,'.MA.', '.HDMA.')
		new_name = string.replace(new_name,'ac3','AC3')
		new_name = string.replace(new_name,'Ac3','AC3')
		new_name = string.replace(new_name,'AC.3.','AC3.')
		new_name = string.replace(new_name,'HD.HRA','')
			
		#new_name = string.replace(new_name,'.HRA.', '.') #wtf
		new_name = string.replace(new_name,'.fr.', '.FRENCH.')
		new_name = string.replace(new_name,'.Fr.', '.FRENCH.')
		new_name = string.replace(new_name,'.FR.', '.FRENCH.')
		new_name = string.replace(new_name,'french', 'FRENCH')
		new_name = string.replace(new_name,'French', 'FRENCH')
		new_name = string.replace(new_name,'VF.', 'FRENCH.')
		new_name = string.replace(new_name,'VFF', 'TRUEFRENCH')		
		new_name = string.replace(new_name,'truefrench', 'TRUEFRENCH')
		new_name = string.replace(new_name,'Truefrench', 'TRUEFRENCH')
		new_name = string.replace(new_name,'TrueFrench', 'TRUEFRENCH')
		new_name = string.replace(new_name,'TrueFRENCH', 'TRUEFRENCH')
		
		new_name = string.replace(new_name,'VF', 'FRENCH')
		new_name = string.replace(new_name,'.PAL.', '.')
		new_name = string.replace(new_name,'HD1080', '1080p')
		new_name = string.replace(new_name,'1080P', '1080p')
		new_name = string.replace(new_name,'720P', '720p')
		
		new_name = string.replace(new_name,'VERSION.LONGUE','EXTENDED')
		new_name = string.replace(new_name,'Version.Longue','EXTENDED')
		new_name = string.replace(new_name,'Extended.Cut', 'EXTENDED')
		new_name = string.replace(new_name,'Extended.Edition', 'EXTENDED')
		new_name = string.replace(new_name,'Director\'s.Cut', 'DIRECTOR.CUT')
		new_name = string.replace(new_name,'Directors.Cut', 'DIRECTOR.CUT')
		new_name = string.replace(new_name,'DC', 'DIRECTOR.CUT')
		new_name = string.replace(new_name,'D/C', 'DIRECTOR.CUT')		
		new_name = string.replace(new_name,'Remastered','REMASTERED')
		new_name = string.replace(new_name,'Theatrical.Cut','THEATRICAL.CUT')
		new_name = string.replace(new_name,'Theatricul.Cut','THEATRICAL.CUT')
		new_name = string.replace(new_name,'Sunshine.Edition','SUNSHINE.EDITION')
		new_name = string.replace(new_name,'Revisited.The.Final.Cut','REVISITED.FiNAL.CUT')		
		new_name = string.replace(new_name,'LIMITED','LiMiTED')
		
		new_name = string.replace(new_name,'iNT','iNTERNAL')
		new_name = string.replace(new_name,'GAIA', 'GAÏA')
		new_name = string.replace(new_name,'Gaïa', 'GAÏA')
		new_name = string.replace(new_name,'GAÃA', 'GAÏA')
		new_name = string.replace(new_name,'GAÏA', 'GAÏA')
		new_name = string.replace(new_name,'GAiA', 'GAÏA')
		
		new_name = string.replace(new_name,'dxva', 'MULTi') #<--- WTF
		new_name = string.replace(new_name,'rip','')
		new_name = string.replace(new_name,'Rip','')
		new_name = string.replace(new_name,'Ripp','')
		new_name = string.replace(new_name,'.mkv.mkv', '.mkv')
		#new_name = string.replace(new_name,'..', '.')	#USELESS
		return self.refactor_line(new_name)
		
	def reformat(self):
		old_path =os.path.join(self.path, self.init_str)
		new_path=os.path.join(self.path, self.reorder())
		os.rename(old_path,new_path)

	def get_size(self):
		path =os.path.join(self.path, self.init_str)
		try:
			self.size = os.path.getsize(path)
		except :
			pass
			self.size =0

			
	def sha512(self):
		path =os.path.join(self.path, self.init_str)
		try:
			h = sha512()
			fd = open(path,'rb')
			for line in fd:
				h.update(line)
			fd.close()
			self.hash_sha512 = str(h.hexdigest())
		except IOError as e:
			print e

		
	def wrez2xml(self,newdoc,newroot):
		"""
			TODO save
			self.l_audio=[]
			self.l_version=[]
		"""
		wrez = newdoc.createElement('wrez')
		wrez.setAttribute('hasChanged', str(self.hasChanged))
		newroot.appendChild(wrez)

		path = newdoc.createElement('path')
		path.setAttribute('value', self.path)
		wrez.appendChild(path)
	
		path = newdoc.createElement('init_str')
		path.setAttribute('value', self.init_str)
		wrez.appendChild(path)

		path = newdoc.createElement('hash_sha512')
		path.setAttribute('value', self.hash_sha512)
		wrez.appendChild(path)
	
		path = newdoc.createElement('src_rip')
		path.setAttribute('value', self.src_rip)
		wrez.appendChild(path)

		path = newdoc.createElement('quality')
		path.setAttribute('value', self.quality)
		wrez.appendChild(path)

		path = newdoc.createElement('codec')
		path.setAttribute('value', self.codec)
		wrez.appendChild(path)
	
		path = newdoc.createElement('language')
		path.setAttribute('value', self.language)
		wrez.appendChild(path)
	
		path = newdoc.createElement('audio')
		path.setAttribute('value', self.audio)
		wrez.appendChild(path)

		path = newdoc.createElement('encoder')
		path.setAttribute('value', self.encoder)
		wrez.appendChild(path)

		path = newdoc.createElement('version')
		path.setAttribute('value', self.version)
		wrez.appendChild(path)
	
		path = newdoc.createElement('extension')
		path.setAttribute('value', self.extension)
		wrez.appendChild(path)

		path = newdoc.createElement('release_year')
		path.setAttribute('value', self.release_year)
		wrez.appendChild(path)
	
		path = newdoc.createElement('title')
		path.setAttribute('value', self.title)
		wrez.appendChild(path)

		path = newdoc.createElement('size')
		path.setAttribute('value', str(self.size))
		wrez.appendChild(path)
		return wrez


def listz2xml(listz):

	newdoc = minidom.Document()
	newroot = newdoc.createElement('listz')

	rootattr = newdoc.createAttribute('time')
	rootattr.nodeValue = '1958'
	newroot.setAttributeNode(rootattr)
	
	for element in listz:
		wrez = element.wrez2xml(newdoc,newroot)
		newroot.appendChild(wrez)

	newdoc.appendChild(newroot)
	strz= newdoc.toprettyxml()
	xml_create(strz)



def list_folder(top):
	
	listz=[] #wrez object list
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			
			if name.endswith(tuple(file_type)):
				path= os.path.join(root, name)
				print ""				
				filz = wrez(root,name)
				print "Before\t:",name
				print "After\t:",filz.reorder()
				char = raw_input("Modify file?\ntype [y/n]\n")
				
				
				if char=='y':
					print "rename file"
					new_path= os.path.join(root, filz.reorder())
					os.rename(path,new_path)
					filz.hasChanged=True
					#listz.append(filz) #save only modified name
					
				listz.append(filz) #save all files movie extension
				
	return listz


def check_redondancy(listz):
	
	for elem in teamz:
		if teamz.count(elem)>1:
			print "element",elem,"is present",teamz.count(elem),"times"



def xml_create(xml_as_str):
	path=str(os.getcwd())+"/backup.xml"
	fd =open(path,'w')
	fd.write(xml_as_str)
	fd.close()
	
	

def test():
	check_redondancy(teamz)
	check_redondancy(versions)
	name="The.Dark.Knight.x264.1080p.DTS.DD.5.1.MULTiF.BluRay.GAÏA.mkv"
	wrez("",name)
	name="XIII.La.Conspiration.Part2.FiNAL.FRENCH.720p.BluRay.x264.JMT.mkv"
	wrez("",name)
	name="The.Matrix.1999.1080p.BluRay.AC3.DTS.x264.GAIA.mkv"
	wrez("",name)
	name="You.Dont.Mess.With.The.Zohan.2008.TRUEFRENCH.720p.BluRay.x264.AiRLiNE.mkv"
	wrez("",name)
	name="Benjamin.Gates.et.le.trésor.des.Templiers.x264.1080p.DTS.DD5.1.MULTi.BluRay.GAÏA.mkv"
	wrez("",name)

def recover_old_filename(listz):
	
	for wrez in listz:
		#wrez.printz() debug
		old_path = os.path.join(wrez.path, wrez.reorder())
		print "Present \t:",old_path
		new_path = os.path.join(wrez.path, wrez.init_str)
		print "replace by\t:",new_path
		char = raw_input("recover file?\ntype [y/n]\n")
		if char=='y':
			print "rename file"
			os.rename(old_path,new_path)

def extract_list_from_xml(path):
	
	doc = minidom.parse(path)
	root = doc.documentElement
	current = root.firstChild
	while current:
			#print current
			
			if current.nodeName == 'wrez':
			
				attrs = current.attributes
				
				print attrs.items()[0]
				hasChanged=attrs.items()[0][1]	
				for elem in current.getElementsByTagName('path'):
					print elem.attributes.items()[0][1]
					path=elem.attributes.items()[0][1]
				
				for elem in current.getElementsByTagName('init_str'):
					print elem.attributes.items()[0][1]
					init_str=elem.attributes.items()[0][1]

				for elem in current.getElementsByTagName('hash_sha512'):
					print elem.attributes.items()[0][1]
					hash_sha512=elem.attributes.items()[0][1]
	
				for elem in current.getElementsByTagName('src_rip'):
					print elem.attributes.items()[0][1]
					src_rip=elem.attributes.items()[0][1]

				for elem in current.getElementsByTagName('quality'):
					print elem.attributes.items()[0][1]
					quality=elem.attributes.items()[0][1]
					
				for elem in current.getElementsByTagName('codec'):
					print elem.attributes.items()[0][1]
					codec=elem.attributes.items()[0][1]
	
				for elem in current.getElementsByTagName('language'):
					print elem.attributes.items()[0][1]
					language=elem.attributes.items()[0][1]
	
				for elem in current.getElementsByTagName('audio'):
					print elem.attributes.items()[0][1]
					audio=elem.attributes.items()[0][1]

				for elem in current.getElementsByTagName('encoder'):
					print elem.attributes.items()[0][1]
					encoder=elem.attributes.items()[0][1]

				for elem in current.getElementsByTagName('version'):
					print elem.attributes.items()[0][1]
					version=elem.attributes.items()[0][1]
			
				for elem in current.getElementsByTagName('extension'):
					print elem.attributes.items()[0][1]
					extension=elem.attributes.items()[0][1]

				for elem in current.getElementsByTagName('release_year'):
					print elem.attributes.items()[0][1]
					release_year=elem.attributes.items()[0][1]
			
				for elem in current.getElementsByTagName('title'):
					print elem.attributes.items()[0][1]
					title=elem.attributes.items()[0][1]

				for elem in current.getElementsByTagName('size'):
					print elem.attributes.items()[0][1]
					size=elem.attributes.items()[0][1]
				
			
			
			#print current.firstChild #same
			current = current.nextSibling
	


def recover_from_xml(path):
	
	listz = extract_list_from_xml(path)
	recover_old_filename(listz)
	
if __name__ == '__main__':
	
	arg_parse = ArgumentParser()
	arg_parse.add_argument('folder', metavar='folder'  , type=str, help='folder containning movies')
	arg = arg_parse.parse_args()
	#test()
	#listz = list_folder(arg.folder)
	#listz2xml(listz)
	#recover_old_filename(listz)
	extract_list_from_xml(str(os.getcwd())+"/backup.xml")

	
