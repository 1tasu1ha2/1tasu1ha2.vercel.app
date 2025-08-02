from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import random, emoji, string, tls_client, requests, os
from uuid import uuid4

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

def hcaptcha(sitekey: str, host: str = "discord.com", rqdata: str = None):
    try:
        payload = {
            "sitekey": sitekey,
            "host": host,
            "key": os.getenv("key")
        }
        if rqdata:
            payload["rqdata"] = rqdata
        response = requests.post(f"https://futon-ga-futtonda.onrender.com/hcaptcha", json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("token")
        return None
    except Exception:
        return None

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
        session = tls_client.Session(client_identifier=f"chrome_124", random_tls_extension_order=True)
        session.get("https://discord.com")
        headers = {
            'accept': '*/*',
            'accept-language': 'en,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Asia/Saigon',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNC4wLjYzNjcuMTE4IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMjQuMC42MzY3LjExOCIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyOTcyNzQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0=',        
        }
        for attempt in range(10):
            data = {
                "session_id": uuid4().hex
            }
            response = session.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json=data)
            response_data = response.json()
            if response.status_code == 200:
                return JSONResponse(content={
                    "success": True,
                    "status_code": response.status_code,
                    "response": response_data
                })
            if "captcha_key" in response_data and "captcha_sitekey" in response_data:
                sitekey = response_data.get("captcha_sitekey")
                rqdata = response_data.get("captcha_rqdata")
                rqtoken = response_data.get("captcha_rqtoken")
                captcha_token = hcaptcha(sitekey, "discord.com", rqdata)
                if captcha_token:
                    headers["x-captcha-key"] = captcha_token
                    if rqtoken:
                        headers["x-captcha-rqtoken"] = rqtoken
                    continue
                else:
                    return JSONResponse(content={
                        "success": False,
                        "message": "Failed to solve hCaptcha ぴよ"
                    }, status_code=500)
            else:
                return JSONResponse(content={
                    "success": False,
                    "status_code": response.status_code,
                    "response": response_data
                }, status_code=response.status_code)
        return JSONResponse(content={
            "success": False,
            "message": "Failed to solve hCaptcha うに"
        }, status_code=500)
    except Exception as error:
        return JSONResponse(content={
            "success": False,
            "message": str(error)
        }, status_code=500)
