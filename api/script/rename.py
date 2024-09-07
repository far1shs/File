from fastapi import Body, APIRouter
from fastapi.responses import JSONResponse
import os

app = APIRouter()


@app.post("/rename")
async def index(
    path: str = Body(..., embed=True), new_path: str = Body(..., embed=True)
):
    try:
        if not os.path.exists(path):
            return JSONResponse(
                status_code=404,
                content={"status": 404, "message": "path not found", "results": None},
            )

        if os.path.exists(new_path):
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "message": "new path already exists",
                    "results": None,
                },
            )
            
        new_path = os.path.join(os.path.dirname(path), new_path)

        os.rename(path, new_path)
        return JSONResponse(
            status_code=200,
            content={"status": 200, "message": "success", "results": new_path},
        )
    except PermissionError as e:
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
                "message": "file or directory is busy or locked",
                "results": None,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "server error", "results": str(e)},
        )
