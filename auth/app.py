from dotenv import load_dotenv

load_dotenv()
from scripts.config import SERVERConf

import uvicorn


if __name__ == "__main__":

    uvicorn.run("main:app", host=SERVERConf.host, port=SERVERConf.port, reload=True)
