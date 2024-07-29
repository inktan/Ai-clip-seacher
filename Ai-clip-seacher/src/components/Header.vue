<script lang="ts" setup>
import { ref, reactive, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import imageSrc from '@/assets/logo.svg';

const props = defineProps({
    loading: {
        type: Boolean,
        required: true,
        default: false,
    },
})

// do not use same name with ref
const form = reactive({
    prompt: '',
    iamge: null,
    imageWeight: 0,
    n: 100,
})
const calculatedWeight = computed(() => form.imageWeight / 100);
const selectedFile = ref(null);

const imageUrl = ref('')
const fileInput = ref(null)

// Ai搜索的信息
const emit = defineEmits(['SubmitQuery']);
const handleSubmit = () => {

    const formData = new FormData();
    formData.append('prompt', form.prompt);
    formData.append('imageWeight', calculatedWeight.value);
    formData.append('prompt_img', selectedFile.value);
    formData.append('n01', 0);
    formData.append('n02', 200);

    emit('SubmitQuery', formData);
}

// 上传图片使用
function triggerFileInput() {
    // 触发隐藏的文件输入元素
    fileInput.value.click();
}

// 上传图片使用
function handleFileChange(event) {
    // 当文件被选中时触发
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
        // 创建一个URL对象，用于在el-image中显示图片
        imageUrl.value = URL.createObjectURL(file);
        console.log(imageUrl.value)
    }
}

function handleReset() {
    window.location.reload();
}

</script>

<template>
    <div class="header-container">
        <el-image style="width: 60px; height: 60px" :src="imageSrc" />
        <div>
            <el-button size="large" @click="handleReset">灵感</el-button>
            <el-button size="large" @click="handleSubmit">AI工具</el-button>
        </div>
        <div class="form">
            <el-form :inline="true" label-width="auto" @submit.prevent="handleSubmit">
                <el-form-item label="输入提示词">
                    <el-input v-model="form.prompt" style="width: 450px" placeholder="Please input prompt" size="large"
                        :maxlength="100" show-word-limit>
                        <template #prefix>
                            <el-icon class="el-input__icon">
                                <search />
                            </el-icon>
                        </template>
                    </el-input>
                    <el-button class="btnSearch" type="primary" :loading="loading" @click="handleSubmit">{{
                        loading ?
                            "搜索中..." : "搜索" }}</el-button>
                </el-form-item>
                <el-form-item label="">
                    <!-- 隐藏真实的文件输入元素 -->
                    <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
                    <el-button class="upload" @click="triggerFileInput">
                        选择图片
                        <el-icon class="el-icon--right">
                            <Upload />
                        </el-icon>
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <span class="demonstration">图片权重</span>
                    <el-slider :min="0" :max="100" v-model="form.imageWeight" />
                </el-form-item>
            </el-form>
        </div>
        <div class="promptImg">
            <el-tooltip placement="top" effect="light">
                <template #content>
                    <img :src="imageUrl" style="max-width: 600px; max-height: 600px;" />
                </template>
                <img v-if="imageUrl" :src="imageUrl" style="height: 65px; cursor: pointer;" />
            </el-tooltip>
        </div>
    </div>
</template>

<style lang="less" scoped>
@import "@/styles/var.less";

.header-container {
    display: flex;
    justify-content: start;
    align-items: center;
    gap: 30px;
    margin: 0 20px;

    .form {
        padding-top: 20px;

        .el-form-item {
            margin-right: 10px;

            .btnSearch {
                margin-left: 10px;
            }

            .upload {
                background-color: rgb(235, 235, 235);
            }

            .el-slider {
                width: 50px;
                margin-left: 20px;
            }
        }
    }

    .promptImg {
        .el-image {
            margin: 0 10px;
        }
    }
}
</style>
