#!/usr/bin/env python
#--*--coding:UTF-8 --*--
#todo thread hash fonction
#	xml date folder
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
l_quality=['4K.','1080p','1080i','720p','576p','576i','480p','480i','TrueHD']
flux=['AVC','x264','h264','MPEG2','XviD','MPEG4','DVXA']
languages=['MULTi','TRUEFRENCH','FRENCH','USA','VOSTFR','.VO.']
audios=['AAC20','DTS.HDMA','DTS','HRA','DD5.1','AC3','5.1']
versions=['LiMiTED','FESTiVAL','STV','UNCUT','UNRATED','RATED','BONUS','SUBFORCED','PROPER','FASTSUB','SUNSHINE.EDITION','REVISITED.FiNAL.CUT','DIRECTOR.CUT','THEATRICAL.CUT','REAL','EXTENDED','REMASTERED','REPACK','REMUX','CUSTOM','COMPLETE','FiNAL','PREAiR','RERIP','RETAIL','DOC']
file_type=['mp4','mkv','m2t','m2ts','ts']
teamz=['iND','iNT','iNTERNAL','ForceBleue','NOWiNHD','FrIeNdS','GAÏA','FHD','RLD','WiKi','.SS.','EbP','HidT','RuDe','HDxT','HDBRiSe','AMIABLE','DREAM','THENiGHTMAREiNHD','FYR','Slug','Ratat','HDZ','BiT','CiNEFOX','DiGiTAL','SoSo','ULSHDULSHD','HDFRENCH','PtS','Sunspot','HDS','ESiR','TAMEREENHD','MouL1','H2.','BigF','DON.','LOST','UNiK','FMS','BestHD','CryHD','wazatt','STI.','PURE','HDicTs','iDHD','KLine','HiDeF','CtrlHD','RedLeadR','MULTiGRPS','NERDHD','Okipic','CHD','GKS','T3k','Flx','LiberTeam','FLAWL3SS','TMB','V.Eyes','TLEMA','SS','KASH','THUGLiNE','MACHD','SSL','4kHD','HayesCarter','HDMaNiAcS','Osmos','STEAL','ROUGH','HDX','HDD','FwD','Rhéia','SANSDouTE','MOMENTUM','SHORTBREHD','CTU','FAUD','Ganesh','LaGoA','HDTFTD','FREHD','Heman','MAGiCAL','ENjOi','iNFAMOUS','HOLiDAYS','GALAC','EliteT','ULSHD','MANGACiTY','EXTREME','ZEST','SLiMHD','JMT','EPZ','BAWLS','FQM','AFG','SiNX','TERRA','NANO','TASTETV','LOGIES','PIX','mSD','tNe','AiRLiNE','RELOADED','Sookie','PROTEiGON','KULTURA','TiMiDe','STuFF','Tekmatek','JRabbit','St4f','ARTEFAC','DUFF','F4ST','ABiTBOL','ATeR','MUxHD','FJF','CARPEDIEM','MiKKELSEN','JASS','RiV3R','FiDELiO','LNA3D,','DIMENSION','NeMo','SEiGHT','KAMUi','KINeMA','CHDBits','FFG','HDILLUZION','HDEAL','CMBHD','HyDe','HDaY','SBSLNA3D','HDCLUB','KievUa','PublicHD','HDWinG','HDChina','LNA3D','JKF3D','BLUEBIRD','TYMOXA','SirYo','FQT','SYNERGY','CiNEFiLE','SALEM']
no_upper=['mkv','x264','h264','m2t','ts','iND','wazatt','xXx']
listz_uploader = ['UpByArG','kn0ppixs','wWw.Mega.Exclue.Com','Extreme.Down.Com']

CSI = "\033[31m"





