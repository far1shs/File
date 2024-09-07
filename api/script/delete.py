import shutil
from fastapi import Body, APIRouter
from fastapi.responses import JSONResponse
import os

app = APIRouter()


@app.post("/delete")
async def index(path: str = Body(..., embed=True)):
    try:
        if os.path.isfile(path):
            os.remove(path)
            return JSONResponse(
                status_code=200,
                content={"status": 200, "message": "file deleted successfully", "results": None},
            )
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return JSONResponse(
                status_code=200,
                content={"status": 200, "message": "directory deleted successfully", "results": None},
            )
        else:
            return JSONResponse(
                status_code=404,
                content={"status": 404, "message": "path not found", "results": None},
            )
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"status": 404, "message": "path not found", "results": None},
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
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "server error", "results": str(e)},
        )
