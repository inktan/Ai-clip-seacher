<script setup>
import { ref, onBeforeMount, onMounted, watchEffect, computed, defineComponent, watch, onUnmounted, nextTick, provide } from 'vue';
import { getRandomImages, postBestImagesPrompt, searchByPicUrl } from '@/api';
import { debounce, delay, showMessage } from '@/utils';

import Detail from '@/components/pic_water_flow/Detail.vue'
import { useGlobalStore } from '@/store/globalStore'
const globalStore = useGlobalStore()

import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();

const prefix_200 = 'http://10.1.12.30:5173\\static_200\\';
const prefix_1k = 'http://10.1.12.30:5173\\static_1\\'

const randomImages = ref([])

onBeforeMount(async () => {
    // 1 首页路由 /
    if (route.path == "/") {
        fetchRandomData()
    }
})

onMounted(() => {
    window.addEventListener('scroll', handleScroll);
})
onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
})
const handleScroll = (event) => {
    if (globalStore.loading)
        return

    // 判断是否要加载更多
    // 条件1 窗口移动到底部
    // 条件2 灵感 / AI搜索
    if (window.scrollY + window.innerHeight >= document.body.scrollHeight) {
        // 1 首页路由 /
        if (route.path == "/") {
            fetchMore_random();
        }
    }
};

// 首页路由为随机页面
const fetchRandomData = async function () {
    randomImages.value = []

    // if (!globalStore.fecth_random)
    //     return

    globalStore.loading = true;
    window.start();
    const data = await getRandomImages(250);
    // randomImages = data.results.map(item => prefix + item);

    randomImages.value = data.results.map(item => ({
        imgUrl: prefix_200 + item[0],
        alt: `Description for ${item[0]}`, // 假设这是图片的替代文本
        isVisible: false,
        loaded: false,
        width: item[1],
        height: item[2],
        translateX: -3000,
        translateY: -3000,
        // ... 添加更多属性
    }));
    // await delay(3000);

    globalStore.loading = false;
    window.done();
}
async function fetchMore_random() {
    // return

    if (!hasMore.value)
        return
    if (globalStore.loading)
        return

    globalStore.loading = true;
    window.start();
    const data = await getRandomImages(250);
    randomImages.value = randomImages.value.concat(data.results.map(item => ({
        imgUrl: prefix_200 + item[0],
        alt: `Description for ${item[0]}`, // 假设这是图片的替代文本
        isVisible: false,
        loaded: false,
        width: item[1],
        height: item[2],
        translateX: -3000,
        translateY: -3000,
        // ... 添加更多属性
    })));
    // await delay(3000);
    window.done();
    globalStore.loading = false;
}

const hasMore = computed(() => {
    return randomImages.value.length < 2000;
})

</script>
<template>
    <Detail :imageInfos="randomImages" />
</template>

<style scoped lang="less">
@import "@/styles/var.less";
</style>