<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, nextTick, provide } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getRandomImages, postBestImagesPrompt, getProjectContent } from '@/api';
import eventBus from '@/eventBus';
import Detail from '@/components/pic_water_flow/Detail.vue'
import ImageAiInfo from '@/components/ImageAiInfo.vue'

import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();

import {useGlobalStore} from '@/store/globalStore'
const globalStore = useGlobalStore()

onBeforeMount(async () => {
  SearchProInfo(routeInfo.value)
})

const routeInfo = computed(() => {
  // console.log(route.query,'query')
  // console.log(route.params,'params')
  const projectName = route.query.projectName || '';
  const projectPath = route.query.projectPath || '';
  const newUrl_1k = route.query.newUrl_1k || '';

  proUrl.value = newUrl_1k;
  proName.value = projectName;

  return projectPath
})

watch(
  () => route.fullPath,
  async (newValue, oldValue) => {
    const projectName = route.query.projectName || '';
    const projectPath = route.query.projectPath || '';
    const newUrl_1k = route.query.newUrl_1k || '';

    if (route.query) {
      proUrl.value = newUrl_1k;
      proName.value = projectName;
      SearchProInfo(projectPath)
    }

  },
  // { immediate: true },
)
const headerLoading = ref(false)

const prefix = 'http://10.1.12.30:5173/static_200/';

const loading = ref(false)
const images = ref([])
// 获取项目详情的相关信息
const proUrl = ref('')
const proName = ref('')
const SearchProInfo = async (projectPath) => {
  // 项目详情页面，移除Fetchmore
  // window.removeEventListener('scroll', handleScroll);
  loading.value = true
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // 'smooth' 表示平滑滚动，也可以是 'auto'
  });
  // 远程获取项目文件夹
  const data = await getProjectContent(projectPath);
  images.value = data.results.map(item => prefix + item);
  loading.value = false;
};

const handleGoBack = () => {
  globalStore.fecthMore = true
  router.push('/');
}

</script>

<template>
  <div class="container">
    <ImageAiInfo :url="proUrl" :projectName="proName" @GoBack="handleGoBack" />
    <el-divider />
    <Detail :loading='loading' :images="images" />
  </div>
</template>

<style lang="less" scoped></style>
