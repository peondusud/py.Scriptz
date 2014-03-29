#!/usr/bin/python       
# *-* coding: utf-8 *-*

import os
import sys
import psutil #to install
from ctypes import *
from ctypes.wintypes import *
import struct
import binascii
from PIL import Image, ImageTk
from math import sin,cos,pi,atan2
import random
import time

noTix_flag=0
try:
    import Tix
    root = Tix.Tcl()
    del(root)

except Exception as e:
    print e
    import Tkinter as Tix
    noTix_flag=1
    print "Warning : Next time install \"tix\" package"

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

'''
http://msdn.microsoft.com/en-us/library/windows/desktop/ms684880%28v=vs.85%29.aspx
'''
PROCESS_VM_OPERATION = 0x0008 	#Required to perform an operation on the address space of a process (see VirtualProtectEx and WriteProcessMemory).
PROCESS_VM_READ = 0x0010 		#Required to read memory in a process using ReadProcessMemory.


def rotz(x,y,rotation):
    _x = (x * cos(rotation)) + (y * sin(rotation))
    _y = (y * cos(rotation)) - (x * sin(rotation))
    return _x ,_y
    
    
def winds():    
    win = Tix.Tk()
    win.title('Rust map')
    
    img = Image.open("C:\\Users\\userz\Desktop\\steamworkshop_webupload_previewfile_203790453_preview.jpg")
    (w,h )= img.size
    ratio=1
    #frame = Tix.Frame(win, width=w/2, height=h/2, borderwidth=1)
    #frame.pack()
    #img = Image.open("C:\\Users\\Xnl\Desktop\\steamworkshop_webupload_previewfile_203790453_preview.jpg")
    photo = ImageTk.PhotoImage(img)
   
    
    #print photo.height(),photo.width()
    print "width ",w
    print "height ",h
    canevas = Tix.Canvas(win,width =w, height = h)
    canevas.create_image(0,0, anchor = Tix.NW, image=photo)
    canevas.config(height=photo.height(),width=photo.width())
    def onRightClic(event):
        X = event.x
        Y = event.y
        #print X,Y
        #X=40
        #Y=40
        r = 7
        angle=-pi/2*4/5
        rotate=[]
        arrow=[ (X+r, Y ), (X-r, Y-r), ( X-r/2, Y),  (X-r, Y+r)]
        for elem in arrow:
            x,y =  rotz(X-elem[0],Y-elem[1],angle)
            rotate.append(x+X)
            rotate.append(y+Y)
        #rotate=[X+r*cos(angle), Y-r*sin(angle) , X-r*sin(angle+3/4*pi), Y+r*sin(angle+3/4*pi),  X-0.5*r*cos(angle), Y+0.5*r*sin(angle),  X+r*sin(angle-3/4*pi), Y+r*sin(angle-3/4*pi)]
       
        arrow =map(int,rotate)
        
        canevas.create_polygon(arrow, outline='green', fill='green', width=1)
    canevas.bind('<Button-3>', onRightClic)
    canevas.pack()
    x_pos= Tix.StringVar()
    z_pos= Tix.StringVar()
    Tix.Label(win,textvariable=x_pos).pack(padx=10,pady=10)
    Tix.Label(win,textvariable=z_pos).pack(padx=10,pady=10)
    def loop_100ms():
        X = random.randint(0, 1000)
        Y = random.randint(0, 1000)
        angle=0
        r=10
        for angle in range(8):
            angle+=pi/8
            rotate=[X+r*cos(angle), Y-r*sin(angle) , X-r*sin(angle+3/4*pi), Y+r*sin(angle+3/4*pi),  X-0.5*r*cos(angle), Y+0.5*r*sin(angle),  X+r*sin(angle-3/4*pi), Y+r*sin(angle-3/4*pi)]
            canevas.create_polygon(rotate, outline='green', fill='green', width=1)
        win.after(100,loop_100ms)
    #loop_100ms()
    win.mainloop()
    
