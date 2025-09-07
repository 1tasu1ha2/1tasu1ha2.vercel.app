from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import random, emoji, string

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get('/api')
async def index():
    try:
        return JSONResponse(
            content={
                'success': True,
                'data': {
                    'routes': [r.path for r in app.routes]
                }
            },
            status_code=200
        )
    except Exception as err:
        return JSONResponse(
            content={
                'success': False,
                'data': {
                    'message': str(err)
                }
            },
            status_code=500
        )

@app.get('/api/random/alphanumeric')
async def random_alphanumeric(
    length: int=1,
    uppercase: bool=True,
    lowercase: bool=True,
    digit: bool=True,
    symbol: bool=False
):
    try:
        chars = ''
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if digit:
            chars += string.digits
        if symbol:
            chars += string.punctuation
        if chars == '':
            return JSONResponse(
                content={
                    'success': False,
                    'data': {
                        'message': '\'uppercase\' or \'lowercase\' or \'digit\' or \'symbol\' must be true.'
                    }
                },
                status_code=400
            )
        if length < 0:
            return JSONResponse(
                content={
                    'success': False,
                    'message': '\'length\' must be greater than 0.'
                },
                status_code=400
            )
        return JSONResponse(
            content={
                'success': True,
                'data': {
                    'string': ''.join(random.choices(chars, k=length))
                }
            },
            status_code=200
        )
    except Exception as err:
        return JSONResponse(
            content={
                'success': False,
                'data': {
                    'message': str(err)
                }
            },
            status_code=500
        )

@app.get('/api/random/emoji')
async def random_emoji(
    length: int=1
):
    try:
        if length < 0:
            return JSONResponse(
                content={
                    'success': False,
                    'message': '\'length\' must be greater than 0.'
                },
                status_code=400
            )
        return JSONResponse(
            content={
                'success': True,
                'data': {
                    'string': ''.join(random.choices(list(emoji.EMOJI_DATA.keys()), k=length))
                }
            },
            status_code=200
        )
    except Exception as err:
       return JSONResponse(
           content={
                'success': False,
                'data': {
                    'message': str(err)
                }
            },
            status_code=500
        )
