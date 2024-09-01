from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from script import get_disk, get_ress, get_file, open_file, upload_file, down_file, new_file, delete_file

API_KEY = "awaqwqwww"
app = FastAPI(docs_url=None)

app.include_router(get_disk.app)
app.include_router(get_ress.app)
app.include_router(get_file.app)
app.include_router(open_file.app)
app.include_router(upload_file.app)
app.include_router(down_file.app)
app.include_router(new_file.app)
app.include_router(delete_file.app)

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        return JSONResponse(
            status_code=403,
            content={"status": 403, "message": "the key is incorrect", "results": None},
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
    uvicorn.run(app="main:app", host="0.0.0.0", port=1244, reload=True)
