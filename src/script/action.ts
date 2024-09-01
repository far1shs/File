import axios from "axios";
import {disk, error, ressLoading, ress, path} from "../model";
import {MessageApiInjection} from "naive-ui/es/message/src/MessageProvider";
import {MessageReactive} from "naive-ui/lib";

export function getDisk() {
    const req = axios.get(`/get_disk`)
    req.then((res) => {
        disk.value = res.data.results;
        getRess(String(localStorage.getItem("path")));
    });
    req.catch(() => {

    });
    req.finally(() => ressLoading.value = false);
}

export function getRess(_path: string) {
    ressLoading.value = true;
    path.value = _path;
    localStorage.setItem("path", _path);
    error.value = false;
    const req = axios.post("/get_ress", {
        "path": _path
    })
    req.then((res) => {
        ress.value = res.data.results;
    });
    req.catch(() => {
        error.value = true;
    });
    req.finally(() => ressLoading.value = false);
}


export function simpleRequest(_path: string, file_path: string, message: MessageApiInjection) {
    let messageReactive: MessageReactive | null = null

    if (!messageReactive) {
        messageReactive = message.loading("加载中", {
            duration: 0
        })
    }

    function removeMessage() {
        if (messageReactive) {
            messageReactive.destroy()
            messageReactive = null
        }
    }

    const req = axios.post(_path, {
        "path": file_path
    })
    req.then(() => {
        message.success("成功");
        getRess(path.value);
    });
    req.catch((err) => {
        message.error(err.response.data.message);
    });
    req.finally(() => removeMessage())
}