class wrez:

	def __init__(self,pathz,name , dic=None):
		"""
			wrez constructor
		"""
		if dic is None:
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
			self.get_size()
			self.search_title()
			self.printz()
		else:
			try:
				self.path = dic["path"]
				self.init_str = dic["init_str"]
				self.hash_sha512 = dic["hash"]
				self.src_rip = dic["src_rip"]
				self.quality = dic["quality"]
				self.codec = dic["codec"]
				self.language = dic["language"]
				self.l_audio = dic["l_audio"]
				self.audio = dic["audio"]
				self.encoder = dic["encoder"]
				self.l_version = dic["l_version"]
				self.version = dic["version"]
				self.extension = dic["extension"]
				self.release_year = dic["release_year"]
				self.title = dic["title"]
				self.size = dic["size"]
				self.hasChanged= dic["hasChanged"]
				self.printz()
			except Exception as e:
				print e
	
		
		
	def search_ext(self,strz):
		"""
			search the extension of a filename string
		"""
		for ext in file_type:	#file_type = list of allow extension words
			if strz.endswith(ext):
				self.extension=ext
				return strz.replace(ext,"")
		return strz

	
	def search_encoder(self,strz):
		"""
			search the encoder's team in the string
		"""
		for team in teamz:	#teamz = list of allow teamz words
			if team in strz:
				self.encoder=team.replace(".","")
				return strz.replace(team,"")
		return strz

	
	def search_quality(self,strz):
		"""
			search the quality in the string
		"""
		for q in l_quality: #l_quality = list of allow quality words
			if q in strz:
				self.quality=q.replace(".","")
				return strz.replace(q,"")
		return strz

		
	def search_codec(self,strz):
		"""
			search the codec in the string
		"""
		for cod in flux: #flux = list of allow codec words
			if cod in strz:
				self.codec=cod.replace(".","")
				return strz.replace(cod,"")
		return strz
		
		
	def search_lang(self,strz):
		"""
			search the language of a movie in the string
		"""
		for lang in languages: #languages = list of allow lang words
			if lang in strz:
				if len(self.language)>0:
					self.language+='.'+lang.replace(".","")
				else:
					self.language+=lang.replace(".","")
				strz =strz.replace(lang,"")
		return strz

		
	def search_version(self,strz):
		"""
			search the version of a movie in a string
			example: directory's cut,...
		"""
		for ver in versions: #version= list of allow version words
			if ver in strz:
				self.l_version.append( ver.replace(".","") )
				strz = strz.replace(ver,"")
				
		return strz

		
	def search_source(self,strz):
		"""
			search source ri in the string
		"""
		for src in sources_rip: #sources_rip = list of allow source words
			if src in strz:
				self.src_rip=src.replace(".","")
				return strz.replace(src,"")
		return strz

		
	def search_audio(self,strz):
		"""
			collect all information about audio in a string
		"""
		for aud in audios: #audios = list of allow audio words
			if aud in strz:
				self.l_audio.append(aud)
				strz= strz.replace(aud,"")
		return strz


	def search_season_episode(self,strz):
		"""
			find the season and episode number on the string
		"""	
		pattern = compile("(S(\d\d)E(\d\d))") #S01E03
		sep = pattern.search(strz)		
		if sep is not None:
			se= sep.group(1)
			season = sep.group(2)
			episode = sep.group(3)
			return strz.replace(se,"")
			
		pattern = compile("((\d\d)x(\d\d))") #01x03
		sep = pattern.search(strz)		
		if sep is not None:
			se= sep.group(1)
			season = sep.group(2)
			episode = sep.group(3)
			return strz.replace(se,"")
			
		pattern = compile("(Ep(\d\d))") #Ep03
		sep = pattern.search(strz)		
		if sep is not None:
			se= sep.group(1)
			episode = sep.group(2)
			return strz.replace(se,"")
		
	def search_year(self,strz):
		"""
			find the year on the string from 1950 to 2019
		"""	
		yr_pattern = compile("(19[56789]\d|20[01]\d)")
		yr = yr_pattern.search(strz)		
		if yr is None:
			return strz	#not find
		else:
			yr= yr.group(1)
			self.release_year=yr
			return strz.replace(yr,"")
	
	
	def reorder(self):
		"""
			reorder filename from all informations collected
		"""
		self.version = ".".join(tuple(self.l_version))		
		self.audio = ".".join(tuple(self.l_audio))
		tuplz = (self.release_year , self.version , self.language, self.quality , self.src_rip ,self.audio , self.codec + '-' + self.encoder, self.extension)
		strz = self.title 
		for elem in tuplz:
			if elem != "":
				strz+="."+elem
		#strz=".".join((self.title ,self.release_year , self.version , self.language, self.quality , self.src_rip ,self.audio , self.codec + '-' + self.encoder, self.extension))
		return strz
			
	def printz(self):
		"""
			print variables function
		"""
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
		strz = self.reorder()
		print "Re-ordered Name =", strz


	def remove_lasts_dots(self, strz):
		while strz[-1]	== '.':
			strz=strz[:-1]
		return strz
		
			
	def search_title(self):
		"""
			remove all parts of a string to find the lat part (the title)
		"""
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
		result = result.replace('...', '.')
		result = result.replace('..', '.')
		self.title = self.remove_lasts_dots(result)
		
	
	def upper_first_char(self,strz):
		"""
			Upper case the first char of a word longer than 2
		"""
		if (len(strz) < 2) or no_upper: #no_upper list of element to no upper 
			return strz
		else:
			return strz[0].upper()+strz[1:]


	def refactor_line(self,strz):
		"""
			Upper case the first character if of each word in the string
		"""
		listz=strz.split(".")
		tmp=[]
		for element in listz:
			tmp.append(self.upper_first_char(element))
		return ".".join( tmp)

		
	def remove_uploader(self,strz):
		"""
			remove uploader or website tags in the filename
		"""
		for elem in listz_uploader:
			if elem in strz:
				strz = strz.replace(elem,'')
		new_name = string.replace(strz,'..', '.')
		return new_name
		
	def warez2dic(self):
		"""
			save the warez as a dictionnary representation (usefull for mongo)
		"""
		warez = {"path" : self.path,\
		"init_str" : self.init_str,\
		"hash_sha512" : self.hash_sha512,\
		"src_rip" : self.src_rip,\
		"quality" : self.quality,\
		"codec" : self.codec,\
		"lang" : self.language,\
		"l_audio" : self.l_audio,\
		"audio" : self.audio,\
		"encoder" : self.encoder,\
		"l_version" : self.l_version,\
		"version" : self.version,\
		"extension" : self.extension,\
		"release_year" : self.release_year,\
		"title" : self.title,\
		"size" : self.size,\
		"hasChanged" : self.hasChanged}
		return warez
		
		
		
	def removez_all(self,name):
		"""
			remove and reformat filename to warez rules
		"""
		new_name = string.replace(name,' ', '.')
		new_name = self.remove_uploader(new_name)
		new_name = string.replace(new_name,'..', '.')
		
		#new_name = string.replace(name,'\&.', '.') BUG
		
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
		new_name = string.replace(new_name,'BRRip', 'BluRay')
		new_name = string.replace(new_name,'BD', 'BluRay')
		new_name = string.replace(new_name,'HD-DVDRiP', 'HDRiP')
		new_name = string.replace(new_name,'HD.DVDRiP', 'HDRiP')
		new_name = string.replace(new_name,'HDVD', 'HDRiP')
		new_name = string.replace(new_name,'HDDVD', 'HDRiP')				
		new_name = string.replace(new_name,'DVDrip','DVDRiP')
		new_name = string.replace(new_name,'DVDriP','DVDRiP')
		new_name = string.replace(new_name,'dvdrip','DVDRiP')
		new_name = string.replace(new_name,'DVD5','DVDRiP')
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
		
		new_name = string.replace(new_name,'HD.HRA','HRA') #High resolution audio
		#new_name = string.replace(new_name,'.HRA.', '.')
		
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
		new_name = string.replace(new_name,'JKF.3D', 'JFK3D')
		new_name = string.replace(new_name,'GAIA', 'GAÏA')
		new_name = string.replace(new_name,'Gaïa', 'GAÏA')
		new_name = string.replace(new_name,'GAÃA', 'GAÏA')
		new_name = string.replace(new_name,'GAÏA', 'GAÏA')
		new_name = string.replace(new_name,'GAiA', 'GAÏA')
		
		new_name = string.replace(new_name,'dxva', 'DXVA') #<harwdare decode
		new_name = string.replace(new_name,'rip','')
		new_name = string.replace(new_name,'Rip','')
		new_name = string.replace(new_name,'Ripp','')
		new_name = string.replace(new_name,'.mkv.mkv', '.mkv')
		#new_name = string.replace(new_name,'..', '.')	#USELESS
		return self.refactor_line(new_name)
		
	def reformat(self):
		"""
			rename the filename with the reorder function
		"""
		old_path = os.path.join( self.path, self.init_str )
		new_path = os.path.join( self.path, self.reorder() )
		os.rename(old_path,new_path)

	def get_size(self):
		"""
			obtain the size of the file
		"""
		path =os.path.join(self.path, self.init_str)
		try:
			self.size = os.path.getsize(path)
		except :
			self.size = 0

			
	def sha512(self):
		"""
			compute sha-512 hash 
		"""
		path = os.path.join(self.path, self.init_str)
		try:
			h = sha512()
			fd = open(path,'rb')
			for line in fd:
				h.update(line)
			fd.close()
			self.hash_sha512 = str(h.hexdigest())
		except IOError as e:
			
			print CSI,"\tWarning",e

		
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


