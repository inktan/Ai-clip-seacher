<script setup>
import { ref, onBeforeMount, onMounted, onUpdated, computed, defineComponent, watch, onUnmounted, inject } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import setPostions from '@/utils/setPositions';
import debounce from '@/utils/debounce';
import { Picture as IconPicture } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router';
const router = useRouter();

import {useGlobalStore} from '@/store/globalStore'
const globalStore = useGlobalStore()

const props = defineProps({
    images: {
        type: Array,
        required: true,
        default: () => [],
    },
})

const deSetPositions = debounce(() => {
    setPostions(200, 20, 'PicWaterfallFlow');
}, 300);

onMounted(() => {
    window.addEventListener('resize', deSetPositions);
    // 初始化 linkVisibility 对象，假设 images 的长度为 images.length
    // props.images.forEach((_, index) => {
    //     linkVisibility.value[index] = true;
    // });
})

onUnmounted(() => {
    window.removeEventListener('resize', deSetPositions);
})

function handleLoad(index) {
    setPostions(200, 20, 'PicWaterfallFlow');
}

// const handleImageError = (index) => {
// 当图片加载失败时，设置对应索引的 linkVisibility 为 false
// linkVisibility.value[index] = false;
// setPostions(200, 20, 'PicWaterfallFlow');
// };
const activeIndex = ref(0); // 用于跟踪当前鼠标悬停的链接索引
// const linkVisibility = ref({}); // 控制每个链接是否显示的对象

function handleMouseOver(index) {
    activeIndex.value = index;
}
function handleMouseLeave(index) {
    activeIndex.value = null;
}

// 项目详情
// const SearchProInfo = inject('SearchProInfo');
function handleClick(url) {

    const startIndex = url.lastIndexOf("/") + 1; // 找到最后一个'/'字符的索引，并加1以指向下一个字符
    const endIndex = url.lastIndexOf("\\"); // 找到最后一个'\'字符的索引
    const parts = url.split('\\');
    const projectName = parts[1];

    const projectPath = url.substring(startIndex, endIndex);
    const newUrl_1k = url.replace("static_200", "static_1");

    // console.log(url)
    globalStore.fecthMore = false
    router.push({
        path: '/proInfoView',
        query: {
            projectName,
            projectPath,
            newUrl_1k,
        }
    });
}

</script>
<template>
    <div class="PicWaterfallFlow-container">
        <!-- <el-button @click="handleClick"></el-button> -->
        <div class="PicWaterfallFlow" id="PicWaterfallFlow" v-if="images.length > 0">
            <div v-for="(url, index)  in images" :key="url">
                <el-link href="" target="" @mouseover="handleMouseOver(index)" @mouseleave="handleMouseLeave(index)"
                    :class="{ 'with-overlay': activeIndex === index }" :underline="false" @click="handleClick(url)">
                    <el-image :src="url" @load="handleLoad(index)" lazy />
                    <div class="overlay" v-if="activeIndex === index">
                        项目详情
                    </div>
                </el-link>
                <!-- <div class="describle">特征</div> -->
            </div>

            <!-- <img v-for="(url, index)  in images" :key="url" :src="url" @load="handleLoad(index)"
                @error="handleError">
            </img> -->

        </div>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "@/styles/var.less";

.PicWaterfallFlow-container {
    .PicWaterfallFlow {
        position: relative;
        overflow: hidden;

        // height: 400px;
        // background-color: rgb(216, 255, 242);
        .el-link {
            display: block;

            .el-image {
                width: 200px;
                height: auto;
                // position: absolute;

                box-shadow: 5px 5px 10px 0 rgba(0, 0, 0, 0.5);
                border-radius: 5%;
                // margin: 5px;
                transition: all 0.35s ease;

                .placeholder_image-slot {
                    width: 200px;
                    height: 500px;
                    background-color: white;
                }
            }
        }

        .describle {
            text-align: center;
            margin: 10px;
            font-size: 12px;
        }

        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            /* 灰色透明蒙版 */
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .with-overlay .overlay {
            opacity: 1;
            border-radius: 5%;
        }

    }
}
</style>
