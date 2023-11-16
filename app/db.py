import os

from pymongo import MongoClient

DB_HOST = os.getenv('DB_HOST', 'mongodb://localhost')
DB_PORT = int(os.getenv('DB_PORT', '27017'))
DB_NAME = os.getenv('DB_NAME', 'TestDb')

#client = MongoClient(DB_HOST, DB_PORT, timeoutMS=3000, connectTimeoutMS=3000, socketTimeoutMS=3000)
client = MongoClient(DB_HOST, DB_PORT)
database = client.get_database(DB_NAME)