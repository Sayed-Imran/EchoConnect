from google.cloud import storage


class CloudStorageUtil:
    def __init__(self):
        """
        The __init__ function is called the constructor and is automatically invoked when an object of a class is created.
        The __init__ function can be thought of as a parameterized constructor that takes arguments and creates instance variables.

        :param self: Reference the object itself
        :return: The object that was created
        :doc-author: Sayed Imran
        """
        self.storage_client = storage.Client()

    async def upload_blob(
        self, bucket_name, source_file_name, destination_blob_name
    ) -> str:
        """
        The upload_blob function uploads a file to the bucket.
        :param self: Access variables that belongs to the class
        :param bucket_name: Specify the name of the bucket to upload to
        :param source_file_name: Specify the name of the file that you want to upload
        :param destination_blob_name: Specify the name of the file that will be stored in your bucket
        :return: The public url of the blob
        :doc-author: Sayed Imran
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            print(f"File {source_file_name} uploaded to {destination_blob_name}")
            return blob.public_url
        except Exception as e:
            print(e)

    def delete_blob(self, bucket_name, blob_name):
        """
        The delete_blob function deletes a blob from the bucket.
        :param self: Reference the class itself
        :param bucket_name: Specify the name of the bucket that contains the blob to delete
        :param blob_name: Specify the blob that you want to delete
        :return: None
        :doc-author: Sayed Imran
        """

        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            print(f"Blob {blob_name} deleted.")
        except Exception as e:
            print(e)
