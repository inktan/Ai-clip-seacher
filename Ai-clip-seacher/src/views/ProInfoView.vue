<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, nextTick, provide } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getRandomImages, postBestImagesPrompt, getProjectContent } from '@/api';
import eventBus from '@/eventBus';
import Detail from '@/components/pic_water_flow/Detail.vue'
import ImageAiInfo from '@/components/ImageAiInfo.vue'
import PicWaterFlow from '@/components/pic_water_flow/PicWaterFlow.vue'

import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();

import { useGlobalStore } from '@/store/globalStore'
const globalStore = useGlobalStore()

const renderingPrefix = ['DSWH', 'FanTuo', 'inplacevisual', '淘宝效果图资源'];
function startsWithAnyPrefix(str, prefixes) {
  for (let prefix of prefixes) {
    if (str.startsWith(prefix)) {
      return true;
    }
  }
  return false;
}

onBeforeMount(async () => {
  SearchProInfo()
})

watch(
  () => route.query.projectPath,
  async (newValue, oldValue) => {
    SearchProInfo()
  },
  // { immediate: true },
)

watch(
  () => route.query.imgName,
  async (newValue, oldValue) => {

    scrollTo({
      top: 0,
      behavior: 'smooth' // 'smooth' 表示平滑滚动，也可以是 'auto'
    });

    newUrl_1k.value = 'http://10.1.12.30:5173\\static_1\\' + route.query.projectPath + '\\' + route.query.imgName

  },
  // { immediate: true },
)

const prefix = 'http://10.1.12.30:5173\\static_200\\';

// 获取项目详情的相关信息
const newUrl_1k = ref('')
const projectName = ref('')
const projectImages = ref([])

const SearchProInfo = async () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // 'smooth' 表示平滑滚动，也可以是 'auto'
  });

  // 远程获取项目文件夹
  newUrl_1k.value = 'http://10.1.12.30:5173\\static_1\\' + route.query.projectPath + '\\' + route.query.imgName
  projectName.value = route.query.projectPath

  // 如果进入效果图文件夹则不进行索引
  // console.log(route.query.projectPath)
  const isRender = startsWithAnyPrefix(route.query.projectPath, renderingPrefix);
  if (isRender) {
    return
  }
  globalStore.loading = true

  const data = await getProjectContent(route.query.projectPath);
  projectImages.value = data.results.map(item => ({
    imgUrl: prefix + item[0],
    alt: `Description for ${item[0]}`, // 假设这是图片的替代文本
    isVisible: false,
    loaded: false,
    width: item[1],
    height: item[2],
    translateX: -3000,
    translateY: -3000,
    // ... 添加更多属性
  }));

  projectName.value = data.project_path

  globalStore.loading = false;

  globalStore.fecth_random = false;
  globalStore.fecth_ai = false;
  globalStore.fecthMore_random = false;
  globalStore.fecthMore_ai = false;
};

</script>

<template>
  <div class="container">
    <ImageAiInfo :newUrl_1k="newUrl_1k" :projectName="projectName" />
    <el-divider />

    <div class=".bg-info-subtle" style="height: 120px;" v-loading="globalStore.loading" v-if="globalStore.loading"
      element-loading-text="AI搜索中..."></div>

    <div v-if="!globalStore.loading && projectImages.length > 0">
      <div class=" text-center m-3 ">
        <span class=" fs-3 text-center">
          项目文件
        </span>
        <span>
          ({{ projectImages.length }}张)
        </span>
      </div>
      <PicWaterFlow v-if="projectImages.length > 0" :imageInfos="projectImages" />
    </div>

    <!-- <Detail  v-loading="globalStore.loading" v-if="globalStore.loading" :imageInfos="projectImages" /> -->

  </div>
</template>

<style lang="less"></style>
