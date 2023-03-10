from datetime import timezone
from typing import Dict
from jose import JWTError, jwt
from datetime import datetime, timedelta
from scripts.constants.secrets import Secrets
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer


class JWT:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def __init__(self) -> None:
        self.max_login_age = Secrets.LOCK_OUT_TIME_MINS
        self.unique_key = Secrets.UNIQUE_KEY
        self.algo = Secrets.ALG

    def create_token(self, data: Dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.max_login_age)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, key=self.unique_key, algorithm=self.algo)

    def verify_token(self, token: str, credential_exception):
        try:

            payload = jwt.decode(token, Secrets.UNIQUE_KEY, algorithms=[Secrets.ALG])
            email: str = payload.get("email")
            user_id: str = payload.get("user_id")

            if user_id is None:
                raise credential_exception
            return {"email": email, "user_id": user_id}
        except JWTError as e:
            raise credential_exception from e

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could Not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return self.verify_token(token, credential_exception=credential_exception)
