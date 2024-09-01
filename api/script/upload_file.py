from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import JSONResponse
import os

app = APIRouter()


@app.post("/upload_file")
async def index(
    file: UploadFile = File(...), save_path: str = Query(..., description="保存路径")
):
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = os.path.join(save_path, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return JSONResponse(
            status_code=200,
            content={"status": 200, "message": "success", "results": file_path},
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
