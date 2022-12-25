import shortuuid
import logging
import os
from datetime import datetime
from scripts.db.mongo import mongo_client
from scripts.utils.cloud_storage_util import CloudStorageUtil
from scripts.db.mongo.posts.collections.post_details import Posts
from scripts.utils.publisher_util import Publisher


class PostsHandler:
    def __init__(self):
        self.posts = Posts(mongo_client=mongo_client)
        self.cloud_storage = CloudStorageUtil()
        self.publisher = Publisher(
            topic_path='projects/silver-approach-371713/topics/post-events')

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
            post['post_id'] = shortuuid.uuid()
            if file:
                with open(file.filename, 'wb') as f:
                    f.write(await file.read())
                file_url = await self.cloud_storage.upload_blob(bucket_name='crazeops-objects',
                                                                source_file_name=file.filename, destination_blob_name=post['post_id']+'.'+file.filename.split('.')[-1])
                os.remove(file.filename)
            post['object_url'] = file_url if file else None
            post['created_at'] = datetime.now()
            post['updated_at'] = datetime.now()
            post['likes'] = 0
            self.posts.create_post(data=post)
            post.pop('_id', None)
            self.publisher.publish(data='create_post', attributes=post)
            return post
        except Exception as e:
            print(e.args)
            logging.error(e.with_traceback())

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
                if post['object_url']:
                    file_name = post['object_url'].split('/')[-1]
                    self.cloud_storage.delete_blob(
                        bucket_name="crazeops-objects", blob_name=file_name)
                self.publisher.publish(data='delete_post', attributes=post)
                if post := self.posts.delete_post(post_id=post_id):
                    return post
        except Exception as e:
            print(e.args)
