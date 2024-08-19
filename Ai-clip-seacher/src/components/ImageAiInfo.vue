<script lang="ts" setup>
import { ref, reactive, onBeforeMount, onMounted, onUpdated, watchEffect, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { getAIReadImage } from '@/api';
import axios from "axios"

const props = defineProps({
    url: {
        type: String,
    },
    projectName: {
        type: String,
    },
})

const aiText = ref('')
const aiLoading = ref(false)

const textDecoder = new TextDecoder();
const fetchAiDescrible = async (img_url) => {
    aiText.value = ''
    aiLoading.value = true
    window.start();
    // window.done();
    const params = {
        'img_url': img_url,
    }
    // 创建URLSearchParams实例并填充参数
    const searchParams = new URLSearchParams();
    for (const key in params) {
        searchParams.append(key, params[key]);
    }

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

watch(
    () => props.url,
    (url) => {
        fetchAiDescrible(url);
    },
    {
        immediate: true // 立即执行回调
    }
)
const loading = ref(true)
const handleLoad = function () {
    loading.value = false;
}
// 定义返回函数
const emit = defineEmits(['GoBack']);

const goBack = () => {
    // 这里可以写上返回的逻辑，比如路由跳转
    emit('GoBack');
};
</script>

<template>
    <div class="proinfo-container" v-loading="loading">
        <div class="back-button">
            <el-button type="info" @click="goBack">
                <el-icon>
                    <Back />
                </el-icon>
                返回
            </el-button>
        </div>
        <div class="box-left">
            <el-image :src="url" fit="contain" @load="handleLoad" />
            <!-- 这里要能够有点击上传图片的功能 -->
        </div>
        <div class="box-right" v-loading="aiLoading" element-loading-text="AI解析中...">
            <div v-if="!aiLoading">
                <h2>项目名称:</h2>
                <span>{{ projectName }}</span>
                <el-divider />
                <h2 class="aiH2">AI解说:</h2>
                <span> {{ aiText }} </span>
                <el-divider />
            </div>
        </div>
    </div>
</template>

<style lang="less" scoped>
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

    .back-button {
        position: absolute;
        top: 5px;
        left: 5px;
        // 脱离文档流后，注意元素的图层顺序问题
        z-index: 1;
    }

    .box-left {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        text-align: center;

        .el-image {
            margin: 5px;
            height: 660px;
            border-radius: 10px;
            transition: 0.5s;
        }
    }

    .box-right {
        margin: 10px;
        margin-top: 30px;
        width: 700px;

        h2 {
            font-weight: bold;
        }

        .aiH2 {
            margin-top: 0;
        }

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
