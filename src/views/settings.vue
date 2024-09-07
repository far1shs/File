<template>
  <n-layout position="absolute">
    <n-layout-header position="absolute">
      <Menubar style="border: none; border-bottom: 1px solid #E2E8F0; border-radius: 0; height: 40px">
        <template #start>
          <b>
            <span @click="router.push('/')" style="cursor: pointer">Far1sh File</span>
          </b>
        </template>
        <template #end>
          <b>
            <n-flex>
              <span @click="win.open('https://github.com/far1shs/File')"
                    style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-github"/>{{ screenWidth < 750 ? "" : "GitHub" }}</span>
              <span @click="router.push('/')" style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-arrow-left"/>{{ screenWidth < 750 ? "" : "返回" }}</span>
            </n-flex>
          </b>
        </template>
      </Menubar>
    </n-layout-header>
    <n-layout-content style="margin-top: 40px">
      <n-scrollbar>
        <n-flex justify="center">
          <n-flex vertical style="margin: 20px; width: 300px">
            <p>您的所有设置都会存储到本地 (localStorage)</p>
            <p>更改API (管理当前API)</p>
            <Select @change="toggleApi(String(api), message)" v-model="api" :options="apiList" option-label="name" option-value="id" placeholder="选择API"/>
            <Button @click="toggleManageCard($event)" label="管理"/>
            <p>版本更新对话框</p>
            <ToggleSwitch @click="toggle('update_dialog', !updateDialog)" v-model="updateDialog"/>
            <p>本地打开(适合本地运行的API, 不使用在线编辑器, 预览等等, 类似一个web版本的资源管理器)</p>
            <ToggleSwitch @click="toggle('local_open', !localOpen)" v-model="localOpen"/>
            <p>监听文件变化(会有些资源损耗)</p>
            <ToggleSwitch @click="toggle('listen_file', !listenFile)" v-model="listenFile"/>
            <p>删除文件对话框(不推荐关闭)</p>
            <ToggleSwitch @click="toggle('delete_dialog', !deleteDialog)" v-model="deleteDialog"/>
            <p style="color: grey; text-align: center">Panel: v0.0.1 API: 0.0.1 Develop Far1sh</p>
            <Button @click="deleteLocalStorageShow = true" severity="danger" label="清空缓存"/>
          </n-flex>
        </n-flex>
      </n-scrollbar>

      <Dialog v-model:visible="addApi.show" modal header="添加API" style="width: 350px">
        <n-flex vertical>
          <InputText v-model="addApi.name" style="width: 100%" placeholder="API 名称"/>
          <InputText v-model="addApi.path" style="width: 100%" placeholder="API 地址"/>
          <InputText v-model="addApi.key" style="width: 100%" placeholder="API KEY"/>
        </n-flex>

        <div style="margin-top: 20px">
          <n-grid :cols="2" :x-gap="12">
            <n-gi>
              <Button style="width: 100%" label="取消" severity="secondary" @click="addApi.show = false"></Button>
            </n-gi>
            <n-gi>
              <Button :loading="addApi.loading" style="width: 100%" label="确定" @click="addApiClick"></Button>
            </n-gi>
          </n-grid>
        </div>
      </Dialog>

      <Dialog v-model:visible="deleteLocalStorageShow" modal header="清空缓存" style="width: 350px">
        <p>清空后, 您会重新进入欢迎页面, 您的数据不会有任何保留, API等等全部清空</p>

        <div style="margin-top: 20px">
          <n-grid :cols="2" :x-gap="12">
            <n-gi>
              <Button style="width: 100%" label="取消" severity="secondary" @click="deleteLocalStorageShow = false"></Button>
            </n-gi>
            <n-gi>
              <Button style="width: 100%" label="确定" @click="deleteLocalStorage"></Button>
            </n-gi>
          </n-grid>
        </div>
      </Dialog>

      <Popover :unstyled="true" ref="manageCard">
        <n-card style="width: 300px; margin-top: 2px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)" size="small">
          <n-flex vertical>
            <Button @click="addApi.show = true" label="添加"/>
            <Button label="修改"/>
            <Button :disabled="apiList.length >= 1" severity="danger" label="删除"/>
          </n-flex>
        </n-card>
      </Popover>
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import {ref} from "vue";
import {screenWidth} from "../script/screen.ts";
import axios from "axios";
import {v4 as uuidv4} from "uuid";
import {useMessage} from "naive-ui";
import {toggleApi} from "../script/tool.ts";

const router = useRouter();
const win = window;
const manageCard = ref();
const message = useMessage();

const api = ref(localStorage.getItem("api"));
const apiList = ref(JSON.parse(String(localStorage.getItem("api_list"))));
const updateDialog = ref(Boolean(localStorage.getItem("update_dialog")));
const localOpen = ref(Boolean(localStorage.getItem("local_open")));
const listenFile = ref(Boolean(localStorage.getItem("listen_file")));
const deleteDialog = ref(Boolean(localStorage.getItem("delete_dialog")));

const addApi = ref({
  show: false,
  name: "",
  path: "https://",
  key: "",
  loading: false
});
const deleteLocalStorageShow = ref(false);

if (!localStorage.getItem("initial")) router.push("/welcome");

function addApiClick() {
  if (!addApi.value.name || !addApi.value.path || !addApi.value.key) {
    message.error("我认为你需要填写完整");
    return;
  }

  addApi.value.loading = true;

  axios.get("/get_disk", {
    baseURL: addApi.value.path,
    headers: {"X-API-KEY": addApi.value.key}
  }).then(() => {
    const id = uuidv4();
    
    const apiListJson = JSON.parse(String(localStorage.getItem("api_list")));
    apiListJson.push({id: id, name: addApi.value.name, path: addApi.value.path, key: addApi.value.key});
    localStorage.setItem("api_list", JSON.stringify(apiListJson));

    addApi.value.show = false;
    addApi.value.name = "";
    addApi.value.path = "https://";
    addApi.value.key = "";

    location.reload();
  }).catch(() => {
    message.error("出错了, 请查看 控制台 中发生的问题");
  }).finally(() => addApi.value.loading = false);
}

function deleteLocalStorage() {
  deleteLocalStorageShow.value = false;
  localStorage.clear();
  location.reload();
}

function toggleManageCard(event: Event) {
  manageCard.value.toggle(event);
}

function toggle(key: string, value: boolean) {
  localStorage.setItem(key, String(value));
}
</script>

<style scoped>
p {
  margin: 0;
}
</style>