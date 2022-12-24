import shortuuid
from datetime import datetime
from scripts.db.mongo import mongo_client
from scripts.utils.cloud_storage_util import CloudStorageUtil
from scripts.db.mongo.posts.collections.post_details import Posts


class PostsHandler:
    def __init__(self):
        self.posts = Posts(mongo_client=mongo_client)
        self.cloud_storage = CloudStorageUtil()

    def get_all_posts(self):
        try:
            if posts := self.posts.find_all_posts():
                return posts
        except Exception as e:
            print(e.args)

    def get_post_by_id(self, post_id: str):
        try:
            if post := self.posts.find_post_by_id(post_id=post_id):
                return post
        except Exception as e:
            print(e.args)

    async def create_post(self, file, post: dict):
        try:
            with open(file.filename, 'wb') as f:
                f.write(await file.read())
            post['post_id'] = shortuuid.uuid()
            file_url = await self.cloud_storage.upload_blob(bucket_name='crazeops-objects',
                source_file_name=file.filename, destination_blob_name=post['post_id']+file.filename.split('.')[-1])
            post['object_url'] = file_url
            post['created_at'] = datetime.now()
            post['updated_at'] = datetime.now()
            self.posts.create_post(data=post)
            post.pop('_id')
            return post
        except Exception as e:
            print(e.args)
            print(e.args)

    def update_post(self, post_id: str, post):
        try:
            post['updated_at'] = datetime.now()
            if post := self.posts.update_post(post_id=post_id, post=post):
                return post
        except Exception as e:
            print(e.args)

    def delete_post(self, post_id: str):
        try:
            if post := self.posts.find_post_by_id(post_id=post_id):
                file_name = post['object_url'].split('/')[-1]
                self.cloud_storage.delete_blob(file_name=file_name)
            if post := self.posts.delete_post(post_id=post_id):
                return post
        except Exception as e:
            print(e.args)

    def delete_file(self, file_name: str):
        try:
            if file_delete := self.cloud_storage.delete_blob(file_name=file_name):
                return file_delete
        except Exception as e:
            print(e.args)
