import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layout/Index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '首页', icon: 'el-icon-s-home' }
      },
      {
        path: 'pets',
        name: 'Pets',
        component: () => import('@/views/pets/List.vue'),
        meta: { title: '宠物管理', icon: 'el-icon-dog' }
      },
      {
        path: 'pets/:id',
        name: 'PetDetail',
        component: () => import('@/views/pets/Detail.vue'),
        meta: { title: '宠物详情', icon: 'el-icon-dog', hidden: true }
      }
    ]
  },
  {
    path: '/medical-records/:recordId',
    component: Layout,
    children: [
      {
        path: 'detail',
        name: 'MedicalRecordDetail',
        component: () => import('@/views/medical-records/Detail.vue'),
        meta: { title: '病历详情', icon: 'el-icon-document', hidden: true }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes
})

export default router
