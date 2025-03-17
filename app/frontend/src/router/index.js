import { createRouter, createWebHashHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import HomePage from '../components/HomePage.vue';
import Registration from '../components/Registration.vue';
import Login from '../components/Login.vue'
import Dashboard from '@/components/dashboard/Main.vue';

const routes = [
  {
    path: '/hello',
    name: 'HelloWorld',
    component: HelloWorld,
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    // meta: {requiresAuth: true}
  },
  
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
})


router.beforeEach((to, from) => {
  const token = localStorage.getItem('token');
  if (to.name === "Login" && token) {
    return {name: 'Dashboard', replace: true};
  }
  if (to.matched.some((route) => route.meta.requiresAuth)) {
    if (token) {
      // User is authenticated
      return
    } else {
      // User is not authenticated; redirect to login
      return {name: 'Login'}
    }
  } else {
    // Allow access to non-protected routes
    // next();
  }
});

export default router
