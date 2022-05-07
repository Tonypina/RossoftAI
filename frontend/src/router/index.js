import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'apriori',
    component: () => import('../views/recomendation/AprioriView.vue')
  },
  {
    path: '/metrics',
    name: 'metrics',
    component: () => import('../views/distance/MetricsView.vue')
  },
  {
    path: '/h-clust',
    name: 'h-clust',
    component: () => import('../views/clustering/HClustView.vue')
  },
  {
    path: '/p-clust',
    name: 'p-clust',
    component: () => import('../views/clustering/PClustView.vue')
  },
  {
    path: '/regression',
    name: 'regression',
    component: () => import('../views/classification/RegressionView.vue')
  },
  {
    path: '/a-prediction',
    name: 'a-prediction',
    component: () => import('../views/prediction/APredictionView.vue')
  },
  {
    path: '/a-classification',
    name: 'a-classification',
    component: () => import('../views/classification/AClassificationView.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
