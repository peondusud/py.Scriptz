import os
import re
import sys
import time
import shutil
import stat
path = os.path.join("F:\HD\deal-la.source.102.720p.nfo")
print path

os.chmod( path, stat.S_IWUSR)
os.remove(path)
