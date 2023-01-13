from scripts.constants import DatabasesNames, CollectionNames
from scripts.utils.mongo_util import MongoCollectionBaseClass


class Posts(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        """
        The __init__ function is called when an instance of the class is created.
        The __init__ function receives a reference to the instance as its first argument,
        which by convention we call self.

        :param self: Refer to the object of the class that is being created
        :param mongo_client: Connect to the mongo database
        :return: The object of the class
        :doc-author: Sayed Imran
        """
        super().__init__(
            mongo_client=mongo_client,
            database=DatabasesNames.posts,
            collection=CollectionNames.post_details,
        )

    def find_all_posts(self):
        if posts := self.find(query={}, filter_dict={"_id": 0}):
            return list(posts)

    def find_post_by_id(self, post_id: str):
        if post := self.find_one(query={"post_id": post_id}):
            return post

    def create_post(self, data):
        self.insert_one(data=data)

    def update_post(self, post_id: str, post):
        if post := self.update_one(query={"post_id": post_id}, data=post, upsert=False):
            return post

    def delete_post(self, post_id: str):
        if post := self.delete_one(query={"post_id": post_id}):
            return post
        
    def fetch_by_aggregate(self, pipelines: list):
        if posts := self.aggregate(pipelines=pipelines):
            return list(posts)
