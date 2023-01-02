from scripts.utils.mongo_util import MongoConnect
from scripts.constants.app_configuration import DBConf

mongo_client = MongoConnect(uri=DBConf.MongoDB.uri)()
