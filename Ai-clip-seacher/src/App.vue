<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, nextTick, provide } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getRandomImages, postBestImagesPrompt,getProjectContent } from '@/api';
import eventBus from '@/eventBus';

import Layout from '@/components/Layout.vue'
import Header from '@/components/Header.vue'
import Detail from '@/views/Detail.vue'
import ProInfo from '@/components/ProInfo.vue'

const randomPicWaterFlow = ref({
  loading: true,
  images: []
})
const proInfoPicWaterFlow = ref({
  loading: true,
  images: []
})


const prefix = 'http://10.1.12.30:8081/static_200/';
const fetcData = async function () {
  randomPicWaterFlow.value.loading = true;
  const images = await getRandomImages(100);
  // console.log(images);
  randomPicWaterFlow.value.images = images.map(item => prefix + item);
  randomPicWaterFlow.value.loading = false;
}

onBeforeMount(fetcData)

async function fetchMore() {
  if (!hasMore.value)
    return
  randomPicWaterFlow.value.loading = true;
  const images = await getRandomImages(100);
  randomPicWaterFlow.value.images = randomPicWaterFlow.value.images.concat(images.map(item => prefix + item));

  randomPicWaterFlow.value.loading = false;
}

const hasMore = computed(() => {
  return randomPicWaterFlow.value.images.length < 10000;
})

const handleScroll = (event) => {
  if (randomPicWaterFlow.value.loading)
    return

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

async function handleSubmitQuery(query) {
  randomPicWaterFlow.value.images = []
  randomPicWaterFlow.value.loading = true;
  const images = await postBestImagesPrompt(query);
  randomPicWaterFlow.value.images = images.map(item => prefix + item);
  randomPicWaterFlow.value.loading = false;
}

// 获取项目详情的相关信息
const proInfoUrl = ref('')
const proInfoShow = ref(false)
const SearchProInfo = async (message) => {
  proInfoPicWaterFlow.value.loading = true
  proInfoUrl.value = message.newUrl_1k;

  window.scrollTo({
    top: 0,
    behavior: 'smooth' // 'smooth' 表示平滑滚动，也可以是 'auto'
  });
  proInfoShow.value = true
  proInfoPicWaterFlow.value.loading = true;
  
  const images = await getProjectContent(message.projectPath);
  proInfoPicWaterFlow.value.images = randomPicWaterFlow.value.images.concat(images.map(item => prefix + item));

};

provide('SearchProInfo', SearchProInfo);

</script>

<template>
  <div class="container">
    <Layout>
      <template #header>
        <div class="header">
          <Header @SubmitQuery="handleSubmitQuery" />
        </div>
      </template>
      <template #main>
        <div class="main">
          <ProInfo v-if="proInfoShow" :url="proInfoUrl" />
          <Detail v-if="proInfoShow" :picWaterFlowInfo="proInfoPicWaterFlow" />
          <Detail v-if="!proInfoShow" :picWaterFlowInfo="randomPicWaterFlow" />
        </div>
      </template>
    </Layout>
  </div>
</template>

<style lang="less" scoped>
.container {
  // overflow: auto;

  .main {
    // height: 1000px;
  }
}
</style>
