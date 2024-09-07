<template>
  <div class="side-navigation">
    <n-scrollbar>
      <ul class="menu">
        <li v-tooltip.bottom="{value: `可用空间: ${formatBytes(item.free)}\n已用空间: ${formatBytes(item.used)}\n总空间: ${formatBytes(item.total)}\n文件系统: ${item.fstype}`, showDelay: 800,}"
            @click="selectItem(item.mountpoint)"
            v-for="(item, index) in props.list"
            :style="{ animationDelay: `${index * 0.05}s` }">
          <div class="icon-label">
            <svg style="width: 38px; height: 38px; margin-right: 10px" t="1725454170586" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5295" width="200" height="200"><path d="M945.984 513.984c9.344 12.032 14.016 25.536 14.016 40.512v205.504c0 19.968-7.232 36.992-21.76 51.008a73.408 73.408 0 0 1-52.928 20.992H138.688c-20.736 0-38.4-7.04-52.928-20.992a68.224 68.224 0 0 1-21.76-51.008v-205.44c0-15.04 4.672-28.544 14.016-40.576L241.28 287.488a63.04 63.04 0 0 1 25.6-23.232C277.952 258.752 289.6 256 302.08 256h419.968c12.48 0 24.128 2.752 35.008 8.256 10.88 5.504 19.456 13.248 25.664 23.232l163.328 226.56zM302.08 328L180.672 496h662.656l-121.344-168H302.08z m583.296 432v-192H138.688v192h746.624z m-49.728-96a45.312 45.312 0 0 1-14.784 33.728 48.704 48.704 0 0 1-35.008 14.272 48.704 48.704 0 0 1-35.008-14.272 45.312 45.312 0 0 1-14.784-33.728c0-12.992 4.928-24.256 14.72-33.728a48.704 48.704 0 0 1 35.072-14.272c13.44 0 25.152 4.736 35.008 14.272 9.856 9.472 14.72 20.736 14.72 33.728z m-149.376 0a45.312 45.312 0 0 1-14.72 33.728 48.704 48.704 0 0 1-35.072 14.272 48.704 48.704 0 0 1-34.944-14.272 45.312 45.312 0 0 1-14.784-33.728c0-12.992 4.928-24.256 14.72-33.728a48.704 48.704 0 0 1 35.008-14.272c13.504 0 25.152 4.736 35.008 14.272 9.856 9.472 14.784 20.736 14.784 33.728z" fill="#2c2c2c" p-id="5296"></path></svg>
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
import {defineProps} from "vue";
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
  transform: translateY(50px);
  animation: fadeInUp 0.5s forwards;
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
  margin-top: -2px;
  margin-right: 15px;
}

.progress-bar {
  width: 100%;
  height: 7px;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>