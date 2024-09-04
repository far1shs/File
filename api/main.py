from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import model
from script import (
    delete,
    get_disk,
    get_ress,
    get_file,
    open_file,
    rename,
    upload_file,
    down_file,
    new_file,
    listen_file,
)


app = FastAPI(docs_url=None)
app.include_router(get_disk.app)
app.include_router(get_ress.app)
app.include_router(get_file.app)
app.include_router(open_file.app)
app.include_router(upload_file.app)
app.include_router(down_file.app)
app.include_router(new_file.app)
app.include_router(delete.app)
app.include_router(listen_file.app)
app.include_router(rename.app)


@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    args = model.args()

    if request.method == "OPTIONS":
        return await call_next(request)

    api_key_header = request.headers.get("X-API-KEY")
    api_key_url = request.query_params.get("api_key")
    if (
        str(api_key_header) != args["server"]["API_KEY"]
        and str(api_key_url) != args["server"]["API_KEY"]
    ):
        return JSONResponse(
            status_code=403,
            content={
                "status": 403,
                "message": "the key is incorrect",
                "results": args["server"]["API_KEY"],
            },
        )

    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

if __name__ == "__main__":
    args = model.args()
    uvicorn.run(
        app="main:app",
        host=args["server"]["host"],
        port=args["server"]["port"],
        reload=True,
    )
