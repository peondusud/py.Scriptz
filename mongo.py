import pymongo
import warez

def add_database(disk ,listz):
	mongodb_uri = 'mongodb://localhost:27017'
	db_name = 'warez_collection'

	try:
		#connection = pymongo.Connection(mongodb_uri)
		connection = pymongo.Connection('localhost', 27017)
		db = connection[db_name]
	except:
		print('Error: Unable to connect to database.')
		connection = None

	if connection is not None:
		for dic in listz:		
			db.disk1.insert(dic)


def find_hash(hashz): 
	mongodb_uri = 'mongodb://localhost:27017'
	db_name = 'warez_collection'

	try:
		#connection = pymongo.Connection(mongodb_uri)
		connection = pymongo.Connection('localhost', 27017)
		db = connection[db_name]
	except:
		print('Error: Unable to connect to database.')
		connection = None

	if connection is not None:
		db.disk1.find({hash_sha512:})
	


def warez2dic(self):
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
