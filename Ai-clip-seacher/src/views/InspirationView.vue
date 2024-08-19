<script setup>
import Detail from '@/components/pic_water_flow/Detail.vue'
import {useGlobalStore} from '@/store/globalStore'
const globalStore = useGlobalStore()

</script>
<template>
    <Detail :loading='globalStore.loading' :images="globalStore.images"/>
</template>

<style scoped lang="less">
@import "@/styles/var.less";
</style>