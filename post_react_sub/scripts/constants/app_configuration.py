if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()


import sys
import os
import os.path
from configparser import ConfigParser, BasicInterpolation


class EnvInterpolation(BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        if not os.path.expandvars(value).startswith("$"):
            return os.path.expandvars(value)
        else:
            return


try:
    config = ConfigParser(interpolation=EnvInterpolation())
    config.read("conf/application.conf")

except Exception:
    print("Error while loading the configuration")
    print("Exiting")
    sys.exit(1)


class DBConf:
    class MongoDB:
        uri = config.get("MONGO_DB", "uri")
        if not uri:
            print("Error, ENV variable Mongo URI not set")
            sys.exit(1)

    class GoogleCred:
        cred = config.get("GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_CRED")
        if not cred:
            print("Error, ENV variable Google Cred not set")
            sys.exit(1)
