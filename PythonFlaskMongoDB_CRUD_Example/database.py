from pymongo import MongoClient
import certifi
import pymongo

MONGO_URI = 'mongodb+srv://Name:password@cluster0.lruo3ww.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["db_Products_app"]
        # Test the connection by listing the collections
        print("Connected to the database. Collections: ", db.list_collection_names())
    except pymongo.errors.OperationFailure as e:
        print(f'Authentication failed: {e.details}')
    except Exception as e:
        print(f'Error connecting to the database: {e}')
    return db