from fastapi import APIRouter
import psutil
from fastapi.responses import JSONResponse

app = APIRouter()

@app.get("/get_disk")
async def index():
    disk_info = []
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError:
            continue
    
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": "success",
            "results": disk_info
        }
    )