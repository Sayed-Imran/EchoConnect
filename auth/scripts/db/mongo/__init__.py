from scripts.config import DBConf
from pymongo import MongoClient

mongo_client = MongoClient(DBConf.MongoDB.uri, connect=False)
