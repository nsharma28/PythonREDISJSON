from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=0)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["POST", "GET"], allow_headers=["*"], max_age=3600,)


@app.get('/')
def home():
    return {'message': 'we are in home page'}


def configure_routing():
    pass


if __name__ == '__main__':
    configure_routing()
    uvicorn.run("main:app", host="127.0.0.1", port=5000, loop='asyncio', workers=2, log_level="info")
else:
    configure_routing()
