<script setup>

import { RouterLink, RouterView } from 'vue-router'

import AIChat from '@/components/AIChat.vue'
import Layout from '@/components/Layout.vue'
import Header from '@/components/Header.vue'

</script>

<template>
  <div>
    <Layout>
      <template #header>
        <div class="header">
          <Header />
        </div>
      </template>
      <template #main>
        <div class="main">
          <RouterView />
        </div>
      </template>
    </Layout>
    <AIChat />
  </div>
</template>
