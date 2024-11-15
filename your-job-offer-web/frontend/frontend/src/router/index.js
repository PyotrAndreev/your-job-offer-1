import { createRouter, createWebHashHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import HomePage from '../components/HomePage.vue';

const routes = [
  {
    path: '/hello',
    name: 'HelloWorld',
    component: HelloWorld,
  },
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
