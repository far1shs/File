import os
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

app = APIRouter()


@app.post("/new_file")
async def index(path: str = Body(..., embed=True), name: str = Body(..., embed=True)):
    try:
        path = os.path.join(path, name)
        if not os.path.exists(path):
            with open(path, "w"):
                pass
        else:
            return JSONResponse(
                status_code=400,
                content={"status": 500, "message": "file already exists", "results": None},
            )
        return JSONResponse(
            status_code=200,
            content={"status": 200, "message": "success", "results": None},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "server error", "results": str(e)},
        )
