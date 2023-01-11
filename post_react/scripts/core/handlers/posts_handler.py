from scripts.db.mongo import mongo_client
from scripts.utils.publisher_util import Publisher
from scripts.db.mongo.posts.collections.post_like_details import Posts


class PostsHandler:
    def __init__(self):
        self.posts = Posts(mongo_client=mongo_client)
        self.publisher = Publisher(
            topic_path="projects/level-slate-373806/topics/post-react-events"
        )

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

    def post_like_dislike(self, post_id: str, user_id: str):
        try:
            post = self.posts.find_one(query={"post_id": post_id})
            if user_id not in post["liked_by"]:
                self.posts.like_post(post_id=post_id, user_id=user_id)
                self.publisher.publish(
                    data="post_liked", attributes={"post_id": post_id}
                )
                like_count = len(post["liked_by"]) + 1
            else:
                self.posts.disklike_post(post_id=post_id, user_id=user_id)
                self.publisher.publish(
                    data="post_disliked", attributes={"post_id": post_id}
                )
                like_count = len(post["liked_by"]) - 1
            return {"like_count": like_count}
        except Exception as e:
            print(e.args)
