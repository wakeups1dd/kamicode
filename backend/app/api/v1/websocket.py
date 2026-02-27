from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Just keep the connection open and wait for messages (though we mostly broadcast)
            data = await websocket.receive_text()
            # If clients send messages, we could handle them here
    except WebSocketDisconnect:
        manager.disconnect(websocket)
