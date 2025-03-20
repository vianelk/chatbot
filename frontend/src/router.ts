import { createRouter, createWebHistory } from 'vue-router';
import chat from './pages/chat.vue';
import upload from './pages/upload.vue';

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/upload', component: chat },
  { path: '/chat', component: upload },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
