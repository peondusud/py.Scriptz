#!/usr/bin/env python
#--*--coding:UTF-8 --*--


import os
import sys
import time
import string
import socket
from fabric.api import *
from fabric.state import env, output, commands, connections, env_options


"""
fabric need  ecdsa pycrypto paramiko
pycrypto on windows need visual compiler
see http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat
	http://stackoverflow.com/questions/3047542/building-lxml-for-python-2-7-on-windows/5122521#5122521
brief : 1st   install  Visual Studio C++ 2008 Express Edition (to fix error: Unable to find vcvarsall.bat)
		2nd   install  Windows SDK for Windows 7 and .NET Framework 3.5 SP1 (to remove: GMP or MPIR library not found)
		3rd   launch  "pip install ecdsa pycrypto paramiko fabric"
"""

def ssh_init(user,passw,hostname="localhost"):
	
	env.user = user		# Set ssh user to use
	env.password = passw
	#ip = str(socket.gethostbyname('media'))

	# both line works
	env.host_string= hostname #only for one target
	#env.hosts=["media"]	#for multi target

	env.shell = "/bin/bash -l -i -c" #to fix alias usage
	#run('shopt -s expand_aliases >> .profile')
	env.warn_only = True
	env.debug = False
	env.colors = True


def exec_remote_cmd(cmd):
	result = run(cmd)
	if result.succeeded:
		sys.stdout.write('$'+cmd+ '\t')
		sys.stdout.write(result+"\n")
	else:
		sys.stdout.write('\n* Command failed: '+cmd+'\n')
		sys.stdout.write(result+"\n")



def ssh_remote_exec (cmd):
	"""
	hide bad printing output
	print("[%s] Executing task '%s'" % (host, name))
	"""
	def do():
		exec_remote_cmd(cmd)
	
	with hide('output','running','warnings','status','debug','aborts'), settings(warn_only=True,quiet=True):
		execute(do)

if __name__ == "__main__":
	hostname="media"
	user="peon"
	passw="pass"
	ssh_init(user,passw,hostname)
	ssh_remote_exec ('media')