def xml_create(xml_as_str):
	"""
		arg:
			xml_as_str: string representing xml file
	
		function:
			write a xml file from a string
	"""
	try:
		path=str(os.getcwd())+"/backup.xml"
		fd =open(path,'w')
		fd.write(xml_as_str)
		fd.close()
	except Exception as e:
		print e


def listz2xml(listz):
	"""
		arg:
			listz=list of warez object

		function:
			create a xml file representing the list of warez objects
			
	"""
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



def list_folder(top,dont_ask=True):
	"""
		arg:
			top = top path directory
			dont_ask = don't ask the user to rename each file
		function:
			list files in a folder
			and for each file create a Warez object

		return:
			list of Warez objects
	"""
	listz=[] #wrez object list
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			
			if name.endswith(tuple(file_type)):
				path= os.path.join(root, name)
				print ""				
				filz = wrez(root,name)
				print "Before\t:",name
				print "After\t:",filz.reorder()
				if not dont_ask:
					char = raw_input("Modify file?\ntype [y/n]\n")
										
					if char=='y':
						print "rename file"
						new_path= os.path.join(root, filz.reorder())
						os.rename(path,new_path)
						filz.hasChanged=True
						#listz.append(filz) #save into the list only modified name
					
				listz.append(filz) #save all files movie extension into the list
				
	return listz




