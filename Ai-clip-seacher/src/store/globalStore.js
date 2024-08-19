import {defineStore} from "pinia";
export const useGlobalStore = defineStore ('globalStore',{
    state: ()=>({
        loading: false,
        // random_images:[],
        images:[], // 首页瀑布流显示的图片
        data: [],
        fecthMore: false,
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
