from scripts.utils.mongo_util import MongoCollectionBaseClass
from scripts.constants import DBNames, CollectionNames
from scripts.constants.db_keys import UserKeys


class User(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(mongo_client, DBNames.connect_base, CollectionNames.user)

    def insert_user(self, data: dict):
        return self.update_one(
            {UserKeys.KEY_EMAIL: data[UserKeys.KEY_EMAIL]}, data, upsert=True
        )

    def get_user(self, email: str):
        return self.find_one({UserKeys.KEY_EMAIL: email})

    def update_user(self, user_id: str, data: dict):
        return self.update_one({"user_id": user_id}, data, upsert=False)