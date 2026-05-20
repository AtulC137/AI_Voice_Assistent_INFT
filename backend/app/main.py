from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.websocket import websocket_endpoint
from app.config import SARVAM_API_KEY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():

    return {
        "status":"running"
    }


@app.websocket("/ws")
async def ws_route(
    websocket: WebSocket
):

    await websocket_endpoint(
        websocket
    )