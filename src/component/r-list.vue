<template>
  <div class="side-navigation">
    <n-scrollbar>
      <ul class="menu">
        <li @contextmenu="handleEllipsisClick($event, item)"
            @click="item.is_directory ? getRess(item.path) : ''"
            v-for="item in props.list" :key="item.path">
          <div class="icon-label">
            <i v-if="item.is_directory" class="pi pi-folder"></i>
            <i v-else class="pi pi-file"></i>
            <div style="width: 100%">
              <span class="label">{{ item.name }}</span>
            </div>
            <div style="margin-right: 8px">
              <div class="clickable-area" @click.stop="handleEllipsisClick($event, item)">
                <i style="margin-left: 12px" class="pi pi-ellipsis-h ellipsis-icon"/>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </n-scrollbar>
    <ContextMenu ref="menu" :model="items" @hide="item_data = null"/>
  </div>
</template>

<script setup lang="ts">
import {defineProps, ref} from "vue";
import {getRess, simpleRequest} from "../script/action.ts";
import {useMessage} from "naive-ui";
import axios from "axios";
import {path} from "../model";

const message = useMessage();
const props = defineProps<{
  list?: any;
}>();
const menu = ref();
const item_data = ref();
const items = ref([
  {
    label: "下载",
    icon: "pi pi-download",
    command: () => {
      window.open(`${axios.defaults.baseURL}/down_file?path=${item_data.value.path}`)
    }
  }, {
    separator: true
  }, {
    label: "新建",
    icon: "pi pi-plus",
    command: () => simpleRequest("/new_file", item_data.value.path, message)
  }, {
    label: "压缩",
    icon: "pi pi-bolt",
    command: () => simpleRequest("/zip_file", item_data.value.path, message)
  }, {
    label: "重命名",
    icon: "pi pi-pencil",
    command: () => simpleRequest("/edit_file", item_data.value.path, message)
  }, {
    label: "删除",
    icon: "pi pi-trash",
    command: () => {
      simpleRequest("/delete_file", item_data.value.path, message);
    }
  },
]);

function handleEllipsisClick(event: any, data: any) {
  item_data.value = data;
  menu.value.show(event);
}
</script>

<style scoped>
.side-navigation {
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.side-navigation li {
  width: 100%;
  height: 45px;
  display: flex;
  align-items: center;
  margin: 3px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, transform 0.1s ease;
  padding-left: 15px;
}

.side-navigation .icon-label {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
}

.side-navigation .icon-label i {
  font-size: 1.5em;
  color: black;
  margin-right: 12px;
}

.label {
  font-size: 1em;
  color: black;
  vertical-align: middle;
}

.side-navigation li:hover {
  background-color: #e9ecef;
}

.side-navigation li.active .icon-label i,
.side-navigation li.active .icon-label .label {
  color: white;
}

.menu {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.clickable-area {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  margin-left: auto;
}

.ellipsis-icon {
  font-size: 1.2em;
  color: black;
}
</style>