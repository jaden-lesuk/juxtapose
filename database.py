from flask import Flask
from flask_pymongo import pymongo

DB = "mongodb+srv://admin:735uK74dOMDBA@lesuk.8p4iy.mongodb.net/juxtapose?retryWrites=true&w=majority"

client = pymongo.MongoClient(DB)
database = client.get_database('juxtapose')
collection = pymongo.collection.Collection(database, 'predictions')