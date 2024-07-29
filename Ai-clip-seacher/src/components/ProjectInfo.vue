<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import PicWaterFlow from '@/components/PicWaterFlow.vue'

const props = defineProps({
    picWaterFlowInfo: {
        type: Object,
        required: true
    },
    url: {
        type: String,
        required: true
    },
})

// function handleClick(){
//     console.log(props.picWaterFlowInfo)
// }

//请求图片

</script>
<template>
    <div class="ProjectInfo-container">
        <el-image style="width: 800px; height: 800px" :src="url" :fit="contain" />
        <PicWaterFlow :images="picWaterFlowInfo.images" />
        <div class="loading" v-loading="picWaterFlowInfo.loading" v-if="picWaterFlowInfo.loading"></div>
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