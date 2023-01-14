from fastapi import HTTPException, status, Depends, UploadFile, File
from fastapi.routing import APIRouter
from scripts.constants import APIConstants
from scripts.errors import RegistrationError, LoginError
from scripts.schemas import (
    RegisterSchema,
    LoginSchema,
    DefaultResponseSchema,
    GoogleLoginSchema,
)
from scripts.core.handlers.user_handler import UserHandler
from scripts.utils.security.jwt_util import JWT

router = APIRouter(prefix=APIConstants.api_authenticate_base)


@router.post(APIConstants.api_register_user)
def register_user(user_data: RegisterSchema):
    try:
        user_handler = UserHandler()
        user_handler.register_user(user_data)
        return DefaultResponseSchema(message="Registration Successfull!")
    except RegistrationError as re:
        return DefaultResponseSchema(status="failed", message=re.args[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post(APIConstants.api_login_user)
def login_user(login_data: LoginSchema):
    try:
        user_handler = UserHandler()
        token = user_handler.login_user(login_data.email, login_data.password)
        return DefaultResponseSchema(
            message="Logged In Successfull!", data={"token": token}
        )
    except LoginError as le:
        return DefaultResponseSchema(status="failed", message=le.args[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@router.post(APIConstants.profile_image)
async def profile_image(file: UploadFile = File(None), user_data = Depends(JWT().get_current_user)):
    try:
        user_handler = UserHandler()
        await user_handler.upload_profile_image(file, user_data)
        return DefaultResponseSchema(
            message="Profile Pic Upload Successfull!"
        )
    except LoginError as le:
        return DefaultResponseSchema(status="failed", message=le.args[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get(APIConstants.get_user)
def get_user_details(user_data = Depends(JWT().get_current_user)):
    try:
        user_handler = UserHandler()
        user = user_handler.get_user_details(user_data['email'])
        user.pop('password')
        return DefaultResponseSchema(
            message="User Details Fetched Successfull!", data=user
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.args,
        ) from e

@router.post(APIConstants.api_google_login_user)
def google_login_user(login_data: GoogleLoginSchema):
    try:
        user_handler = UserHandler()
        token = user_handler.register_login_google_user(login_data.id_token)
        return DefaultResponseSchema(
            message="Logged In Successfull!", data={"token": token}
        )
    except LoginError as le:
        return DefaultResponseSchema(status="failed", message=le.args[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
