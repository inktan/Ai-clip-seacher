import { createRouter, createWebHistory,createWebHashHistory } from 'vue-router'
import InspirationView from '@/views/InspirationView.vue'
import ProInfoView from '@/views/ProInfoView.vue'

import Search from '@/views/Search.vue'
import SearchByPic from '@/views/SearchByPic.vue'

const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL),
  history: createWebHashHistory(),

  routes: [
    {
      path: '/',
      name: 'home',
      component: InspirationView
    },
    {
      path: '/proInfoView',
      name: 'proInfoView',
      component: ProInfoView
    },
    {
      path: '/search',
      name: 'search',
      component: Search
    },
    {
      path: '/searchByPic',
      name: 'searchByPic',
      component: SearchByPic
    },
    {
      // path: '/about',
      // name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/About.vue')
    },
  ]
})

export default router
