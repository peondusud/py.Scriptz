import libtorrent as lt
import os

save_torrent_folder ="/home/peon/"

def create_torrent(path,filename=""):
    fs = lt.file_storage()
    if filename=="":
		listz = list_folder(top)
		for tuplez in listz:
			path=tuplez[0]
			filename=tuplez[1]
			fs.add_file(pathz , size)
    else:
        pathz = os.path.join(path,filename)
        print "pathz", pathz
        size = os.path.getsize(pathz)
        fs.add_file(filename, size)
        #fs.add_file(pathz , size)
    tor = lt.create_torrent(fs)
    lt.set_piece_hashes(tor,'.')
    tor.set_comment("COMEONES")
    tor.set_creator("PEONDUSUD")
    announce_url = "http://www.gks.gs/tracker"
    tor.add_tracker(announce_url)
    tor.set_priv(True)
    tor.add_url_seed("http://192.168.70.136:58888")
    print dir(tor)
    f = open(save_torrent_folder + filename + ".torrent", "wb")
    f.write(lt.bencode(tor.generate()))
    f.close()
    print "torrent raw :"
    print lt.bencode(tor.generate())


def list_folder(top):
	
	listz=[] 
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			#path= os.path.join(root, name)				
			filz = tuple(root,name)					
			listz.append(filz)		
	return listz


if __name__ == '__main__':

	filename="DNS.ova"
	#filename=""
	path="/home/peon"
	create_torrent(path,filename)
