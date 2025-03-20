import { createRouter, createWebHistory } from 'vue-router';
import chat from './pages/chat.vue';
import upload from './pages/upload.vue';

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/upload', component: upload },
  { path: '/chat', component: chat },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
