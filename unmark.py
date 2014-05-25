#!/usr/bin/env python
#--*--coding:UTF-8 --*--

import sys
import os
import re
import subprocess
import argparse
import random
import logging
from tempfile import mkstemp
from shutil import move

SIG="by peon."

def gen_numbers():
	return "".join( [ chr(c) for c in range(ord("0"),ord("9")+1) ])
	

def gen_alpha():
	return "".join( [chr(c) for c in range(ord("a"),ord("z")+1)])

def gen_upper_alpha():
	return "".join( [chr(c) for c in range(ord("A"),ord("Z")+1)])

def alpha():
	return gen_numbers() + gen_alpha() + gen_upper_alpha()

def get_file_extension(file_path):
	fileExtension = os.path.splitext(file_path)[1]
	return fileExtension

def get_fileName(file_path):
	fileName = os.path.basename(file_path)
	return fileName

def get_parent_folder(file_path):
	dir = os.path.dirname(file_path)
	#dir = os.path.abspath(os.path.join(f_path, os.pardir))
	return os.path.basename(os.path.normpath(dir))

def gen_TempfileName(file_path):
	"""
		generate "/orig_dir/tmp_"+filename+"8random char from alpha"."extension"
	"""
	alphabet = alpha()
	strz = "".join( [random.choice(alphabet) for c in range(8)] )
	#strz = strz.replace(" ", "")
	strz='_'+strz
	fileName =  os.path.splitext(get_fileName(file_path))[0] #remove extension
	tempFile = os.path.join( os.path.dirname(file_path), "tmp_"+ fileName +strz + get_file_extension(file_path))
	return tempFile

def whatisthis(s):
	logger = logging.getLogger('MyLog')
	if isinstance(s, str):
		logger.info("ordinary string")
	elif isinstance(s, unicode):
		logger.info("unicode string")
	else:
		logger.info("not a string")

def replaz(file_path, pattern, subst):
	logger = logging.getLogger('MyLog')
	try:
		fh, abs_path = mkstemp() 	#Create temp file
		logger.debug("Create temp file")
		new_file = open(abs_path,'wb')
		old_file = open(file_path,'rb')
		for line in old_file:
			new_file.write(line.replace(pattern, subst))
		new_file.close()	#close temp file
		os.close(fh)
		old_file.close()
		os.remove(file_path)	#Remove original file
		logger.debug("Remove original file")
		move(abs_path, file_path)
		return True
	except IOError :
		logger.error("IO Error")
		return False

def the_watermark(text):
	logger = logging.getLogger('MyLog')
	logger.debug("type text",type(text))
	#whatisthis(text)
	reg = re.compile('Ce document est la propri.+[0-2][0-9]:[0-5][0-9]')
	result = reg.findall(text)
	for m in result:
		print "[INFO] Watermark is" , m
		return m

def clean_watermark(filz, tempFile):
	logger = logging.getLogger('MyLog')
	try:
		fd = open(tempFile, 'rb')
		pdf_uncompress = fd.read()
		fd.close()
		patt = the_watermark(pdf_uncompress)
		if patt is not None:
			#replaz(tempFile, patt, "by peon.")
			replaz(tempFile, patt, SIG)
			return True
		else:
			logger.info("No pattern find")
			return False
	except IOError :
		logger.error("IO Error")
		return False

def uncompress_PDF(filz):
	logger = logging.getLogger('MyLog')
	tempFile = gen_TempfileName(os.path.abspath(filz))
	logger.debug( "uncompress_PDF tempFile", tempFile)
	p = subprocess.Popen(["pdftk", os.path.abspath(filz),"output", tempFile , "uncompress"], stdout=subprocess.PIPE)
	output, err = p.communicate()
	#logger.info("*** Running pdftk uncompress command ***\n")
	print "[INFO]\tRunning pdftk uncompress command\n", output 
	if err is None:
		logger.debug("No error keep going")
		return tempFile
	else:
		print "uncompress_PDF err :", err
		logger.info("Something goes wrong, during uncompression stage")
		return None

