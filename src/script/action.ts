import axios from "axios";
import {disk, editorContext, editorShow, error, path, ress, ressLoading} from "../model";
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
    localStorage.setItem("path", _path);
    path.value = _path;
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

export function simpleRequest(
    _path: string,
    file_path: string = "",
    message: MessageApiInjection,
    {
        request = true,
        click = () => {},
        dataObject = null,
        data = { path: file_path },
        resource = false
    }: {
        request?: Boolean,
        click?: (...args: any[]) => void,
        dataObject?: any,
        data?: any,
        resource?: boolean
    } = {}
): void {
    let messageReactive: MessageReactive | null = null;

    messageReactive = message.loading("加载中", {
        duration: 0
    });

    const req = axios.post(_path, data);
    req.then((res) => {
        message.success("成功");
        if (request) {
            getRess(path.value);
        }
        if (resource) {
            click(dataObject, res, /* 其他参数 */);
        } else {
            click(dataObject, /* 其他参数 */);
        }
    });
    req.catch((err) => {
        message.error(err.response.data.message);
    });
    req.finally(() => {
        if (messageReactive) {
            messageReactive.destroy();
            messageReactive = null;
        }
    });
}

export function editorRequest(path: string, message: MessageApiInjection) {
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

    const req = axios.post("/get_file", {
        "path": path
    })
    req.then((res) => {
        editorShow.value = true;
        editorContext.value = res.data.results;
    });
    req.catch((err) => {
        message.error(err.response.data.message);
    });
    req.finally(() => removeMessage());
}