import os
import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse

app = APIRouter()


def custom_sort_key(item):
    name = item["name"]
    is_directory = item["is_directory"]
    try:
        num_part = int(name)
    except ValueError:
        num_part = float("inf")
    return (not is_directory, num_part, name)


@app.get("/get_ress")
async def index(path: str):
    file_info_list = []

    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            is_directory = os.path.isdir(item_path)
            item_info = {
                "name": item,
                "path": item_path,
                "is_directory": is_directory,
                "type": os.path.splitext(item)[1] if not is_directory else None,
                "size": os.path.getsize(item_path) if not is_directory else None,
                "modified_date": time.ctime(os.path.getmtime(item_path)),
            }
            file_info_list.append(item_info)
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"status": 500, "message": str(e), "results": None}
        )

    # 按自定义顺序排序
    sorted_file_info_list = sorted(file_info_list, key=custom_sort_key)

    return JSONResponse(
        status_code=200,
        content={"status": 200, "message": "success", "results": sorted_file_info_list},
    )
