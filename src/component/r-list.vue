<template>
  <div class="side-navigation">
    <n-scrollbar>
      <ul class="menu">
        <li @contextmenu="onImageRightClick" @click="item.is_directory ? getRess(item.path) : ''" v-for="item in props.list" :key="item.path">
          <div class="icon-label">
            <i v-if="item.is_directory" class="pi pi-folder"></i>
            <i v-else class="pi pi-file"></i>
            <div style="width: 100vh">
              <span class="label">{{ item.name }}</span>
            </div>
          </div>
        </li>
      </ul>
    </n-scrollbar>
    <ContextMenu ref="menu" :model="items" />
  </div>
</template>

<script setup lang="ts">
import {defineProps, ref} from "vue";
import {getRess} from "../script/action.ts";
import {path} from "../model";

const props = defineProps<{
  list?: any;
}>();
const menu = ref();
const items = ref([
  { label: 'Copy', icon: 'pi pi-copy' },
  { label: 'Rename', icon: 'pi pi-file-edit' }
]);

const onImageRightClick = (event) => {
  menu.value.show(event);
};
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
  align-items: center;
  justify-content: flex-start;
}

.side-navigation .icon-label i {
  font-size: 1.5em;
  color: black;
  margin-right: 12px; /* 图标和标签之间的间距 */
}

.side-navigation .icon-label .label {
  margin-top: 2px;
  font-size: 1em;
  color: black;
}

.side-navigation .icon-label .progress {
  border: 0;
}

.side-navigation li:hover {
  background-color: #e9ecef;
}

.side-navigation li.active {
  background-color: black;
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
</style>

