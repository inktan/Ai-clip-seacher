import { defineStore } from "pinia";
export const useGlobalStore = defineStore('globalStore', {
    state: () => ({
        loading: false,
        // random_images:[],
        images: [], // 首页瀑布流显示的图片
        // projectImages: [], // 首页瀑布流显示的图片

        rendering: true,
        realScene: true,
        imageUrl:'',

        data: [],
        fecth_random: true,
        fecth_ai: true,
        fecthMore_random: true,
        fecthMore_ai: true,
        // formData_ai: new FormData(),
        searchCount: 0,// 请求次数
        randomCount: 0,// 请求次数

        projectName: '', // 项目详情的名字请求次数
        projectPath: '', // 项目详情的路径请求次数
        newUrl_1k: '',// 项目详情的查看图片

    }),

    actions: {
        // 定义动作
        // increment(context) {
        //     context.commit('increment');
        // }
        async fetchBanner(ctx) {
            ctx.commit("setLoading", true);
            const resp = await userApi.login(payload.loginId, payload.loginPwd);
            // console.log(resp)
            ctx.commit("setUser", resp);
            ctx.commit("setLoading", false);
            return resp;
        },
        async whoAmI(ctx) {
            ctx.commit("setLoading", true);
            const resp = await userApi.whoAmI();
            ctx.commit("setUser", resp);
            ctx.commit("setLoading", false);
        },
        async loginOut(ctx,) {
            ctx.commit("setLoading", true);
            await userApi.loginOut();
            ctx.commit("setUser", null);
            ctx.commit("setLoading", null);
        }
    },
})
