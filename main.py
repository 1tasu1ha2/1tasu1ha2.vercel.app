from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import random, emoji, string
from uuid import uuid4
from curl_cffi.requests import Session

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/random-emoji")
def random_emoji(length: str="1"):
    try:
        num = float(length)
        if num.is_integer() and num > 0:
            return JSONResponse(content={
                "success": True,
                "result": "".join(random.choices(list(emoji.EMOJI_DATA.keys()), k=int(num)))
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

@app.post("/api/join")
async def join(token: str, invite: str):
    try:
        if not token and invite:
            return JSONResponse(content={
                "success": False,
                "message": "Please provide token and invite."
            }, status_code=400)
        if not token:
            return JSONResponse(content={
                "success": False,
                "message": "Please provide token."
            }, status_code=400)
        if not invite:
            return JSONResponse(content={
                "success": False,
                "message": "Please provide invite."
            }, status_code=400)
        session = Session()
        session.get("https://discord.com")
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en",
            "authorization": token,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9168 Chrome/128.0.6613.36 Electron/32.0.0 Safari/537.36",
            "x-discord-locale": "en-US",
            "x-debug-options": "bugReporterEnabled",
            "x-super-properties": "eyJvcyI6ICJXaW5kb3dzIiwgImJyb3dzZXIiOiAiRGlzY29yZCBDbGllbnQiLCAicmVsZWFzZV9jaGFubmVsIjogInN0YWJsZSIsICJjbGllbnRfdmVyc2lvbiI6ICIxLjAuOTE2OCIsICJvc192ZXJzaW9uIjogIjEwLjAuMTkwNDUiLCAic3lzdGVtX2xvY2FsZSI6ICJlbiIsICJicm93c2VyX3VzZXJfYWdlbnQiOiAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgZGlzY29yZC8xLjAuOTE2OCBDaHJvbWUvMTI4LjAuNjYxMy4zNiBFbGVjdHJvbi8zMi4wLjAgU2FmYXJpLzUzNy4zNiIsICJicm93c2VyX3ZlcnNpb24iOiAiMzIuMC4wIiwgImNsaWVudF9idWlsZF9udW1iZXIiOiAzMzkyMjEsICJuYXRpdmVfYnVpbGRfbnVtYmVyIjogNTQwMzksICJjbGllbnRfZXZlbnRfc291cmNlIjogbnVsbH0="
        }
        data = {
            "session_id": uuid4().hex
        }
        response = session.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json=data)
        return JSONResponse(content={
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json()
        }, status_code=response.status_code)
    except Exception as error:
        return JSONResponse(content={
            "success": False,
            "message": str(error)
        }, status_code=500)