def check_redondancy(listz):
	"""
		arg:
			listz=list to check
		
		function:
			check if an element is present more than one time into the list
	"""
	for elem in teamz:
		if teamz.count(elem)>1:
			print "element",elem,"is present",teamz.count(elem),"times"	


def test():
	"""
		test some filename examples 
	"""
	check_redondancy(teamz)
	check_redondancy(versions)
	name="The.Dark.Knight.x264.1080p.DTS.DD.5.1.MULTi.BluRay.GAÏA.mkv"
	wrez("",name)
	name="XIII.La.Conspiration.Part2.FiNAL.FRENCH.720p.BluRay.x264.JMT.mkv"
	wrez("",name)
	name="The.Matrix.1999.1080p.BluRay.AC3.DTS.x264.GAIA.mkv"
	wrez("",name)
	name="You.Dont.Mess.With.The.Zohan.2008.TRUEFRENCH.720p.BluRay.x264.AiRLiNE.mkv"
	wrez("",name)
	name="Benjamin.Gates.et.le.trésor.des.Templiers.x264.1080p.DTS.DD5.1.MULTi.BluRay.GAÏA.mkv"
	wrez("",name)





def extract_list_from_xml(path):
	"""
		arg:
			path = xml file path

		function:
			extract a list of warez objects from a xml file

		return:
			list of warez objects
	"""
	listz=[]
	doc = minidom.parse(path)
	root = doc.documentElement
	current = root.firstChild
	while current:
			#print current
			
			if current.nodeName == 'wrez':
			
				attrs = current.attributes				
				#print attrs.items()[0]
				
				hasChanged=attrs.items()[0][1]
				#print hasChanged
				
				for elem in current.getElementsByTagName('path'):
					path=elem.attributes.items()[0][1]
					#print path
				
				for elem in current.getElementsByTagName('init_str'):
					init_str=elem.attributes.items()[0][1]
					#print init_str

				for elem in current.getElementsByTagName('hash_sha512'):
					hash_sha512=elem.attributes.items()[0][1]
					#print hash_sha512
	
				for elem in current.getElementsByTagName('src_rip'):
					src_rip=elem.attributes.items()[0][1]
					#print src_rip

				for elem in current.getElementsByTagName('quality'):
					quality=elem.attributes.items()[0][1]
					#print quality
					
				for elem in current.getElementsByTagName('codec'):
					codec=elem.attributes.items()[0][1]
					#print codec
	
				for elem in current.getElementsByTagName('language'):
					language=elem.attributes.items()[0][1]
					#print language
	
				for elem in current.getElementsByTagName('audio'):
					audio=elem.attributes.items()[0][1]
					#print audio

				for elem in current.getElementsByTagName('encoder'):
					encoder=elem.attributes.items()[0][1]
					#print encoder

				for elem in current.getElementsByTagName('version'):
					version=elem.attributes.items()[0][1]
					#print version
			
				for elem in current.getElementsByTagName('extension'):
					extension=elem.attributes.items()[0][1]
					#print extension

				for elem in current.getElementsByTagName('release_year'):
					release_year=elem.attributes.items()[0][1]
					#print release_year
			
				for elem in current.getElementsByTagName('title'):
					title=elem.attributes.items()[0][1]
					#print title

				for elem in current.getElementsByTagName('size'):					
					size=elem.attributes.items()[0][1]
					#print size

				dic = {}
				dic["path"] = path 
				dic["init_str"] = init_str
				dic["hash"] = hash_sha512
				dic["src_rip"] = src_rip
				dic["quality"] = quality
				dic["codec"] = codec
				dic["language"] = language
				dic["l_audio"] = l_audio
				dic["audio"] = audio
				dic["encoder"] = encoder
				dic["l_version"] = l_version
				dic["version"] = version
				dic["extension"] = extension
				dic["release_year"] = release_year
				dic["title"] = title
				dic["size"] = size
				dic["hasChanged"] = shasChanged
				warz = warez("","",dic) #create warez object
				
				listz.append(warz)			
			
			#print current.firstChild #same
			current = current.nextSibling
	return listz
			

