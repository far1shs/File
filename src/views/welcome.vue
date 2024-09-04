<template>
  <div v-show="!local.getItem('initial')"
       style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <n-flex justify="center">
      <n-flex vertical>
        <div style="text-align: center">
          <h2>欢迎使用 Far1sh 的文件管理器</h2>
          <p>你需要完成初始设置</p>
        </div>
        <InputText v-model="apiName" style="width: 300px" placeholder="API 名称"/>
        <InputText v-model="apiPath" style="width: 300px" placeholder="API 地址"/>
        <InputText v-model="apiKey" style="width: 300px" placeholder="API KEY"/>
        <Button :loading="loading" @click="save" label="保存"/>
      </n-flex>
    </n-flex>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";
import {useMessage} from "naive-ui";
import {v4 as uuidv4} from "uuid";

const router = useRouter();
const message = useMessage();
const apiName = ref("");
const apiPath = ref("https://");
const apiKey = ref("");
const loading = ref(false);

const local = localStorage;

if (local.getItem("initial")) router.push("/");

function save() {
  if (!apiName.value || !apiPath.value || !apiKey.value) {
    message.error("我认为你需要填写完整");
    return;
  }
  
  loading.value = true;

  axios.get("/get_disk", {
    baseURL: apiPath.value,
    headers: {"X-API-KEY": apiKey.value}
  }).then((res) => {
    const id = uuidv4();
    local.setItem("initial", String(true));
    local.setItem("path", res.data.results[0].mountpoint);
    local.setItem("api", id);
    local.setItem("api_list", JSON.stringify([
      {id: id, name: apiName.value, path: apiPath.value, key: apiKey.value}
    ]));
    location.reload();
  }).catch(() => {
    message.error("出错了, 请查看 控制台 中发生的问题");
  }).finally(() => loading.value = false);
}

// const selectedCity = ref();
// const cities = ref([
//   {name: "zh-cn", code: "zh-cn"},
//   {name: "en-us", code: "en-us"},
//   {name: "ja-jp", code: "ja-jp"},
// ]);
</script>