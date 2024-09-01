<template>
  <n-config-provider :theme="null" :theme-overrides="themeColor">
    <n-loading-bar-provider>
      <n-message-provider>
        <router-view />
      </n-message-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
const themeColor = {
  common: {
    primaryColor: "#000000",
    primaryColorHover: "#000000",
    primaryColorPressed: "#000000",
    primaryColorSuppl: "#000000",
    borderRadius: "5px"
  },
  Layout: {
    headerBorderColor: "#E2E8F0",
    siderBorderColor: "#E2E8F0",
  },
  Card: {
    titleFontWeight: 1000,
    borderColor: "#E2E8F0"
  },
  List: {
    colorHover: "#e9ecef"
  }
}
</script>

<style scoped>
:root {
  --border-radius: 2px;
}
</style>