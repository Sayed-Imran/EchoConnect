import shortuuid
import logging
import os
from scripts.db.mongo import mongo_client
from scripts.utils.cloud_storage_util import CloudStorageUtil
from scripts.db.mongo.posts.collections.post_details import Posts
from scripts.db.mongo.connect_base.collections.user import User
from scripts.utils.publisher_util import Publisher
import pendulum

class PostsHandler:
    def __init__(self):
        self.posts = Posts(mongo_client=mongo_client)
        self.user = User(mongo_client=mongo_client)
        self.cloud_storage = CloudStorageUtil()
        self.publisher = Publisher(
            topic_path='projects/level-slate-373806/topics/post-crud-events')

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

    async def create_post(self, file, post: dict, user_id:str):
        try:
            post['post_id'] = shortuuid.uuid()
            post['user_id'] = user_id
            user = self.user.get_user(user_id=user_id)
            post['user_name'] = user['user_name']
            post['user_profile'] = user['profile-image']
            if file:
                with open(file.filename, 'wb') as f:
                    f.write(await file.read())
                file_url = await self.cloud_storage.upload_blob(bucket_name='echo-connect-objects',source_file_name=file.filename, destination_blob_name=post['post_id']+'.'+file.filename.split('.')[-1])
                os.remove(file.filename)
            post['object_url'] = file_url if file else None
            post['created_at'] = pendulum.now().strftime("%d/%m/%Y")
            post['updated_at'] = pendulum.now().strftime("%d/%m/%Y")
            post['likes'] = 0
            self.posts.create_post(data=post)
            post.pop('_id', None)
            self.publisher.publish(data='create_post', attributes=post)
            return post
        except Exception as e:
            print(e.args)
            logging.error(e.with_traceback(None))

    def update_post(self, post_id: str, post):
        try:
            post['updated_at'] = pendulum.now().strftime("%d/%m/%Y")
            if post := self.posts.update_post(post_id=post_id, post=post):
                return post
        except Exception as e:
            print(e.args)

    def delete_post(self, post_id: str, user_id:str):
        try:
            if post := self.posts.find_post_by_id(post_id=post_id):
                if post['user_id'] != user_id:
                    raise Exception('Unauthorized')
                if post['object_url']:
                    file_name = post['object_url'].split('/')[-1]
                    self.cloud_storage.delete_blob(
                        bucket_name="echo-connect-objects", blob_name=file_name)
                self.publisher.publish(data='delete_post', attributes=post)
                if post := self.posts.delete_post(post_id=post_id):
                    return post
        except Exception as e:
            print(e.args)
