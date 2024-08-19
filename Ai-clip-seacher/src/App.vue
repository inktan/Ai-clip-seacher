<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, nextTick, provide, inject } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getRandomImages, postBestImagesPrompt} from '@/api';
import {useGlobalStore} from '@/store/globalStore'
const globalStore = useGlobalStore()

import AIChat from '@/components/AIChat.vue'
import Layout from '@/components/Layout.vue'
import Header from '@/components/Header.vue'

// 随机灵感
const prefix = 'http://10.1.12.30:5173/static_200/';
const fetchRandomData = async function () {
  globalStore.images = []

  globalStore.loading = true;
  window.start();
  // window.done();
  const data = await getRandomImages(100);
  // console.log(images);
  globalStore.images = data.results.map(item => prefix + item);

  globalStore.loading = false;
  // window.start();
  window.done();
}

onBeforeMount(fetchRandomData)

async function fetchMore() {
  if (!hasMore.value)
    return
  globalStore.loading = true;
  window.start();
  // window.done();
  const data = await getRandomImages(100);
  globalStore.images  = globalStore.images.concat(data.results.map(item => prefix + item));
  window.done();

  globalStore.loading = false;
}

const hasMore = computed(() => {
  return globalStore.images.length < 10000;
})

const handleScroll = (event) => {
  if (globalStore.loading || !globalStore.fecthMore )
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

function handleRandomImgs() {
  globalStore.images = []
  fetchRandomData()
}

// AI搜图
const headerLoading = ref(false)
async function handleSubmitQuery(query) {

  globalStore.images = []
  headerLoading.value = true
  globalStore.loading = true;
  window.start();
  // window.done();

  const data = await postBestImagesPrompt(query);
  globalStore.images = data.results.map(item => prefix + item);
  globalStore.loading = false;
  headerLoading.value = false
  // window.start();

  // 打印中英文对比信息
  // console.log(`输出搜索关键词：${data.prompt}`)
  window.done();
}
// AI图文解析
function handleTextImgAna() {
  console.log('handleTextImgAna')
}

</script>

<template>
  <div class="container">
    <Layout>
      <template #header>
        <div class="header">
          <Header @RandomImgs="handleRandomImgs" @TextImgAna="handleTextImgAna" @SubmitQuery="handleSubmitQuery"
            :loading="headerLoading" />
        </div>
      </template>
      <template #main>
        <div class="main">
          <RouterView/>
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
}
</style>
