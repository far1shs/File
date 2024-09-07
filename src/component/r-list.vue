<template>
  <div class="side-navigation">
    <n-scrollbar>
      <ul class="menu">
        <!--:class="{'active': isSelected(item)}"-->
        <li @contextmenu="menuClick($event, item)"
            @click="item.is_directory ? getRess(item.path) : editorRequest(item.path, message)"
            v-for="(item, index) in props.list" :key="item.path"
            :style="{ animationDelay: `${index * 0.05}s` }"
            :class="{'animated': isAnimated(index)}">
          <div class="icon-label">
            <i v-if="item.is_directory" class="pi pi-folder"></i>
            <i v-else-if="isImageFile(item.type)" class="pi pi-image"></i>
            <i v-else-if="isZipFile(item.type)" class="pi pi-box"></i>
            <i v-else class="pi pi-file"></i>
            <div style="width: 100%">
              <span class="label">{{ item.name }}</span>
            </div>
            <div style="margin-right: 8px; display: flex; align-items: center;">
              <span v-if="!item.is_directory" class="file-size">{{ formatBytes(item.size) }}</span>
              <div class="clickable-area" @click.stop="menuClick($event, item)">
                <i style="margin-left: 12px" class="pi pi-ellipsis-h ellipsis-icon"/>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </n-scrollbar>

    <ContextMenu ref="menu" :model="items" @hide="dataObjectTemp = null"/>

    <Dialog v-model:visible="newFileShow" modal header="新建文件" style="width: 350px">
      <InputText v-model="newFileName" style="width: 100%" placeholder="输入文件名"/>

      <div style="margin-top: 20px">
        <n-grid :cols="2" :x-gap="12">
          <n-gi>
            <Button style="width: 100%" label="取消" severity="secondary" @click="newFileShow = false"></Button>
          </n-gi>
          <n-gi>
            <Button style="width: 100%" label="确定" @click="newFile"></Button>
          </n-gi>
        </n-grid>
      </div>
    </Dialog>

    <Dialog v-model:visible="renameFileShow" modal header="重命名" style="width: 350px">
      <InputText v-model="dataObject.name" style="width: 100%" placeholder="输入新名称"/>

      <div style="margin-top: 20px">
        <n-grid :cols="2" :x-gap="12">
          <n-gi>
            <Button style="width: 100%" label="取消" severity="secondary" @click="renameFileShow = false"></Button>
          </n-gi>
          <n-gi>
            <Button style="width: 100%" label="确定" @click="renameFile"></Button>
          </n-gi>
        </n-grid>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import {defineProps, ref} from "vue";
import {editorRequest, getRess, simpleRequest} from "../script/action.ts";
import {useMessage} from "naive-ui";
import axios from "axios";
import {formatBytes} from "../script/tool.ts";
import {path, ress} from "../model";
import {MessageReactive} from "naive-ui/lib";
import {dataObject} from "../model/index.ts";

const message = useMessage();
const props = defineProps<{
  list?: any;
}>();
const menu = ref();
// const selectedItems = ref([]);
const dataObjectTemp = ref();

