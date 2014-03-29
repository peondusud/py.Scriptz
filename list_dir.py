import os
import re
import sys
import time
import shutil
import stat
import os



def list_folder(top):
        for root, dirs, files in os.walk(top, topdown=False):
                for name in files:                        
                        if name.endswith("tex"):
                                path= os.path.join(root, name)
                                print ""
                                print "path", path
                                print "root", root
                                print "filename", name



print os.getcwd()
list_folder(os.getcwd())
