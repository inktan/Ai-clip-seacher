import { createStore } from 'vuex';
import setting from '././setting';
import banner from '././banner';

export default createStore({
    modules: {
        setting,
        banner,
    },
    strict: true,

});
