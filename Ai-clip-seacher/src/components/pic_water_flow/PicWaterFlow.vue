<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineProps, watch, onUnmounted, watchEffect } from 'vue';
// import setPostions from '@/utils/setPositions';
import debounce from '@/utils/debounce';
import { useRoute, useRouter } from 'vue-router';
const router = useRouter();

import { useGlobalStore } from '@/store/globalStore'
const globalStore = useGlobalStore()

const props = defineProps({
    imageInfos: {
        type: Array,
        default: () => [],
        required: true // 根据你的需求决定是否必填
    }
});

const PicWaterfallFlowDiv = ref(null);

const deSetPositions = debounce(() => {
    const colWidth = 200
    const gapWidth = 20

    if (PicWaterfallFlowDiv.value) {
        const containerRect = PicWaterfallFlowDiv.value.getBoundingClientRect()
        // console.log(containerRect)

        // const style = window.getComputedStyle(PicWaterfallFlowDiv.value);
        const flowWidth = parseInt(containerRect.width);
        // const flowHeight = parseInt(style.height);
        // console.log(`宽度: ${flowWidth}, 高度:${flowHeight}`);

        var colsTmp = flowWidth / (colWidth + gapWidth);
        var cols = Math.floor(flowWidth / (colWidth + gapWidth));
        if ((colsTmp - cols) < 0.3) {
            cols -= 1
        }
        // console.log(flowWidth / (colWidth + gapWidth))
        // console.log(Math.floor(flowWidth / (colWidth + gapWidth)))
        var leftSpace = (flowWidth - cols * (colWidth + gapWidth)) * 0.5;
        var arr = new Array(cols);
        arr.fill(0);

        for (var i = 0; i < props.imageInfos.length; i++) {
            var image = props.imageInfos[i];
            var minTop = Math.min(...arr);
            var index = arr.indexOf(minTop);
            arr[index] += image.height + gapWidth;
            var left = leftSpace + index * (gapWidth + colWidth);

            image.translateX = left;
            image.translateY = minTop;

            // 窗口顶部位置  图片底部y值与窗口上边界的距离
            const topBool = minTop + containerRect.top + image.height + gapWidth > 100
            // 窗口底部位置  图片顶部y值与窗口下边界的距离
            const bottomBool = minTop + containerRect.top < window.innerHeight + 10

            if (topBool && bottomBool) {
                image.isVisible = true;
            }
            else {
                image.isVisible = false;
            }
        }

        contentHeight.value = Math.max(...arr);
        filteredItems.value = props.imageInfos.filter(item => item.isVisible);

        // imageElements.value.forEach((el) => {
        //     if (el) {
        //         observer.observe(el);
        //     }
        // });
    }
}, 300);

const isBoxVisible = (boxRect, containerRect) => {
    return (
        boxRect.top < containerRect.bottom &&
        boxRect.bottom > containerRect.top &&
        boxRect.left < containerRect.right &&
        boxRect.right > containerRect.left
    );
};

const filteredItems = ref([])

const imageElements = ref([]);

// 使用IntersectionObserver来观察每个img元素。当图片进入或离开可视范围时，isVisible状态会相应地更新。
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        const index = imageElements.value.indexOf(entry.target);
        // console.log(index)
        if (entry.isIntersecting) {
            props.imageInfos[index].isVisible = true;
            // 可以选择停止观察，如果不再需要
            // observer.unobserve(entry.target);
        } else {
            props.imageInfos[index].isVisible = false;
        }
    });
}, {
    rootMargin: '0px',
    threshold: 0.1 // 触发回调的交并比阈值
});

// 初始高度
const contentHeight = ref(0);
watchEffect(() => {
    if (globalStore.getCount || props.imageInfos) {
        // console.log('watchEffect')
        deSetPositions();
    }
});

onMounted(() => {
    window.addEventListener('resize', deSetPositions);
    window.addEventListener('scroll', deSetPositions);

})

onUnmounted(() => {
    window.removeEventListener('resize', deSetPositions);
    window.removeEventListener('scroll', deSetPositions);

    observer.disconnect();
})

function handleImageLoad(index) {
    filteredItems.value[index].loaded = true;
}

const handleImageError = (index) => {
    // filteredItems.value[index].loaded = false;
    // filteredItems.value[index].isVisible = false;
    // deSetPositions();
};

const activeIndex = ref(0); // 用于跟踪当前鼠标悬停的链接索引

function handleMouseOver(index) {
    activeIndex.value = index;
}
function handleMouseLeave(index) {
    activeIndex.value = null;
}

const loading = ref(true)
function handleClick(url) {
    const parts = url.split('\\');

    const projectPath = parts.slice(2, -1).join('\\');
    const imgName = parts[parts.length - 1];

    // 项目详情页面，移除Fetchmore
    globalStore.fecth_random = false;
    globalStore.fecth_ai = false;
    globalStore.fecthMore_random = false
    globalStore.fecthMore_ai = false

    router.push({
        path: '/proInfoView',
        query: {
            projectPath: projectPath,
            imgName: imgName,
        }
    });
}
// 计算瀑布的高度尺寸
// 绑定v-if位于窗口内的为true

</script>
<template>
    <!-- id="PicWaterfallFlow" 函数监控的布局瀑布流盒子 -->
    <div ref="PicWaterfallFlowDiv" class="PicWaterfallFlow position-relative" id="PicWaterfallFlow"
        :style="{ height: contentHeight + 'px' }">
        <div class="flow-item position-absolute top-0 start-0" v-for="(item, index) in filteredItems" :key="item.imgUrl"
            :ref="el => { imageElements[index] = el }" :style="{
                transform: 'translateX(' + item.translateX + 'px) translateY(' + item.translateY + 'px)',
                width: item.width + 'px',
                height: item.height + 'px'
            }">
            <a class="rounded-4 overflow-hidden d-block w-100 h-100" @mouseover="handleMouseOver(index)"
                style="cursor: pointer;" @mouseleave="handleMouseLeave(index)"
                :class="{ 'with-overlay': activeIndex === index }" :underline="false" @click="handleClick(item.imgUrl)">
                <div class="w-100 h-100">
                    <img class=" w-100 h-100" :src="item.imgUrl" @load="handleImageLoad(index)"
                        @error="handleImageError(index)" />
                    <div class="overlay w-100 h-100 position-absolute top-0 start-0 bottom-0 end-0 d-flex align-items-center justify-content-center"
                        v-if="item.loaded">
                        项目详情
                    </div>
                    <!-- 占位符 -->
                    <div v-if="!item.loaded" class="position-absolute top-0 start-0 w-100 h-100 bg-white z-n1">
                        <div class="p-2 placeholder-glow h-100" style="cursor: wait;">
                            <span class="m-2 d-block placeholder col-7"></span>
                            <span class="m-2 d-block placeholder col-4"></span>
                            <span class="m-2 d-block placeholder col-4"></span>
                            <span class="m-2 d-block placeholder col-6"></span>
                            <span class="m-2 d-block placeholder col-8"></span>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
@import "@/styles/var.less";

.PicWaterfallFlow {

    .flow-item {
        a {
            box-shadow: 5px 5px 10px 0 rgba(0, 0, 0, 0.5);
        }

        transition: transform .2s;

        img {
            transition: all 0.35s ease;
        }

        .placeholder {
            box-shadow: 5px 5px 10px 0 rgba(0, 0, 0, 0.5);
        }

        .describle {
            text-align: center;
            margin: 10px;
            font-size: 12px;
        }

        .overlay {
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .with-overlay .overlay {
            opacity: 1;
        }

    }
}
</style>
