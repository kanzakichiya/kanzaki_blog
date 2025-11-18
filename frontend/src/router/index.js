// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import HomeView from '../views/HomeView.vue'
import CreateView from '../views/CreateView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import LoginView from '../views/LoginView.vue'
import TagView from '../views/TagView.vue'
import TagIndexView from '../views/TagIndexView.vue' // 1. 导入新组件

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 公开页面
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/posts/:id', name: 'post-detail', component: PostDetailView },
    { path: '/tags', name: 'tag-index', component: TagIndexView }, // 2. 添加新路由 (列表)
    { path: '/tags/:id', name: 'tag-view', component: TagView }, // (详情)

    // 受保护页面
    { path: '/create', name: 'create', component: CreateView, meta: { requiresAuth: true } },
    { path: '/edit/:id', name: 'edit', component: CreateView, meta: { requiresAuth: true } },
  ]
})

// --- 4. 全局路由守卫 (核心) ---
router.beforeEach((to, from, next) => {
  // 在 Pinia 初始化之前，我们无法在顶层获取 store，
  // 所以我们必须在 beforeEach 内部获取它。
  const authStore = useAuthStore()

  // 检查目标路由是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 1. 未登录，且想去受保护的页面 -> 强制跳转到登录页
    next({ name: 'login' })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    // 2. 已登录，但又想去登录页 -> 强制跳回首页
    next({ name: 'home' })
  } else {
    // 3. 其他情况 (已登录或访问公开页) -> 正常放行
    next()
  }
})

export default router