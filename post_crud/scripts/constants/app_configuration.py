if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()


import sys
import os
import os.path
from configparser import ConfigParser, BasicInterpolation
import json, shortuuid


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

except:
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
        cred = json.loads(cred)
        cred["private_key"] = cred["private_key"].replace("\\n", "\n")
        if not cred:
            print("Error, ENV variable Google Cred not set")
            sys.exit(1)
        cred_file = f"{shortuuid.uuid()}.json"
        cred_file_path = f"./{cred_file}"
        with open(cred_file_path, "w") as cred_write:
            cred_write.write(json.dumps(cred))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_file_path
