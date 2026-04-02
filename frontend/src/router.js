import { createMemoryHistory, createRouter } from 'vue-router'

import MainView from './vues/MainView.vue'
import LoginView from './vues/LoginView.vue'
import AboutView from './vues/AboutView.vue'

const routes = [
  { path: '/', component: MainView },
  { path: '/login', component: LoginView },
  { path: '/about', component: AboutView },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router
