<script setup>
import { ref, reactive, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, provide, inject } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import imageSrc from '@/assets/logo.svg';
import { useGlobalStore } from '@/store/globalStore'
const globalStore = useGlobalStore()

import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();

// do not use same name with ref
const form = reactive({
    prompt: '',
    iamge: null,
    imageWeight: 50,
    n: 100,
})
const calculatedWeight = computed(() => form.imageWeight / 100);
const selectedFile = ref(null);

const fileInput = ref(null)
const emit = defineEmits(['SubmitQuery', 'RandomImgs', 'TextImgAna']);

// 基于文字信息和图片信息进行Ai搜索
const handleEnter = () => {
    handleSubmit()
}
const handleSubmit = () => {
    globalStore.searchCount += 1

    globalStore.fecthMore_random = false;
    globalStore.fecthMore_ai = true;

    // console.log(`输入搜索关键词：${form.prompt}`)
    const formData = new FormData();
    formData.append('prompt', form.prompt);
    formData.append('imageWeight', calculatedWeight.value);
    formData.append('prompt_img', selectedFile.value);
    formData.append('prompt_img_url', '');
    formData.append('rendering_img', globalStore.rendering);
    formData.append('realScene_img', globalStore.realScene);
    formData.append('n01', 0);
    formData.append('n02', 250);

    globalStore.formData_ai = formData;

    router.push('/search');
    // emit('SubmitQuery');
}

// 上传图片使用
function triggerFileInput() {
    // 触发隐藏的文件输入元素
    fileInput.value.click();
}

watch(
    () => globalStore.imageUrl,
    async (newValue, oldValue) => {
        if (newValue) {
            try {
                // 使用fetch获取图片数据
                const response = await fetch(newValue);
                if (!response.ok) throw new Error('Network response was not ok.');
                // 将响应转换为Blob
                const blob = await response.blob();
                // 创建File对象
                const fileName = newValue.split('/').pop(); // 假设URL的最后一部分是文件名
                const file = new File([blob], fileName, { type: blob.type });
                // 将File对象赋值给selectedFile.value
                selectedFile.value = file;
            } catch (error) {
                console.error('Error fetching image:', error);
            }
        }
    },
    // { immediate: true } // 如果你希望在watch创建时立即执行，可以取消注释
);

// 上传图片使用
function handleFileChange(event) {
    // 当文件被选中时触发
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
        // 创建一个URL对象，用于在el-image中显示图片
        // console.log(globalStore.imageUrl)
        globalStore.imageUrl = URL.createObjectURL(file);
    }
}

// 刷新灵感图片
function handleRandomImgs() {
    globalStore.randomCount += 1

    // 1 首页路由 /
    if (route.path == "/") {
        window.location.reload();
    }
    // 2 基于详图进入以图搜图的路由 /searchByPic
    else {
        router.push('/');
        globalStore.imageUrl = ''
    }
}

</script>

<template>
    <div class="d-flex align-items-center ps-5 mb-3 bg-white border-bottom" style="height: 80px;">
        <img :src="imageSrc" style="width: 60px; height: 60px" alt="...">
        <div class="ms-4">
            <el-button @click="handleRandomImgs">灵感</el-button>
        </div>
        <el-input class="ms-4" v-model="form.prompt" style="width: 450px" placeholder="输入搜索关键词……" size="large"
            :maxlength="100" show-word-limit @keyup.enter="handleEnter">
            <template #prefix>
                <el-icon class="el-input__icon">
                    <search />
                </el-icon>
            </template>
        </el-input>
        <el-button class="ms-3" type="primary" :loading="globalStore.loading" @click="handleSubmit">{{
            globalStore.loading ?
                "搜索中..." : "搜索" }}</el-button>
        <!-- 隐藏真实的文件输入元素 -->
        <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
        <el-tooltip class="box-item" effect="dark" content="上传图片找相似图" placement="top-start">
            <el-button class="ms-2" @click="triggerFileInput">
                选择图片
                <el-icon class="el-icon--right">
                    <Upload />
                </el-icon>
            </el-button>
        </el-tooltip>
        <p class="ms-2 mb-0" style="font-size: small ">图片权重</p>
        <el-slider class="ms-3 mb-0" style="width: 100px;" :min="0" :max="100" v-model="form.imageWeight" />
        <el-checkbox class="ms-3 me-0" v-model="globalStore.rendering" label="效果图" size="large" />
        <el-checkbox class="ms-3 me-0" v-model="globalStore.realScene" label="实景" size="large" />
        <div class="promptImg ms-3">
            <el-tooltip placement="top" effect="light">
                <template #content>
                    <img :src="globalStore.imageUrl" style="max-width: 600px; max-height: 600px;" />
                </template>
                <img v-if="globalStore.imageUrl" :src="globalStore.imageUrl" style="height: 65px; cursor: pointer;" />
            </el-tooltip>
        </div>
    </div>
</template>
