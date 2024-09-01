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
              <span @click="router.push('/settings')" style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-cog"/>设置</span>
            </n-flex>
          </b>
        </template>
      </Menubar>
    </n-layout-header>
    <n-layout style="margin-top: 40px" position="absolute" has-sider>
      <n-layout-sider v-show="screenWidth > 750" bordered :native-scrollbar="false" :width="240">
        <r-navigation-bar :list="disk"/>
      </n-layout-sider>
      <n-layout>
        <n-layout-content>
          <div
              style="position: fixed;  background-color: white; width: 100%; z-index: 100; padding: 18px;">
            <n-flex>
              <Button @click="back" severity="secondary" outlined icon="pi pi-angle-left"/>
              <Button @click="refresh" severity="secondary" outlined icon="pi pi-refresh"/>
              <InputText v-model="path" @keydown.enter="getRess(path)"/>
            </n-flex>
          </div>

          <div style="margin-top: 60px;">
            <div v-if="loading" style="margin-top: 25%">
              <n-flex vertical style="text-align: center;">
                <ProgressSpinner style="width: 50px; height: 50px;" strokeWidth="3" animationDuration=".8s"/>
              </n-flex>
            </div>

            <div v-else-if="error" style="margin-top: 24%; text-align: center">
              <i style="font-size: 48px" class="pi pi-times-circle"></i>
              <p>出错了, 请检查控制台(F12)-网络</p>
            </div>

            <div v-else>
              <r-list :list="ress"/>
            </div>
          </div>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import {screenWidth} from "../script/screen.ts";
import RNavigationBar from "../component/r-navigation-bar.vue";
import RList from "../component/r-list.vue";
import {path, disk, ress, loading, error} from "../model";
import {getDisk, getRess} from "../script/action.ts";

const router = useRouter();
const win = window;

if (!localStorage.getItem("initial")) router.push("/welcome");

getDisk();

function refresh() {
  getRess(path.value);
}

function back() {
  if (path.value.includes('\\')) {
    // Windows 路径处理
    const parts = path.value.split('\\');
    if (parts.length > 2) {
      parts.pop();
      path.value = parts.join('\\');
    } else {
      path.value = parts[0] + '\\';
    }
  } else {
    // Linux 路径处理
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
</script>