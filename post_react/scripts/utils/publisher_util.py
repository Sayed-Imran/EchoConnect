from google.cloud import pubsub_v1


class Publisher:
    def __init__(self, topic_path):
        self.topic_path = topic_path
        self.publisher_client = pubsub_v1.PublisherClient()

    def publish(self, data, attributes):
        future = self.publisher_client.publish(
            self.topic_path, data=data.encode("utf-8"), **attributes
        )
        print(future.result())
        return "Published messages."
