import axios from "axios";
import {disk, error, loading, ress, path} from "../model";

export function getDisk() {
    const req = axios.get(`/get_disk`)
    req.then((res) => {
        disk.value = res.data.results;
        getRess(String(localStorage.getItem("path")));
    });
    req.catch(() => {
        
    });
    req.finally(() => loading.value = false);
}

export function getRess(_path: string) {
    loading.value = true;
    path.value = _path;
    localStorage.setItem("path", _path);
    error.value = false;
    const req = axios.get(`/get_ress?path=${_path}`)
    req.then((res) => {
        ress.value = res.data.results;
    });
    req.catch(() => {
        error.value = true;
    });
    req.finally(() => loading.value = false);
}