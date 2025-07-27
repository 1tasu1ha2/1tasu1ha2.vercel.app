from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random, emoji

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

@app.get("/api/random-emoji")
def random_emoji(length: int=1):
    res = JSONResponse(content={
        "success": True,
        "result": "".join(random.choices(list(emoji.EMOJI_DATA.keys()), k=length))
    }, status_code=200)
    return res
