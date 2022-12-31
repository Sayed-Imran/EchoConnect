from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(passwd: str):
    return pwd_context.hash(passwd)


def verify_pass(passwd, hashed):
    return pwd_context.verify(passwd, hashed)
