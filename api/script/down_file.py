from urllib import parse
import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse

app = APIRouter()

@app.get("/down_file")
async def download_file(path: str = Query(..., description="Path to the file")):
    try:
        full_path = os.path.join("files", parse.unquote(path))

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="File not found")

        # 返回文件响应
        return FileResponse(
            full_path,
            media_type="application/octet-stream",
            filename=os.path.basename(full_path),
        )
    except HTTPException as e:
        # 捕获并返回 HTTP 异常
        return JSONResponse(
            status_code=e.status_code,
            content={"code": e.status_code, "message": e.detail, "results": None},
        )
    except Exception as e:
        # 捕获其他异常并返回服务器错误
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "Server error", "results": str(e)},
        )