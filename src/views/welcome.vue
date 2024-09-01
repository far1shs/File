<template>
  <div v-show="!local.getItem('initial')"
       style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <n-flex justify="center">
      <n-flex vertical>
        <div style="text-align: center">
          <h2>欢迎使用 Far1sh 的文件管理器</h2>
          <p>你需要完成初始设置</p>
        </div>
        <InputText v-model="apiName" style="width: 300px" type="text" placeholder="API 名字(怎么好听怎么来)"/>
        <InputText v-model="apiPath" style="width: 300px" type="text" placeholder="API 地址"/>
        <InputText v-model="apiKey" style="width: 300px" type="text" placeholder="API KEY"/>
        <!--        <Select disabled style="width: 300px" v-model="selectedCity" :options="cities" optionLabel="name"-->
        <!--                placeholder="语言 Language"/>-->
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
const apiPath = ref("");
const apiKey = ref("");
const loading = ref(false);

const local = localStorage;

if (local.getItem("initial")) router.push("/");

function save() {
  if (apiName.value === "" || apiName.value === null) {
    message.error("我认为你需要填写完整");
    return;
  }
  if (apiPath.value === "" || apiPath.value === null) {
    message.error("我认为你需要填写完整");
    return;
  }
  if (apiKey.value === "" || apiKey.value === null) {
    message.error("我认为你需要填写完整");
    return;
  }

  loading.value = true;

  axios.get("/get_disk", {
    baseURL: apiPath.value
  }).then((res) => {
    if (res.data.status === 200) {
      const id = uuidv4();
      local.setItem("initial", String(true));
      local.setItem("path", res.data.results[0].mountpoint);
      local.setItem("api", id);
      local.setItem("api_list", JSON.stringify([
        {id: id, name: apiName.value, path: apiPath.value, key: apiKey.value}
      ]));
      location.reload();
    } else {
      message.error("出错了, 请查看 控制台-网络 中 get_disk 请求发生的问题");
    }
  }).catch(() => {
    message.error("出错了, 请查看 控制台 中 发生的问题");
  }).finally(() => loading.value = false);
}

// const selectedCity = ref();
// const cities = ref([
//   {name: "zh-cn", code: "zh-cn"},
//   {name: "en-us", code: "en-us"},
//   {name: "ja-jp", code: "ja-jp"},
// ]);
</script>