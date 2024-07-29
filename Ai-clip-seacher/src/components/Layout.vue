<script setup>
</script>
<template>
    <div class="layout-container">
        <div class="header">
            <slot name="header"></slot>
        </div>
        <div class="topFill"></div>
        <div class="main">
            <slot name="main"></slot>
        </div>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "@/styles/var.less";

.layout-container {
    .header {
        position: fixed;
        height: 80px;
        width: 100%;
        background-color: rgb(253, 253, 253);

        border-top: 1px solid rgb(194, 194, 194);
        border-bottom: 1px solid rgb(194, 194, 194);
        z-index: 1;
    }

    .topFill {
        height: 100px;
        background-color: white;
    }

    .main {
        margin: 0 50px;
        // background-color: rgb(253, 236, 214);
        overflow: auto;
    }
}
</style>