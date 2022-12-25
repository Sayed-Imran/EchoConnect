import logging
import os
from datetime import datetime
from scripts.db.mongo import mongo_client
from scripts.db.mongo.posts.collections.post_like_details import Posts


class PostsHandler:
    def __init__(self):
        self.posts = Posts(mongo_client=mongo_client)

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

    def create_post(self, post_id: str):
        try:
            post = {"post_id": post_id, "liked_by": []}
            print(post,type(post))
            self.posts.create_post(data=post)
            post.pop('_id', None)
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
                post = self.posts.delete_post(post_id=post_id)
                return post
        except Exception as e:
            print(e.args)
