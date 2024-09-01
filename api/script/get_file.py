from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path


app = APIRouter()


@app.get("/get_file")
async def index(path: str):
    file_path = Path(path)
    if file_path.exists():
        content = file_path.read_text()
        return JSONResponse(
            status_code=200,
            content={"status": 200, "message": "success", "results": content},
        )


    else:
        return JSONResponse(
            status_code=401,
            content={"status": 401, "message": "file not found", "results": None},
        )