def recover_old_filename(listz):
	"""
		arg:
			listz=warez object list
			
		function:
			ask the user if he wants to change the filename by the original value
	"""
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


def recover_from_xml(path):
	"""
		restore original filename from a xml file
	"""
	listz = extract_list_from_xml(path)
	recover_old_filename(listz)


def listz2diclist(listz):
	"""
		transform a warez list object to a list of dictionnary
	"""
	tmp=[]
	for elem in listz:
		dic = elem.warez2dic()
		tmp.append(dic)
	return tmp



def save_list_mongo(listz):
	"""
		save a list into mongo database
	"""	
	connection = pymongo.Connection('localhost', 27017)
	db = connection.database
	collection = db.warez_collection


	
if __name__ == '__main__':
	
	arg_parse = ArgumentParser()
	arg_parse.add_argument('folder', metavar='folder'  , type=str, help='folder containning movies')
	arg = arg_parse.parse_args()

	
	test() #test some example fonction

	
	#listz = list_folder(arg.folder)	#list files in a folder and for each create a warez object
	#listz2xml(listz)	#save list of warez object 
	#recover_old_filename(listz)	#change the filename by the original value for each warez object in list
	
	#listz = extract_list_from_xml( str( os.getcwd() ) + "/backup.xml" )	#recover a list of warez objects from a xml file

	