const items = ref([
  {
    label: "下载",
    icon: "pi pi-download",
    command: async () => {
      const res = dataObjectTemp.value;
      let messageReactive: MessageReactive | null = null

      messageReactive = message.loading("加载中", {
        duration: 0
      })

      try {
        const req = await axios.post(`${axios.defaults.baseURL}/down_file`, {
          "path": res.path
        }, {
          responseType: "blob"
        });

        const url = window.URL.createObjectURL(new Blob([req.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", res.name);
        document.body.appendChild(link);
        link.click();
      } catch (e) {
        message.error("下载错误");
      }

      if (messageReactive) {
        messageReactive.destroy()
        messageReactive = null
      }
    }
  }, {
    separator: true
  }, {
    label: "压缩",
    icon: "pi pi-bolt",
    command: () => simpleRequest("/zip_file", dataObjectTemp.value.path, message)
  }, {
    label: "重命名",
    icon: "pi pi-pencil",
    command: () => {
      dataObject.value = JSON.parse(JSON.stringify(dataObjectTemp.value))
      renameFileShow.value = true;
    }
  }, {
    label: "删除",
    icon: "pi pi-trash",
    command: () => {
      simpleRequest("/delete", dataObjectTemp.value.path, message, {
        request: false,
        click: (dataObject: any) => {
          ress.value = ress.value.filter((item: any) => item.name !== dataObject.name);
        },
        dataObject: dataObjectTemp.value
      });
    }
  }, {
    separator: true
  }, {
    label: "新建",
    icon: "pi pi-plus",
    items: [
      {
        label: "新建文件",
        icon: "pi pi-file",
        command: () => {
          dataObject.value = JSON.parse(JSON.stringify(dataObjectTemp.value))
          newFileShow.value = true;
        }
      }, {
        label: "新建文件夹",
        icon: "pi pi-folder",
        command: () => simpleRequest("/new_folder", dataObjectTemp.value.path, message)
      }
    ]
  }, {
    separator: true
  }, {
    label: "属性",
    icon: "pi pi-info-circle",
    command: () => renameFileShow.value = true
  }
]);

const newFileShow = ref(false);
const newFileName = ref("");
const renameFileShow = ref(false);

function newFile() {
  simpleRequest("/new_file", "", message, {
    data: {
      path: path.value,
      name: "213.txt"
    },
    click: (dataObject: any, res: any, newFileShowValue: boolean) => {
      // const index = ress.value.findIndex((item: any) => item.path === dataObject.path);
      //
      // ress.value[index].name = dataObject.name;
      // ress.value[index].path = res.data.results
      newFileShow.value = newFileShowValue;
    },
  });
}

function renameFile() {
  simpleRequest("/rename", "", message, {
    data: {
      path: dataObject.value.path,
      new_path: dataObject.value.name
    },
    click: (dataObject: any, res: any, renameFileShowValue: boolean) => {
      const index = ress.value.findIndex((item: any) => item.path === dataObject.path);

      ress.value[index].name = dataObject.name;
      ress.value[index].path = res.data.results;
      renameFileShow.value = renameFileShowValue;
    },
    resource: true,
    dataObject: dataObject.value,
    request: false
  });
}

function isImageFile(type: string): boolean {
  const imageExtensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".jfif", ".ico", ".avif"];
  return imageExtensions.includes(type);
}

function isZipFile(type: string): boolean {
  const zipExtensions = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".tar.gz", ".tar.bz2"];
  return zipExtensions.includes(type);
}

function menuClick(event: any, data: any) {
  menu.value.show(event);
  dataObjectTemp.value = data;
}

const animatedItems = ref([]);

function isAnimated(index: any) {
  return animatedItems.value.includes(<never>index);
}

setTimeout(() => {
  animatedItems.value = props.list.map((item: any, index: any) => index);
}, 1500);


// function toggleSelection(item: any) {
//   const index = selectedItems.value.indexOf(item);
//   if (index === -1) {
//     selectedItems.value.push(item);
//   } else {
//     selectedItems.value.splice(index, 1);
//   }
// }
//
// function isSelected(item: any): boolean {
//   return selectedItems.value.includes(item);
// }
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
  opacity: 0;
  transform: translateY(50px);
  animation: fadeInUp 0.5s forwards;
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

.side-navigation li:hover {
  background-color: #e9ecef;
}

/* 添加 active 类的样式 */
.side-navigation li.active {
  background-color: #eeeff4;
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

.label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
  font-size: 1em;
  color: black;
  vertical-align: middle;
}

.ellipsis-icon {
  font-size: 1.2em;
  color: black;
}

.file-size {
  width: 80px;
  margin-right: 8px;
  font-size: 0.9em;
  color: #555;
  text-align: right;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.side-navigation li.animated {
  transform: none;
}
</style>