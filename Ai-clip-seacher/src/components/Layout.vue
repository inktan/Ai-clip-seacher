<script setup>
</script>
<template>
    <div>
        <div class=" position-sticky top-0 z-3">
            <slot name="header"></slot>
        </div>
        <div>
            <slot name="main"></slot>
        </div>
    </div>
</template>
