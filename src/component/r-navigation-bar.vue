<template>
  <div class="side-navigation">
    <n-scrollbar>
      <ul class="menu">
        <li v-tooltip.bottom="{value: `可用空间: ${formatBytes(item.free)}\n已用空间: ${formatBytes(item.used)}\n总空间: ${formatBytes(item.total)}\n文件系统: ${item.fstype}`, showDelay: 800,}"
            @click="selectItem(item.device)" v-for="item in props.list" :key="item.device">
          <div class="icon-label">
            <i class="pi pi-inbox"></i>
            <n-flex :size="0" vertical class="flex-container">
              <div class="label-container">
                <span class="label">{{ item.device }}</span>
                <span class="label total-space">{{ formatBytes(item.total) }}</span>
              </div>
              <ProgressBar style="" class="progress-bar" :showValue="false" :value="item.percent"></ProgressBar>
            </n-flex>
          </div>
        </li>
      </ul>
    </n-scrollbar>
  </div>
</template>

<script setup lang="ts">
import {defineProps, Ref, ref} from "vue";
import {formatBytes} from "../script/tool.ts";
import {getRess} from "../script/action.ts";
import {menuShow} from "../model/navigation.ts";

const props = defineProps<{
  list?: any;
}>();

function selectItem(path: string) {
  getRess(path);
  menuShow.value = false;
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
  align-items: center;
  justify-content: flex-start;
  width: 100%;
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
  width: 100%;
}

.label-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.total-space {
  margin-left: auto;
}

.flex-container {
  width: 100%;
  margin-right: 15px;
}

.progress-bar {
  width: 100%;
  height: 7px;
}
</style>