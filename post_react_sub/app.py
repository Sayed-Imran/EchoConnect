from google.cloud import pubsub_v1
from dotenv import load_dotenv
load_dotenv()
from scripts.core.handlers.post_handler import PostsHandler

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    'level-slate-373806', 'post-react-events-sub')
posts_handler = PostsHandler()


def callback(message):
    print(f'data :{message}')
    if message.data.decode('utf-8') == 'post_liked':
        posts_handler.like_post(message.attributes['post_id'])
    elif message.data.decode('utf-8') == 'post_disliked':
        posts_handler.dislike_post(message.attributes['post_id'])
    message.ack()


streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result()
    except Exception as e:
        streaming_pull_future.cancel()
        print(e)
