<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineProps, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import PicWaterFlow from '@/components/pic_water_flow/PicWaterFlow.vue'
import { useGlobalStore } from '@/store/globalStore'
const globalStore = useGlobalStore()

const props = defineProps({
    imageInfos: {
        type: Array,
        default: () => [],
        required: true // 根据你的需求决定是否必填
    }
});
</script>
<template>
    <div class="detail-container">
        <PicWaterFlow :imageInfos="imageInfos"/>
        <div class=" " style="height: 100px;" v-loading="globalStore.loading" v-if="globalStore.loading"
            element-loading-text="AI搜索中..."></div>
    </div>
</template>
