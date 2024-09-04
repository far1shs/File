from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pathlib import Path
import chardet


app = APIRouter()


@app.post("/get_file")
async def index(path: str = Body(..., embed=True)):
    try:
        file_path = Path(path)
        if file_path.exists():
            try:
                with open(file_path, "rb") as f:
                    raw_data = f.read()

                result = chardet.detect(raw_data)
                encoding = result["encoding"]
                
                content = file_path.read_text(encoding)
                return JSONResponse(
                    status_code=200,
                    content={"status": 200, "message": "success", "results": content},
                )
            except PermissionError:
                return JSONResponse(
                    status_code=403,
                    content={
                        "status": 403,
                        "message": "there are no permissions",
                        "results": None,
                    },
                )
            except IOError as e:
                return JSONResponse(
                    status_code=409,
                    content={
                        "status": 409,
                        "message": "file is busy or locked",
                        "results": None,
                    },
                )
        else:
            return JSONResponse(
                status_code=404,
                content={"status": 404, "message": "file not found", "results": None},
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "server error", "results": str(e)},
        )
