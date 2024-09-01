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
              <span v-show="screenWidth < 750" @click="menuShow = true" style="cursor: pointer; display: flex; align-items: center;"><i
                  style="margin-right: 5px" class="pi pi-inbox"/>磁盘管理</span>
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
              style="position: fixed; background-color: white; width: 100%; z-index: 100; padding: 18px;">
            <div :style="screenWidth > 750 ? 'margin-right: 240px;' : ''" class="toolbar">
              <Button :disabled="loading" @click="back" severity="secondary" outlined icon="pi pi-angle-left"/>
              <Button :loading="loading" @click="refresh" severity="secondary" outlined icon="pi pi-refresh"/>
              <InputText v-model="path" @keydown.enter="getRess(path)" class="input-text"/>
              <Button severity="secondary" outlined icon="pi pi-bars"/>
            </div>
          </div>

          <div style="margin-top: 60px;">
            <div v-if="loading" style="margin-top: 25%">
              <n-flex vertical style="text-align: center;">
                <ProgressSpinner style="width: 50px; height: 50px;" strokeWidth="3" animationDuration=".8s"/>
              </n-flex>
            </div>

            <div v-else-if="ress.length === 0" style="margin-top: 24%; text-align: center">
              <i style="font-size: 48px" class="pi pi-trash"></i>
              <p>这里干净的就像是你的钱包</p>
            </div>

            <div v-else-if="error" style="margin-top: 24%; text-align: center">
              <i style="font-size: 48px" class="pi pi-times-circle"></i>
              <p>出错了, 请检查控制台(F12)-网络</p>
            </div>

            <div v-else>
              <r-list :list="ress"/>
            </div>
          </div>

          <n-drawer v-model:show="menuShow" placement="bottom" style="height: 100%; border: 0">
            <div style="margin: 10px 30px 0; display: flex; justify-content: space-between; align-items: center;">
                <span style="display: flex; align-items: center;"><i style="margin-right: 12px; font-size: 1.5em;"
                                                                     class="pi pi-inbox"></i>磁盘列表</span>
              <i @click="menuShow = false" style="font-size: 1.5em; cursor: pointer" class="pi pi-times"></i>
            </div>

            <Divider style="margin: 10px 0;" type="solid"/>
            <r-navigation-bar :list="disk"/>
          </n-drawer>
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
import {menuShow} from "../model/navigation.ts";
import {useMessage} from "naive-ui";

const router = useRouter();
const win = window;
const message = useMessage();

if (!localStorage.getItem("initial")) router.push("/welcome");

getDisk();

function refresh() {
  getRess(path.value);
}

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