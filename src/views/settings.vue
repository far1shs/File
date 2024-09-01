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
              <span @click="win.open('https://github.com/far1shs/File')" style="cursor: pointer; display: flex; align-items: center;"><i
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
        <n-flex vertical style="margin: 20px; width: 300px">
          <p>您的所有设置都会存储到本地 (localStorage)</p>
          <p>更改API</p>
          <Select v-model="selectedCity" :options="cities" optionLabel="name" placeholder="选择API" class="w-full md:w-56" />
          <Button label="管理"/>
        </n-flex>
      </n-scrollbar>
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import { ref } from "vue";

const router = useRouter();
const win = window;

const selectedCity = ref();
const cities = ref([
  { name: 'New York', code: 'NY' },
  { name: 'Rome', code: 'RM' },
  { name: 'London', code: 'LDN' },
  { name: 'Istanbul', code: 'IST' },
  { name: 'Paris', code: 'PRS' }
]);
</script>

<style scoped>
p {
  margin: 0;
}
</style>