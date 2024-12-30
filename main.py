
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/masterfile/{tickers}")
def read_item(tickers: str):
    return using_websocket.run_websocket_session(tickers.split(","))
