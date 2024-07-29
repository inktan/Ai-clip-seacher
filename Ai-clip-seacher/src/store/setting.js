import * as userApi from "@/api";
export default {
    namespaced: true,
    state: {
        loading: false,
        user: null,
    },
    mutations: {
        setLoading(state, payload) {
            state.loading = payload;
        },
        setUser(state, payload) {
            state.user = payload;
        }
    },
    actions: {
        // 定义动作
        // increment(context) {
        //     context.commit('increment');
        // }
        async login(ctx, payload) {
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
    getters: {
        // 定义获取器
        // doubleCount(state) {
        //     return state.count * 2;
        // }
        status(state) {
            if (state.loading) {
                return 'loading';
            } else if (state.user) {
                return "login";
            } else {
                return 'unlogin';
            }
        }
    }
}
