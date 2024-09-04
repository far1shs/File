import os
from fastapi import APIRouter, Body
from fastapi.responses import FileResponse, JSONResponse

app = APIRouter()


@app.post("/down_file")
async def index(path: str = Body(..., embed=True)):
    try:
        path = os.path.join("files", path)

        if not os.path.exists(path):
            return JSONResponse(
                status_code=404,
                content={"code": 404, "message": "file not found", "results": None},
            )

        return FileResponse(
            path,
            media_type="application/octet-stream",
            filename=os.path.basename(path),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "server error", "results": str(e)},
        )
