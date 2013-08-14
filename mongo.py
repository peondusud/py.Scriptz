import pymongo

connection = Connection('localhost', 27017)
db = connection.database
collection = db.warez_collection
