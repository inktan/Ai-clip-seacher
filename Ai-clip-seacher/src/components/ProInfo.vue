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
const fetchAiDescrible = async () => {
    aiText.value = ''
    aiLoading.value = true
    window.start();
    // window.done();
    const resp = await fetch(`http://10.1.12.30:5001/ai_image_description?img_url=${props.url}`)
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
watchEffect(fetchAiDescrible);

const loading = ref(true)
const handleLoad = function () {
    loading.value = false;
}

</script>

<template>
    <div class="proinfo-container" v-loading="loading">
        <div class="box-left">
            <el-image :src="url" fit="contain" @load="handleLoad" />
        </div>
        <div class="box-right" v-loading="aiLoading" element-loading-text="AI解析中...">
            <div v-if="!aiLoading">
                <h2>项目名称:</h2>
                <p>{{ projectName }}</p> 
                <h2>AI解说:</h2>
                <p>{{ aiText }}</p>
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

    .box-left {
        margin: 10px;
        width: 100%;
        text-align: center;

        .el-image {
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

        p {
            margin-top: 10px;
            margin-right: 30px;
            text-indent: 2em;
            font-size: 15px;
            line-height: 20px;
        }
    }
}
</style>
