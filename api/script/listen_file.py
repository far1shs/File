from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
from pathlib import Path
import os

app = APIRouter()

@app.websocket("/listen_file")
async def index(websocket: WebSocket):
    await websocket.accept()
    path_str = await websocket.receive_text()

    # 确保路径名在 Windows 上正确处理
    if os.name == 'nt':
        path_str = path_str.strip('"')

    path = Path(path_str)
    
    async def send(event):
        await websocket.send(True)

    event_handler = FileSystemEventHandler()
    event_handler.on_created = asyncio.run(send)
    event_handler.on_deleted = asyncio.run(send)
    event_handler.on_moved = asyncio.run(send)

    observer = Observer()
    observer.schedule(event_handler, path.as_posix(), recursive=True)
    observer.start()

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        observer.stop()
    observer.join()