import pymongo
import warez

#todo update if  dic exist in disk
# create delette database function

mongodb_uri = 'mongodb://localhost:27017'
db_name = 'warez_collection'

def add_database(disk ,listz):


	try:
		#connection = pymongo.Connection(mongodb_uri)
		connection = pymongo.Connection('localhost', 27017)
		db = connection[db_name]
	except:
		print('Error: Unable to connect to database.')
		connection = None

	if connection is not None:
		for dic in listz:		
			db.disk.insert(dic)


def show_database_disk(disk):


	try:
		#connection = pymongo.Connection(mongodb_uri)
		connection = pymongo.Connection('localhost', 27017)
		db = connection[db_name]
	except:
		print('Error: Unable to connect to database.')
		connection = None

	if connection is not None:
		
		print (db.disk.name)
		print connection.database_names(False) #false = no show system database
		
		for elem in db.disk.find():
			print elem
		


def find_hash(disk,hashz): 
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
		db.disk.find({hash_sha512:"848499599949"})
	

if __name__ == '__main__':
	pass
