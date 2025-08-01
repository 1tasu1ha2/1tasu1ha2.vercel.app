from fastapi import FastAPI, Request
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
async def join(request: Request):
    body = await request.json()
    token = body.get("token")
    invite = body.get("invite")
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
            "accept-language": "ja",
            "authorization": token,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15",
            "x-discord-locale": "ja",
            "x-debug-options": "bugReporterEnabled",
            "x-super-properties": "eyJvcyI6ImlPUyIsImJyb3dzZXIiOiJNb2JpbGUgU2FmYXJpIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTVfNykgQXBwbGVXZWJLaXQvNjA1LjEuMTUgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzE4LjQgU2FmYXJpLzYwNS4xLjE1IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTguNCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQyNTQ4NywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6ImE4ZmJiNzIzLTk3MTktNDM2Ni1iZWYwLTIxODNkZjhiYTliNiIsImxhdW5jaF9zaWduYXR1cmUiOiIyNDNjNjJlMC0wMjZhLTQ0ZjctOTAxOC1hMmFiZDBjYWYxOGYiLCJjbGllbnRfaGVhcnRiZWF0X3Nlc3Npb25faWQiOiI3NmU5YjczYS00ZDc0LTQ0NmMtODFlYS0zMTI3ZjgxZGFiMGUiLCJjbGllbnRfYXBwX3N0YXRlIjoiZm9jdXNlZCJ9"
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
