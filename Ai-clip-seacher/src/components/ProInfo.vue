<script lang="ts" setup>
import { ref, reactive, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'

const props = defineProps({
    url: {
        type: String,
    },
})

const loading = ref(true)
const handleLoad = function () {
    loading.value = false;
    // console.log('=====>>>')
}

</script>

<template>
    <div class="proinfo-container" v-loading="loading">
        <div class="box-left">
            <el-image :src="url" fit="contain" @load="handleLoad" />
        </div>
        <div class="box-right">Right Box</div>
    </div>
</template>

<style lang="less" scoped>
@import "@/styles/var.less";

.proinfo-container {
    background-color: rgb(212, 235, 255);
    margin: 70px;
    margin-top: 1px;
    margin-bottom: 30px;
    display: flex;
    border-radius: 10px;
    // border: 1px dashed;

    .box-left {
        width: 100%;
        text-align: center;

        .el-image {
            height: 660px;
            border-radius: 10px;
            transition: 0.5s;
        }
    }

    .box-right {
        width: 600px;
    }
}
</style>
