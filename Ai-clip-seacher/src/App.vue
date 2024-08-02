<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, nextTick, provide } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getRandomImages, postBestImagesPrompt, getProjectContent } from '@/api';
import eventBus from '@/eventBus';

import AIChat from '@/components/AIChat.vue'
import Layout from '@/components/Layout.vue'
import Header from '@/components/Header.vue'
import Detail from '@/views/Detail.vue'
import ProInfo from '@/components/ProInfo.vue'

const headerLoading = ref(false)
const randomPicWaterFlow = ref({
  loading: true,
  images: []
})

const prefix = 'http://10.1.12.30:5173/static_200/';
const fetcData = async function () {
  randomPicWaterFlow.value.loading = true;
  window.start();
  // window.done();
  const data = await getRandomImages(100);
  // console.log(images);
  randomPicWaterFlow.value.images = data.results.map(item => prefix + item);
  randomPicWaterFlow.value.loading = false;
  // window.start();
  window.done();
}

onBeforeMount(fetcData)

async function fetchMore() {
  if (!hasMore.value)
    return
  randomPicWaterFlow.value.loading = true;
  window.start();
  // window.done();
  const data = await getRandomImages(100);
  randomPicWaterFlow.value.images = randomPicWaterFlow.value.images.concat(data.results.map(item => prefix + item));
  window.done();

  randomPicWaterFlow.value.loading = false;
}

const hasMore = computed(() => {
  return randomPicWaterFlow.value.images.length < 10000;
})

const handleScroll = (event) => {
  if (randomPicWaterFlow.value.loading)
    return
  // 判断是否要加载更多
  // 条件1 窗口移动到底部
  // 条件2 灵感 / AI搜索
  if (window.scrollY + window.innerHeight >= document.body.scrollHeight) {
    fetchMore();
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
})
// Ai搜图
async function handleSubmitQuery(query) {
  randomPicWaterFlow.value.images = []
  proInfoShow.value = false
  headerLoading.value = true
  randomPicWaterFlow.value.loading = true;
  window.start();
  // window.done();
  const data = await postBestImagesPrompt(query);
  randomPicWaterFlow.value.images = data.results.map(item => prefix + item);
  randomPicWaterFlow.value.loading = false;
  headerLoading.value = false
  // window.start();

  // 打印中英文对比信息
  console.log(`输出搜索关键词：${data.prompt}`)
  window.done();
}

// 获取项目详情的相关信息

const proInfoPicWaterFlow = ref({
  loading: true,
  images: [],
  describle: ''
})

const proInfoUrl = ref('')
const projectName = ref('')
const proInfoShow = ref(false)
const SearchProInfo = async (message) => {
  // 项目详情页面，移除Fetchmore
  window.removeEventListener('scroll', handleScroll);

  proInfoPicWaterFlow.value.loading = true
  proInfoUrl.value = message.newUrl_1k;
  projectName.value = message.projectName;
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // 'smooth' 表示平滑滚动，也可以是 'auto'
  });
  proInfoShow.value = true
  proInfoPicWaterFlow.value.loading = true;
  // 远程获取项目文件夹
  const data = await getProjectContent(message.projectPath);
  proInfoPicWaterFlow.value.images = data.results.map(item => prefix + item);
  proInfoPicWaterFlow.value.loading = false;
};

provide('SearchProInfo', SearchProInfo);
const handleGoBack = () => {
  proInfoShow.value = false;
}
</script>

<template>
  <div class="container">
    <Layout>
      <template #header>
        <div class="header">
          <Header @SubmitQuery="handleSubmitQuery" :loading="headerLoading" />
        </div>
      </template>
      <template #main>
        <div class="main">
          <ProInfo v-if="proInfoShow" :url="proInfoUrl" :projectName="projectName" @GoBack="handleGoBack" />
          <el-divider  v-if="proInfoShow" />
          <Detail v-if="proInfoShow" :picWaterFlowInfo="proInfoPicWaterFlow" />
          <Detail v-if="!proInfoShow" :picWaterFlowInfo="randomPicWaterFlow" />
        </div>
      </template>
    </Layout>
    <AIChat />
  </div>
</template>

<style lang="less" scoped>
.container {
  // overflow: auto;
  position: relative;

  .main {
    // height: 1000px;
  }
}
</style>
