from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from script import get_disk, get_ress, get_file, open_file, upload_file

app = FastAPI(docs_url=None)

app.include_router(get_disk.app)
app.include_router(get_ress.app)
app.include_router(get_file.app)
app.include_router(open_file.app)
app.include_router(upload_file.app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=1244, reload=True)
