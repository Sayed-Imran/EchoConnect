import logging
from typing import Dict, Optional
from pymongo.cursor import Cursor
from pymongo import MongoClient
from scripts.errors import MongoException

UPDATE_EXCEPTION_MSG = "Unable to update data"
logger = logging.getLogger(__name__)

class MongoConnect:
    def __init__(self, uri):
        """
        The __init__ function is called when an instance of the class is created. 
        The __init__ function can take arguments, but self is always the first one. 
        Self is just a reference to the instance of the class. It’s automatically 
        passed in when you instantiate an instance of the class.
        
        :param self: Refer to the object instance
        :param uri: Specify the connection string to connect to the mongo database
        :return: Nothing
        :doc-author: Sayed Imran
        """
        
        try:
            self.uri = uri
            self.client = MongoClient(self.uri, connect=False)

        except Exception as e:
            raise MongoException("Unable to connect to mongo") from e

    def __call__(self, *args, **kwds):
        """
        The __call__ function is a special method that allows an object to be called just like a function. 
        The __call__ method can reference variables local to the object, because it is executed in the context of that object. 
        It’s kind of like how methods within a class have access to all the attributes and methods of that class.
        
        :param self: Access variables that belongs to the class
        :param *args: Pass a non-keyworded, variable-length argument list
        :param **kwds: Pass keyword arguments to the __call__ function
        :return: The client object
        :doc-author: Sayed Imran
        """
        return self.client


class MongoCollectionBaseClass:
    def __init__(self, mongo_client, database, collection):
        """
        The __init__ function is called when an instance of the class is created. 
        It initializes the attributes of the class, and sets up a connection to MongoDB.
        
        
        :param self: Refer to the object itself
        :param mongo_client: Connect to the mongodb server
        :param database: Specify the database name
        :param collection: Specify the name of the collection to use
        :return: The mongoclient object
        :doc-author: Sayed Imran
        """
        self.client = mongo_client
        self.database = database
        self.collection = collection

    def insert_one(self, data: dict):
        """
        The insert_one function inserts a single document into the specified collection.
        It returns the inserted_id of the new document.
        
        :param self: Reference the class instance
        :param data: dict: Pass the data that is to be inserted into the database
        :return: The _id of the inserted document
        :doc-author: Sayed Imran
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.insert_one(data)

        except Exception as e:
            logger.exception(e.args)
            raise MongoException("Unable to insert data") from e

    def find(
        self,
        query: Dict,
        filter_dict: Optional[Dict] = None,
        sort=None,
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> Cursor:
        """
        The find function returns a cursor to the data in the database. 
        The query is a dictionary that contains the filter for documents and other options. 
        The filter_dict is an optional argument that can be used to specify what fields are returned in each document. The sort argument allows you to sort by one or more fields, with direction specified as well.
        
        :param self: Refer to the class instance
        :param query: Dict: Specify the query to be executed
        :param filter_dict: Optional[Dict]: Filter out unwanted data
        :param sort: Sort the results of the query
        :param skip: Optional[int]: Specify the number of documents to skip in a find operation
        :param limit: Optional[int]: Limit the number of documents returned in a query
        :param : Specify the number of documents to skip before starting to return the results
        :return: A cursor object
        :doc-author: Trelent
        """
        if sort is None:
            sort = []
        if filter_dict is None:
            filter_dict = {"_id": 0}
        database_name = self.database
        collection_name = self.collection
        try:
            db = self.client[database_name]
            collection = db[collection_name]
            if len(sort) > 0:
                cursor = (
                    collection.find(
                        query,
                        filter_dict,
                    )
                    .sort(sort)
                    .skip(skip)
                )
            else:
                cursor = collection.find(query, filter_dict).skip(skip)
            if limit:
                cursor = cursor.limit(limit)

            return cursor
        except Exception as e:
            raise MongoException("Unable to find data") from e

    def find_one(self, query: Dict, filter_dict: Optional[Dict] = None):
        try:
            database_name = self.database
            collection_name = self.collection
            if filter_dict is None:
                filter_dict = {"_id": 0}
            db = self.client[database_name]
            collection = db[collection_name]
            return collection.find_one(query, filter_dict)
        except Exception as e:
            raise MongoException("Unable to find data") from e

    def update_one(self, query: Dict, data: Dict, upsert: bool):
        try:

            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(query, {"$set": data}, upsert=upsert)
            return response.modified_count
        except Exception as e:
            raise MongoException(UPDATE_EXCEPTION_MSG) from e

    def delete_one(self, query: Dict):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.delete_one(query)
            return response.deleted_count
        except Exception as e:
            raise MongoException("Unable to delete data") from e

    def update_push_array(
        self, query: Dict, data: str, array_key: str, upsert: bool = True
    ):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(
                query, {"$push": {array_key: data}}, upsert=upsert
            )
            return response.modified_count

        except Exception as e:
            raise MongoException(UPDATE_EXCEPTION_MSG) from e

    def update_pull_array(
        self, query: Dict, data: str, array_key: str, upsert: bool = True
    ):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(
                query, {"$pull": {array_key: data}}, upsert=upsert
            )
            return response.modified_count

        except Exception as e:
            print(e.args)
            raise MongoException(UPDATE_EXCEPTION_MSG) from e
