import { createRouter, createWebHashHistory } from 'vue-router'
import AprioriView from '../views/AprioriView.vue'

const routes = [
  {
    path: '/',
    name: 'apriori',
    component: AprioriView
  },
  {
    path: '/metrics',
    name: 'metrics',
    component: () => import('../views/MetricsView.vue')
  },
  {
    path: '/h-clust',
    name: 'h-clust',
    component: () => import('../views/HClustView.vue')
  },
  {
    path: '/p-clust',
    name: 'p-clust',
    component: () => import('../views/PClustView.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
