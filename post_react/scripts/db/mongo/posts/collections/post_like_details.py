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
            collection=CollectionNames.post_like_details,
        )

    def find_all_posts(self):
        if posts := self.find(query={}, filter_dict={"_id": 0}):
            return list(posts)

    def find_post_by_id(self, post_id: str):
        if post := self.find_one(query={"post_id": post_id}):
            return post

    def update_post(self, post_id: str, post):
        if post := self.update_one(query={"post_id": post_id}, data=post, upsert=False):
            return post

    def like_post(self, post_id: str, user_id: str):
        return self.update_push_array(
            query={'post_id': post_id}, data=user_id, array_key='liked_by')
        

    def disklike_post(self, post_id: str, user_id: str):
        return self.update_pull_array(
            query={'post_id': post_id}, data=user_id, array_key='liked_by')