def get_pid(strz="rust.exe"):
    i=None
    print "try to find pid from process name :", strz
    process = filter(lambda p: p.name == strz, psutil.process_iter())
    for i in process:
        print "process name :",i.name," PID =",i.pid
    if i is not None:
        return i.pid #return last
    return i

def readBytes(h_process, address, bytes=4):
		
    buffer = create_string_buffer(bytes)
    bytesread = c_ulong(0)
    bufferSize = bytes
    ReadProcessMemory(h_process, address, buffer, bufferSize,byref(bytesread))
    string = buffer.raw
    return string

def readInt(h_process, address):
    """
    __usage__	int_value = m.readInt(0x000000)
    """	
    string = readBytes(h_process,address,4)
    number = struct.unpack('<i',string)[0]
    return number

def readLong(h_process, address):
    """		
    __usage__	long_value = m.readLong(0x000000)
    """
    string = readBytes(h_process,address,4)
    number = struct.unpack('<l',string)[0]
    return number

def readULong(h_process, address):
    """
    __usage__	ulong_value = m.readULong(0x000000)
    """
    string = readBytes(h_process,address,4)
    number = struct.unpack('<L',string)[0]
    return number

def readFloat(h_process, address):
    """
    __usage__	float_value = m.readFloat(0x000000)
    """
    string = readBytes(h_process,address,4)
    number = struct.unpack('<f',string)[0]
    return number
		
def readString(h_process, address, bytes=50):
    """
    __usage__	name = m.readString(0x000000)
    """
    buffer = readBytes(h_process, address, bytes)
    i = buffer.find('\x00')
    if i != -1:
        return buffer[:i]
    else:
        return buffer


def test():
    '''
        hProcess :   	 A handle to the process with memory that is being read. The handle must have PROCESS_VM_READ access to the process.
        lpBaseAddress :  A pointer to the base address in the specified process from which to read. Before any data transfer occurs, the system verifies that all data in the base address and memory of the specified size is accessible for read access, and if it is not accessible the function fails.
        lpBuffer :   	 A pointer to a buffer that receives the contents from the address space of the specified process.
        nSize :    		 The number of bytes to be read from the specified process.
        lpNumberOfBytesRead : A pointer to a variable that receives the number of bytes transferred into the specified buffer. If lpNumberOfBytesRead is NULL, the parameter is ignored.
    '''
    bytesRead = c_ulong(0)
    bufferSize= 64
    #buffer = c_char_p("The data goes here")
    buffer = create_string_buffer(bufferSize)
    print  bufferSize
    rPM = WinDLL('kernel32',use_last_error=True).ReadProcessMemory
    rPM.argtypes = [HANDLE,LPCVOID,LPVOID,c_size_t,POINTER(c_size_t)]
    rPM.restype = BOOL
    tmp = rPM(processHandle, addrz, buffer, bufferSize, byref(bytesRead))
    if tmp:
        print( type(buffer.value), dir(buffer.value))
        print("Success:", ord(str(buffer.value)))
    else:
        print("Failed to access process memory")
  
def my_upper(strz):
    strz = strz.replace('a','A')
    strz = strz.replace('b','B')
    strz = strz.replace('c','C')
    strz = strz.replace('d','D')
    strz = strz.replace('e','E')
    strz = strz.replace('f','F')
    return strz
    
if __name__ == "__main__":

    pid = get_pid("mumble.exe")
    #addrz = 0x6AF25E04 #value = 100
    addrz = 0x6AF266EC # val = 10.07
    if pid is None:
        print "no pid found, exit"
        sys.exit()
    else:
        print "Try to OpenProcess for pid", pid
        processHandle = OpenProcess(PROCESS_VM_READ, False, pid)
        if  not processHandle:
            print "Failed: Get Handle - Error code: ", windll.kernel32.GetLastError()
        else:
            print "Success: Got Handle for PID:", pid
            var =  readFloat(processHandle, addrz)
            print "@ddr ",my_upper(hex(addrz)),"=>  value  = ",var
            
            
            
            CloseHandle(processHandle)
            winds()
          
        