def compress_PDF(tempFile, filz):
	logger = logging.getLogger('MyLog')
	p = subprocess.Popen(["pdftk", os.path.abspath(tempFile),"output", filz , "compress"], stdout=subprocess.PIPE)
	output, err = p.communicate()
	#logger.info("*** Running pdftk compress command ***\n")
	print "[INFO]\tRunning pdftk compress command\n", output
	if err is None:
		logger.debug("No error keep going")
		return filz
	else:
		print "compress_PDF err :", err
		logger.info("Something goes wrong, during compression stage")
		#remove
		return None

def unmark_process(filz):
	logger = logging.getLogger('MyLog')
	if filz.endswith(("PDF","pdf")):
		logger.debug("File ends with PDF extension name")
		logger.debug('filz = ', filz)
		logger.info("Try to uncompress PDF")
		tempFile = uncompress_PDF(filz)
		logger.debug('tempFile = ', tempFile)
		if tempFile is not None:
			logger.info("PDF uncompressed")
			logger.info("Try to remove watermark")
			tmp = clean_watermark(filz, tempFile)
			if tmp:
				logger.info("Watermark removed")
				zmp = compress_PDF(tempFile, filz+"z")
				if zmp is not None:
					logger.info("PDF recompressed\n")
					try:
						logger.debug("Try to remove filz", filz)
						os.remove(filz)
						logger.debug("Pass remove tempFile", filz)
					except (OSError, IOError, Error) as e:
						logger.error("Error removing filz", filz, e)
					try:
						logger.debug("Try to remove tempFile", tempFile)
						os.remove(tempFile)
						logger.debug("Pass remove tempFile", tempFile)
					except (OSError, IOError, Error) as e:
						logger.error("Error removing tempFile", tempFile, e)
					logger.info("Temp files removed\n")
					logger.debug("Try to move unmanrked PDF to original location")
					try:
						logger.debug("Try to remove tempFile", tempFile)
						move(filz+"z", filz)
						logger.info("PDF "+filz+" correctly unmarked")
					except (OSError, IOError, Error) as e:
						logger.error("Error moving "+filz+"z to", filz, e)
				else:
					logger.info("Something goes wrong, during compression stage")
			else:
				try:
					logger.debug("Try to remove tempFile", tempFile)
					os.remove(tempFile) #as you want
					logger.debug("Pass removed tempFile", tempFile)
					logger.info("Temp files removed")
					logger.info("No mark pattern found, maybe you need to custom RegEx or already removed")
				except (OSError, IOError, Error) as e:
					logger.error("Error removing tempFile", tempFile, e)
		else:
			logger.info("Fail to uncompress PDF")
	else:
		logger.info("file no ends with PDF extension")

if __name__ == "__main__":
	parser = argparse.ArgumentParser("A script for remove watermarked PDF file")
	parser.add_argument('file', metavar='file'  , type=str, help='PDF file name')
	#parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	parser.add_argument("-v", "--verbose", const = 1, default = 0,type = int, nargs="?", help="increase verbosity: 0 = info, 1 = only warnings, 2 = debug. No number means info. Default is no verbosity.")
	parser.add_argument("-v", "--nSignature",  type=str, default = SIG , help='PDF file name')
	args = parser.parse_args()
	SIG= args.nSignature
	
	logger = logging.getLogger('MyLog')
	formatter = logging.Formatter('[%(levelname)s] %(message)s')
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	#print args.verbose
	if args.verbose == 0:
		logger.setLevel(logging.INFO)
	elif args.verbose == 1:
		logger.setLevel(logging.WARNING) 
	elif args.verbose == 2:
		logger.setLevel(logging.DEBUG) 
	
	filz = os.path.abspath(args.file)
	if filz is not None:
		logger.debug("Filz params is not None")
		if os.path.isdir(filz):
			logger.debug("Filz is a directory")
			for root, dirs, files in os.walk(filz, topdown=False):
				for name in files:
					if name.endswith(("PDF","pdf")):
						path= os.path.join(root, name)
						print "\nFilename", name
						logger.debug("path", path)
						unmark_process(path)
			
		else:
			logger.debug("Filz is not a directory")
			if os.path.isfile(filz):
				logger.debug("Filz is a file")
				print "\nFilename", filz
				unmark_process(filz)
