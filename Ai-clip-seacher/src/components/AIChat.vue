<script lang="ts" setup>
import { ref, reactive, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { ChatDotRound, } from '@element-plus/icons-vue'

const isButtonVisible = ref(true);
const isChatBoxVisible = ref(false);

function toggleChat() {
    isButtonVisible.value = !isButtonVisible.value;
    isChatBoxVisible.value = !isChatBoxVisible.value;
}

</script>

<template>
    <div class="aichat-container">
        <el-button class="open-btn" :class="{ 'moving-button': isButtonVisible }" @click="toggleChat" size="large"
            type="default" :icon="ChatDotRound">
            AI助手
        </el-button>
        <div class="chat-box" :class="{ visible: isChatBoxVisible }">
            <div class="chat-content">
                AI助手
            </div>
            <el-button class="close-btn" type="" @click="toggleChat">隐藏</el-button>
        </div>
    </div>
</template>

<style lang="less" scoped>
@import "@/styles/var.less";

.aichat-container {
    .open-btn {
        justify-content: flex-start;
        width: 150px;
        border-radius: 30px;
        position: fixed;
        right: -60px;
        bottom: 200px;
        border-radius: 30px;
        transition: all 0.5s ease;
        transform: translateX(100px);
    }

    @keyframes moveLeftRight {
        0% {
            transform: translateX(0);
        }

        50% {
            transform: translateX(20px);
            /* 移动10px到右边 */
        }

        100% {
            transform: translateX(0);
            /* 移动回到原位 */
        }
    }

    .moving-button {
        animation: moveLeftRight 2s infinite alternate ease-in-out;
    }

    .chat-box {
        position: fixed;
        border: 1px solid #ccc;
        padding: 3px;
        // box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
        transition: all 0.5s ease;
        // z-index: 1;
        right: 10px;
        bottom: 10px;
        width: 500px;
        height: 600px;
        transform: translateX(660px);


        &.visible {
            transform: translateX(0px);
        }

        .chat-content {
            background-color: #d9ecff;
            width: 100%;
            height: 100%;
        }

        .close-btn {
            position: absolute;
            right: 0;
            top: 0;
            transform: translate(-10px, -30px); /* 向左和向上各偏移10像素 */

        }
    }
}
</style>
