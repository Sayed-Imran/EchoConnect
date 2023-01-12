import uvicorn

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
