<script lang="ts" setup>
import { ref, reactive, onBeforeMount, onMounted, onUpdated, watchEffect, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getAIReadImage } from '@/api';
import axios from "axios"

import { useGlobalStore } from '@/store/globalStore'
const globalStore = useGlobalStore()

import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();

const props = defineProps({
    newUrl_1k: {
        type: String,
        default: () => '',
        required: true // 根据你的需求决定是否必填
    },
    projectName: {
        type: String,
        default: () => '',
        required: true // 根据你的需求决定是否必填
    }
});

const aiText = ref('')
const aiLoading = ref(false)

const textDecoder = new TextDecoder();
const fetchAiDescrible = async () => {
    aiText.value = ''
    aiLoading.value = true
    window.start();
    // window.done();
    const params = {
        'img_url': props.newUrl_1k,
    }
    // 创建URLSearchParams实例并填充参数
    const searchParams = new URLSearchParams();
    for (const key in params) {
        searchParams.append(key, params[key]);
    }
    // console.log(searchParams.toString())
    const resp = await getAIReadImage(searchParams.toString())
    const reader = resp.body.getReader();
    while (1) {
        aiLoading.value = false
        const { done, value } = await reader.read();
        if (done)
            break
        const str = textDecoder.decode(value)
        aiText.value += str
    }
    // window.start();
    window.done();
};

onMounted(() => {
    fetchAiDescrible()
})

watch(
    () => props.newUrl_1k,
    (url) => {
        fetchAiDescrible();
    },
    {
        // immediate: true // 立即执行回调
    }
)
const loading = ref(true)
const handleLoad = function () {
    loading.value = false;
}
// 定义返回函数
// const emit = defineEmits(['GoBack',"SearchByPic"]);

const goBack = () => {
    // 这里可以写上返回的逻辑，比如路由跳转
    // emit('GoBack');

    globalStore.fecthMore_random = true
    router.push('/');
};

// 基于当前图片进行以图搜图
const SearchByPic = () => {
    router.push({
        path: '/searchByPic',
        query: route.query
    });
};

</script>

<template>
    <div class="proinfo-container" v-loading="loading" element-loading-text="图片加载中...">

        <el-button class="position-absolute z-1 " style="top: 10px; right: 10px;" type="info" @click="SearchByPic">
            <span>
                以图搜图&nbsp;&nbsp;
            </span>
            <el-icon>
                <Right />
            </el-icon>
        </el-button>
        <div class="box-left">
            <el-image :src="newUrl_1k" fit="contain" @load="handleLoad" />
        </div>
        <div class="box-right" v-loading="aiLoading" element-loading-text="AI解析中...">
            <div v-if="!aiLoading">
                <h5>项目名称:</h5>
                <span>{{ projectName }}</span>
                <el-divider />
                <h5 class="aiH2">AI解说:</h5>
                <span> {{ aiText }} </span>
                <el-divider />
            </div>
        </div>
    </div>
</template>

<style lang="less">
@import "@/styles/var.less";

.proinfo-container {
    background-color: rgb(241, 241, 241);
    margin: 70px;
    margin-top: 1px;
    margin-bottom: 30px;
    display: flex;
    border-radius: 10px;
    // border: 1px dashed;
    position: relative;

    .box-left {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        text-align: center;

        .el-image {
            margin: 5px;
            // margin-top:50px;
            height: 660px;
            border-radius: 10px;
            transition: 0.5s;
        }
    }

    .box-right {
        margin: 10px;
        margin-top: 30px;
        width: 700px;

        span {
            display: block;
            margin-top: 10px;
            margin-right: 30px;
            text-indent: 2em;
            font-size: 15px;
            line-height: 22px;
            word-wrap: break-word;
            // background: linear-gradient(to right, #e9e9eb, #b1b3b8) no-repeat right bottom;
            // background-size: 0 2px;
            // transition: background-size 1s;
        }

        span:hover {
            background-position: left bottom;
            background-size: 100% 2px;

        }
    }
}
</style>
