from scripts.utils.mongo_util import MongoCollectionBaseClass
from scripts.constants import DatabasesNames, CollectionNames
from scripts.constants.db_keys import UserKeys


class User(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(mongo_client, DatabasesNames.connect_base, CollectionNames.user)


    def get_user(self, user_id: str):
        return self.find_one({"user_id": user_id})
