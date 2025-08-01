from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import random, emoji, string

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/random-emoji")
def random_emoji(length: str = "1"):
    try:
        num = float(length)
        if num.is_integer() and num > 0:
            emojis = [
                e for e in emoji.EMOJI_DATA.keys()
                if not any(tone in e for tone in ["🏻", "🏼", "🏽", "🏾", "🏿"])
            ]
            return JSONResponse(content={
                "success": True,
                "result": "".join(random.choices(emojis, k=int(num)))
            })
        else:
            raise ValueError
    except ValueError:
        return JSONResponse(content={
            "success": False,
            "message": "Length must be a positive integer."
        }, status_code=400)

@app.get("/api/random-string")
def random_string(length: str="1"):
    try:
        num = float(length)
        if num.is_integer() and num>0:
            return JSONResponse(content={
                "success": True,
                "result": "".join(random.choices(string.ascii_letters+string.digits, k=int(num)))
            })
        else:
            raise ValueError
    except ValueError:
        return JSONResponse(content={
            "success": False,
            "message": "Length must be a positive integer."
        }, status_code=400)
