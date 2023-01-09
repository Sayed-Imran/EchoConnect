from scripts.db.mongo import mongo_client
from scripts.db.mongo.posts.collections.post_details import Posts


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

    def update_post(self, post_id: str, post):
        try:
            if post := self.posts.update_post(post_id=post_id, post=post):
                return post
        except Exception as e:
            print(e.args)

    def like_post(self, post_id: str):
        try:
            post = self.posts.find_one(query={"post_id": post_id})
            post['likes'] += 1
            self.posts.update_one(
                query={"post_id": post_id}, data=post, upsert=False)
        except Exception as e:
            print(e.args)

    def dislike_post(self, post_id: str):
        try:
            post = self.posts.find_one(query={"post_id": post_id})
            post['likes'] -= 1
            self.posts.update_one(
                query={"post_id": post_id}, data=post, upsert=False)
        except Exception as e:
            print(e.args)