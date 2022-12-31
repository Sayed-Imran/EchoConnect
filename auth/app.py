from scripts.config import SERVERConf

import uvicorn


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    uvicorn.run("main:app", host=SERVERConf.host, port=SERVERConf.port, reload=True)
