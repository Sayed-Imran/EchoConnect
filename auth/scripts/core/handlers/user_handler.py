import shortuuid
import os
from scripts.db.mongo.connect_base.collections.user import User
from scripts.db.mongo import mongo_client
from scripts.schemas import RegisterSchema
from scripts.logging import logger
from scripts.errors import RegistrationError, LoginError
from scripts.utils.security.hash import hash_password, verify_pass
from scripts.utils.security.jwt_util import JWT
from google.oauth2 import id_token
from google.auth.transport import requests
from scripts.config import AuthenticationConf
from scripts.utils.cloud_storage_util import CloudStorageUtil


class UserHandler:
    def __init__(self) -> None:
        """
        The __init__ function is called when an instance of the class is created.
        It initializes attributes that all instances of the class will have access to.

        :param self: Refer to the object that is being created
        :return: None
        :doc-author: Sayed Imran
        """
        self.user_conn = User(mongo_client)
        self.jwt_util = JWT()
        self.cloud_storage = CloudStorageUtil()

    def register_user(self, register_user: RegisterSchema):
        """
        The register_user function is used to register a new user.
        It takes in a RegisterSchema object and returns the newly created user_id

        :param self: Access the class attributes
        :param register_user: RegisterSchema: Validate the user input
        :return: None
        :doc-author: Sayed Imran
        """
        try:
            if self.user_conn.get_user(register_user.email):
                raise RegistrationError("User already exists")
            register_user.user_id = shortuuid.uuid()
            register_user.password = hash_password(register_user.password)
            register_user = register_user.dict()
            register_user['user_name'] = register_user['first_name'] + \
                '_' + register_user['last_name']
            register_user['profile-image'] = 'https://storage.googleapis.com/echo-connect-objects/default-avatar.jpeg'
            self.user_conn.insert_user(register_user)
        except RegistrationError as re:
            logger.exception(re.args)
            raise re
        except Exception as e:
            logger.exception(e.__traceback__)
            raise RegistrationError("Unable to register user") from e

    async def upload_profile_image(self, file, user_data: dict):
        try:
            with open(file.filename, "wb") as f:
                f.write(await file.read())
            file_url = await self.cloud_storage.upload_blob(
                bucket_name="echo-connect-objects",
                source_file_name=file.filename,
                destination_blob_name=user_data["user_id"] + "." +
                file.filename.split(".")[-1],
            )
            os.remove(file.filename)
            self.user_conn.update_user(
                user_id=user_data['user_id'], data={"profile-image": file_url}
            )
        except Exception as e:
            print(e.args)

    def login_user(self, email: str, password: str):
        """
        The login_user function is used to login a user. It takes in an email and password as parameters,
        and returns a JWT token if the login is successful. If the user cannot be found or if the password does not match,
        it raises an exception.

        :param self: Access the class attributes
        :param email: str: Pass in the email address of the user
        :param password: str: Verify the password
        :return: A JWT token
        :doc-author: Sayed Imran
        """
        try:
            user = self.user_conn.get_user(email)
            if not user:
                raise LoginError("User not found")
            if not verify_pass(password, user["password"]):
                raise LoginError("Invalid password")
            return self.jwt_util.create_token(
                {"email": email, "user_id": user["user_id"]}
            )
        except LoginError as le:
            logger.exception(le.args)
            raise le
        except Exception as e:
            logger.exception(e.__traceback__)
            raise LoginError("Unable to login user") from e

    def register_login_google_user(self, token: str):
        """
        The register_login_google_user function is used to register a user using Google OAuth.
        It takes in the token as an argument and returns a JWT token for the user.

        :param self: Access the class attributes
        :param token: str: Pass the token that is retrieved from the google login page
        :return: A jwt token
        :doc-author: Trelent
        """
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), AuthenticationConf.google_id
            )
            user = self.user_conn.get_user(id_info["email"])
            if not user:
                user = RegisterSchema(
                    user_id=shortuuid.uuid(),
                    email=id_info["email"],
                    password=hash_password(shortuuid.uuid()),
                    first_name=id_info["given_name"],
                    last_name=id_info["family_name"],
                ).dict()
                self.user_conn.insert_user(user)
            return self.jwt_util.create_token(
                {"email": id_info["email"], "user_id": user["user_id"]}
            )
        except Exception as e:
            logger.exception(e.__traceback__)
            raise LoginError("Unable to login using Google") from e
