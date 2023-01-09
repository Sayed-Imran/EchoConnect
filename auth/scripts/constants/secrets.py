from scripts.config import AuthenticationConf


class Secrets:
    LOCK_OUT_TIME_MINS = 30
    UNIQUE_KEY = AuthenticationConf.encryption_key
    ALG = "HS256"
