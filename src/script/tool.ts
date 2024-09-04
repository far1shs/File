import axios from "axios";
import {ressLoading} from "../model";
import {MessageApiInjection} from "naive-ui/es/message/src/MessageProvider";
import {MessageReactive} from "naive-ui/lib";

export function formatBytes(bytes: number, decimals: number = 2): string {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export interface Item {
    id: string;
    name: string;
    path: string;
    key: string;
}

export function getApiListItem(id: string, data: any): Item | undefined {
    return data.find((item: Item) => item.id === id);
}

export function toggleApi(id: string, message: MessageApiInjection) {
    let messageReactive: MessageReactive | null = null

    messageReactive = message.loading("切换并拉取配置", {
        duration: 0
    })

    const api = getApiListItem(id, JSON.parse(String(localStorage.getItem("api_list"))));
    const req = axios.get("/get_disk", {
        baseURL: api?.path,
        headers: {
            "X-API-KEY": api?.key
        }
    })
    req.then((res) => {
        localStorage.setItem("path", res.data.results[0].mountpoint);
        localStorage.setItem("api", id);
        location.reload();
    });
    req.catch(() => {
        message.error("切换失败, API错误请检查 控制台-网络");
    });
    req.finally(() => {
        ressLoading.value = false;
        if (messageReactive) {
            messageReactive.destroy()
            messageReactive = null
        }
    });
}