from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import random, string
import emoji_data_python

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

emojis = [e.char for e in emoji_data_python.emoji_data if not e.is_skin_tone and e.is_emoji]

@app.get("/api/random-emoji")
def random_emoji(length: str = "1"):
    try:
        num = float(length)
        if num.is_integer() and num > 0:
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
def random_string(length: str = "1"):
    try:
        num = float(length)
        if num.is_integer() and num > 0:
            return JSONResponse(content={
                "success": True,
                "result": "".join(random.choices(string.ascii_letters + string.digits, k=int(num)))
            })
        else:
            raise ValueError
    except ValueError:
        return JSONResponse(content={
            "success": False,
            "message": "Length must be a positive integer."
        }, status_code=400)
