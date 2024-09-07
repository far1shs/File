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
              <span @click="toggleApiCard($event)" style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-server"/>
                {{ screenWidth < 750 ? "" : apiList?.name }}
              </span>
              <span v-show="screenWidth < 750" @click="menuShow = true"
                    style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-inbox"/></span>
              <span @click="router.push('/settings')" style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-cog"/>{{ screenWidth < 750 ? "" : "设置" }}</span>
            </n-flex>
          </b>
        </template>
      </Menubar>
    </n-layout-header>
    <n-layout style="margin-top: 40px" position="absolute" has-sider>
      <n-layout-sider v-show="screenWidth > 750" bordered :native-scrollbar="false" :width="240">
        <r-navigation-bar :list="disk"/>
      </n-layout-sider>

      <n-layout-content>
        <n-layout position="absolute">
          <n-layout-header position="absolute" style="height: 74px">
            <div
                style="position: fixed; background-color: white; width: 100%; z-index: 100; padding: 18px; border-bottom: 1px solid #E2E8F0">
              <div :style="screenWidth > 750 ? 'margin-right: 240px;' : ''" class="toolbar">
                <Button :disabled="ressLoading" @click="back" severity="secondary" outlined icon="pi pi-angle-left"/>
                <Button :loading="ressLoading" @click="getRess(path)" severity="secondary" outlined
                        icon="pi pi-refresh"/>
                <InputText v-model="path" @keydown.enter="getRess(path)" class="input-text"/>
                <Button @click="toggleMenuCard($event)" severity="secondary" outlined icon="pi pi-bars"/>
              </div>
            </div>
          </n-layout-header>

          <n-layout position="absolute" :native-scrollbar="false" style="margin-top: 74px">
            <div v-if="ressLoading" style="margin-top: 21%">
              <n-flex vertical style="text-align: center;">
                <ProgressSpinner style="width: 50px; height: 50px;" strokeWidth="3" animationDuration=".8s"/>
              </n-flex>
            </div>

            <div v-else-if="ress.length === 0" style="margin-top: 20%; text-align: center">
              <i style="font-size: 48px" class="pi pi-trash"></i>
              <p>这里干净的就像是你的钱包</p>
            </div>

            <div v-else-if="error" style="margin-top: 20%; text-align: center">
              <i style="font-size: 48px" class="pi pi-times-circle"></i>
              <p>出错了, 请检查控制台(F12)-网络</p>
            </div>

            <r-list v-else :list="ress"/>
          </n-layout>
        </n-layout>

        <n-drawer v-model:show="menuShow" placement="bottom" height="100%">
          <div style="margin: 10px 30px 0; display: flex; justify-content: space-between; align-items: center;">
                <span style="display: flex; align-items: center;">
                  <i style="margin-right: 12px; font-size: 1.5em;" class="pi pi-inbox"></i>磁盘列表
                </span>
            <i @click="menuShow = false" style="font-size: 1.5em; cursor: pointer" class="pi pi-times"></i>
          </div>

          <Divider style="margin: 10px 0;" type="solid"/>

          <r-navigation-bar :list="disk"/>
        </n-drawer>

        <n-drawer v-model:show="editorShow" height="100%" placement="bottom" :close-on-esc="false">
          <n-layout position="absolute">
            <n-layout-header position="absolute" style="height: 44px">
              <div style="margin: 10px 30px 0; display: flex; justify-content: space-between; align-items: center;">
                <span style="display: flex; align-items: center;">
                  <i style="margin-right: 12px; font-size: 1.5em;" class="pi pi-file-edit"></i>编辑
                </span>
                <i @click="editorShow = false" style="font-size: 1.5em; cursor: pointer" class="pi pi-times"></i>
              </div>
            </n-layout-header>

            <div style="height: 100%; display: flex; flex-direction: column; margin-top: 44px">
              <div style="flex: 1; margin-bottom: 44px;">
                <MonacoEditor
                    style="width: 100%; height: 100%"
                    theme="vs"
                    :options="editorOptions"
                    language="json"
                    v-model:value="editorContext"
                ></MonacoEditor>
              </div>
            </div>
          </n-layout>
        </n-drawer>

        <Menu style="padding: 5px" :popup="true" ref="apiCard" :model="apiLists">
          <template #item="{ item, props }">
            <a @click="toggleApi(item.id, message)" class="flex items-center" v-bind="props.action">
              <span>{{ item.name }}</span>
            </a>
          </template>
        </Menu>

        <Menu style="padding: 5px" :popup="true" ref="menuCard" :model="menuLists" />

        <Dialog v-model:visible="uploadFileShow" modal header="上传文件" :style="{ width: '25rem' }">
          <n-upload
              :multiple="true"
              directory-dnd
              :action="`${axios.defaults.baseURL}/upload_file`"
              :headers="{'X-API-KEY': axios.defaults.headers['X-API-KEY']}"
              :data="{save_path: path}"
              :show-remove-button="false"
              v-on:finish="getRess(path)"
          >
            <n-upload-dragger style="height: 200px">
              <n-flex style="margin-top: 28px" vertical>
                <div>
                  <i style="font-size: 48px" class="pi pi-upload"></i>
                </div>
                <n-text style="font-size: 16px">
                  点击或者拖动文件到该区域来上传
                </n-text>
              </n-flex>
            </n-upload-dragger>
          </n-upload>
        </Dialog>

        <ContextMenu ref="menu" :model="items"/>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import {screenWidth} from "../script/screen.ts";
import RNavigationBar from "../component/r-navigation-bar.vue";
import RList from "../component/r-list.vue";
import {apiList, disk, editorContext, editorShow, error, path, ress, ressLoading} from "../model";
import {getDisk, getRess} from "../script/action.ts";
import {menuShow} from "../model/navigation.ts";
import {ref} from "vue";
import axios from "axios";
import {toggleApi} from "../script/tool.ts";
import {useMessage} from "naive-ui";
import MonacoEditor from "monaco-editor-vue3";

const router = useRouter();
const win = window;
const local = localStorage;
const message = useMessage();

const apiCard = ref();
const apiLists = ref(JSON.parse(String(localStorage.getItem("api_list"))));
const menuCard = ref();
const menuLists = [
  {
    label: "属性",
    icon: "pi pi-info-circle",
  }
]
const uploadFileShow = ref(false);
const menu = ref();
const items = ref([
  {
    label: "上传",
    icon: "pi pi-upload",
    command: () => uploadFileShow.value = true
  }, {
    label: "多选",
    icon: "pi pi-expand",
    command: () => uploadFileShow.value = true
  }
]);

const editorOptions = {
  colorDecorators: true,
  lineHeight: 24,
  tabSize: 2,
  scrollBeyondLastLine: false,
  minimap: {
    enabled: false
  }
}

if (!local.getItem("initial")) router.push("/welcome");

getDisk();

function back() {
  if (path.value.includes('\\')) {
    const parts = path.value.split('\\');
    if (parts.length > 2) {
      parts.pop();
      path.value = parts.join('\\');
    } else {
      path.value = parts[0] + '\\';
    }
  } else {
    const parts = path.value.split('/');
    if (parts.length > 2) {
      parts.pop();
      path.value = parts.join('/');
    } else {
      path.value = '/';
    }
  }
  getRess(path.value);
}

function toggleApiCard(event: Event) {
  apiCard.value.toggle(event);
}

function toggleMenuCard(event: Event) {
  menuCard.value.toggle(event);
}
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-text {
  flex: 1;
}
</style>