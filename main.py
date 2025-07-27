from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import random, emoji

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/random-emoji")
def random_emoji(length: float=1):
    if length.is_integer() and length > 0:
        length = int(length)
        return JSONResponse(content={
            "success": True,
            "result": "".join(random.choices(list(emoji.EMOJI_DATA.keys()), k=length))
        })
    else:
        return JSONResponse(content={
            "success": False,
            "message": "Please provide a positive integer."
        }, status_code=400)
