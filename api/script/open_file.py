from fastapi import Body, APIRouter
from fastapi.responses import JSONResponse
import os

app = APIRouter()


@app.post("/open_file")
async def index(path: str = Body(..., embed=True)):
    try:
        os.startfile(path)
        return JSONResponse(
            status_code=200,
            content={"status": 200, "message": "success", "results": None},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "error", "results": str(e)},
        )
