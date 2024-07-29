import '@/styles/reset.css'
import '@/styles/global.less'
// import Mock from "mockjs"
// import "highlight.js/styles/github.css"; //实现代码高亮

import { createApp, h } from 'vue'
// import { showMessage } from '@/utils';
// import './mock'

import App from './App.vue'
// import App from './App-RightList.vue'
const app = createApp(App)

import store from './store';
app.use(store);

import router from './router'
app.use(router);

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

app.use(ElementPlus, { size: 'small', zIndex: 3000 })
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

// app.provide('$showMessage', showMessage);
app.mount('#app');



