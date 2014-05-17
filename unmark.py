#!/usr/bin/env python
#--*--coding:UTF-8 --*--

import sys
import os
import re
import subprocess
import argparse
import random
from tempfile import mkstemp
from shutil import move


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
	if isinstance(s, str):
		print "ordinary string"
	elif isinstance(s, unicode):
		print "unicode string"
	else:
		print "not a string"

def replaz(file_path, pattern, subst):
	try:
		fh, abs_path = mkstemp() 	#Create temp file
		new_file = open(abs_path,'wb')
		old_file = open(file_path,'rb')
		for line in old_file:
			new_file.write(line.replace(pattern, subst))
		new_file.close()	#close temp file
		os.close(fh)
		old_file.close()
		os.remove(file_path)	#Remove original file
		move(abs_path, file_path)
		return True
	except IOError :
		print "IO Error"
		return False

def the_watermark(text):
	#print type(text)
	#whatisthis(text)
	reg = re.compile('Ce document est la propri.+[0-2][0-9]:[0-5][0-9]')
	result = reg.findall(text)
	for m in result:
		print "Watermark is",m
		return m
		#text.replace(m,"by peon")

def clean_watermark(filz, tempFile):
	try:
		fd = open(tempFile, 'rb')
		pdf_uncompress = fd.read()
		fd.close()
		patt = the_watermark(pdf_uncompress)
		if patt is not None:
			replaz(tempFile, patt, "by peon.")
			return True
		else:
			print "no pattern find"
			return False
	except IOError :
		print "IO Error"
		return False

def uncompress_PDF(filz):
	tempFile = gen_TempfileName(os.path.abspath(filz))
	print "", tempFile
	p = subprocess.Popen(["pdftk", os.path.abspath(filz),"output", tempFile , "uncompress"], stdout=subprocess.PIPE)
	output, err = p.communicate()
	print "*** Running pdftk uncompress command ***\n", output
	#print err
	if err is None:
		#print "No error keep going"
		return tempFile
	else:
		print "Something goes wrong, during uncompression stage"
		return None

def compress_PDF(tempFile, filz):
	p = subprocess.Popen(["pdftk", os.path.abspath(tempFile),"output", filz , "compress"], stdout=subprocess.PIPE)
	output, err = p.communicate()
	print "*** Running pdftk uncompress command ***\n", output
	#print err
	if err is None:
		#print "No error keep going"
		return filz
	else:
		print "Something goes wrong, during compression stage"
		#remove
		return None

if __name__ == "__main__":
	arg_parse = argparse.ArgumentParser()
	arg_parse.add_argument('file', metavar='file'  , type=str, help='PDF file name')
	args = arg_parse.parse_args()
	
	filz = args.file
	if filz  is not None:
		#print "Filz is not None"
		if not os.path.isdir(filz):
			#print "Filz is not a directory"
			if filz.endswith(("PDF","pdf")):
				#os.remove(file_path)
				#print "Filz ends with PDF extension name"
				#print 'filz = ', filz
				print "try to uncompress PDF"
				tempFile = uncompress_PDF(filz)
				if tempFile is not None:
					print "PDF uncompressed\n"
					print "Try to remove mark\n"
					tmp = clean_watermark(filz, tempFile)
					if tmp:
						print "Watermark removed\n"
						zmp = compress_PDF(tempFile, filz+"z")
						if zmp is not None:
							print "PDF recompressed\n"
							os.remove(filz)
							os.remove(tempFile)
							print "temp files removed\n"
							move(filz+"z", filz)
					else:
						#os.remove(tempFile) #as you want
						print "No pattern found"
				else:
					print "Fail to uncompress PDF"
