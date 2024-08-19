<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import PicWaterFlow from '@/components/pic_water_flow/PicWaterFlow.vue'

const props = defineProps({
    loading: {
        type: Boolean,
        required: true
    },
    images: {
        type: Array,
        required: true,
        default: () => [],
    },
})

</script>
<template>
    <div class="detail-container">
        <PicWaterFlow :images=images />
        <div class="loading" v-loading="loading" v-if="loading"  element-loading-text="AI搜索中..."></div>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "@/styles/var.less";

.detail-container {
    .loading {
        height: 100px;
    }
}
</style>