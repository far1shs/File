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
                  style="margin-right: 5px" class="pi pi-github"/>GitHub</span>
              <span @click="router.push('/')" style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-arrow-left"/>返回</span>
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
            <p>更改API</p>
            <Select v-model="api" :options="apiList" option-label="name" option-value="id" placeholder="选择API"/>
            <Button label="管理"/>
            <p>本地打开(适合本地运行的API, 不使用在线编辑器, 预览等等, 类似一个web版本的资源管理器)</p>
            <ToggleSwitch @click="localOpenClick" v-model="localOpen"/>
            <p>监听文件变化(会有些资源损耗)</p>
            <ToggleSwitch @click="listenFileClick" v-model="listenFile"/>
            <Button @click="deleteLocalStorageShow = true" severity="danger" label="清空缓存"/>
          </n-flex>
        </n-flex>
      </n-scrollbar>

      <Dialog v-model:visible="deleteLocalStorageShow" modal header="清空缓存" :style="{ width: '25rem' }">
        <p>清空后, 您会重新进入欢迎页面, 您的数据不会有任何保留, API等等全部清空</p>

        <div style="float: right">
          <n-flex>
            <Button label="取消" severity="secondary" @click="deleteLocalStorageShow = false"></Button>
            <Button label="确定" severity="danger" @click="deleteLocalStorage"></Button>
          </n-flex>
        </div>
      </Dialog>
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import {ref} from "vue";

const router = useRouter();
const win = window;

const api = ref(localStorage.getItem("api"));
const apiList = ref(JSON.parse(String(localStorage.getItem("api_list"))));
const localOpen = ref(Boolean(localStorage.getItem("local_open")));
const listenFile = ref(Boolean(localStorage.getItem("listen_file")));
const deleteLocalStorageShow = ref(false);

if (!localStorage.getItem("initial")) router.push("/welcome");

function deleteLocalStorage() {
  deleteLocalStorageShow.value = false;
  localStorage.clear();
  location.reload();
}

function localOpenClick() {
  localStorage.setItem("local_open", String(!localOpen.value))
}

function listenFileClick() {
  localStorage.setItem("listen_file", String(!listenFile.value))
}
</script>

<style scoped>
p {
  margin: 0;
}
</style>