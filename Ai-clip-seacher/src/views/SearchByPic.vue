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

onBeforeMount(async () => {
    searchByPic()
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
        searchByPicFetchMore();
    }
};


const hasMore = computed(() => {
    return globalStore.images.length < 2000;
})

// 基于详图进行图搜图
async function searchByPic() {
    globalStore.images = []
    globalStore.loading = true;
    window.start();

    globalStore.fecthMore_random = false;
    globalStore.fecthMore_ai = true;

    // console.log(`输入搜索关键词：${form.prompt}`)
    const formData = new FormData();
    formData.append('prompt', '');
    formData.append('imageWeight', 1.0);
    formData.append('prompt_img', new Blob([]));
    const newUrl_1k = prefix_1k + route.query.projectPath + '\\' + route.query.imgName
    globalStore.imageUrl = newUrl_1k
    formData.append('prompt_img_url', newUrl_1k);
    formData.append('rendering_img', globalStore.rendering);
    formData.append('realScene_img', globalStore.realScene);
    formData.append('n01', 0);
    formData.append('n02', 250);
    // for (const pair of formData.entries()) {
    //     console.log(`${pair[0]}:${pair[1]}`);
    // }

    globalStore.formData_ai = formData;
    // console.log(globalStore.formData_ai)
    // return

    const data = await searchByPicUrl(globalStore.formData_ai);
    globalStore.images = data.results.map(item => ({
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

    await delay(3000);
    window.done();
    globalStore.loading = false;
}
async function searchByPicFetchMore() {
    if (!hasMore.value)
        return
    if (globalStore.loading)
        return

    globalStore.loading = true;
    window.start();
    await delay(3000);

    // 获取当前 n01 和 n02 的值
    let n01 = parseInt(globalStore.formData_ai.get('n01'), 10);
    let n02 = parseInt(globalStore.formData_ai.get('n02'), 10);

    // 自增500
    n01 += 250;
    n02 += 250;
    // 更新 formData 对象中的值
    globalStore.formData_ai.set('n01', n01);
    globalStore.formData_ai.set('n02', n02);
    const data = await searchByPicUrl(globalStore.formData_ai);
    globalStore.images = globalStore.images.concat(data.results.map(item => ({
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
    await delay(3000);
    window.done();
    globalStore.loading = false;
}

</script>
<template>
    <Detail :imageInfos="globalStore.images" />
</template>

<style scoped lang="less">
@import "@/styles/var.less";
</style>