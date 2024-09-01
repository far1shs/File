<template>
  <div class="side-navigation">
    <n-scrollbar>
      <ul class="menu">
        <li @click="getRess(item.device)" v-for="item in list">
          <div v-tooltip.bottom="{value: `可用空间: ${formatBytes(item.free)}\n已用空间: ${formatBytes(item.used)}\n总空间: ${formatBytes(item.total)}`, showDelay: 800,}" class="icon-label">
            <i class="pi pi-inbox"></i>
            <n-flex :size="0" vertical>
              <div>
                <span class="label">{{ item.device }}</span>
                <span style="float: right; margin-top: 0" class="label">{{ formatBytes(item.total) }}</span>
              </div>
              <ProgressBar style="height: 7px; width: 145px" :showValue="false" :value="item.percent"></ProgressBar>
            </n-flex>
          </div>
        </li>
      </ul>
    </n-scrollbar>
  </div>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import {defineProps} from "vue";
import {formatBytes} from "../script/tool.ts";
import {getRess} from "../script/action.ts";

const router = useRouter();

const props = defineProps<{
  list?: any;
}>();
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

.side-navigation li:active {
  transform: scale(0.98);
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
