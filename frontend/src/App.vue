<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="nav-container">
      <RouterLink to="/" class="logo-group">
        <div class="logo-icon">
          <svg width="32" height="32" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="18" stroke="currentColor" stroke-width="3" class="stroke-blue"/>
            <circle cx="20" cy="20" r="10" class="fill-pink"/>
            <circle cx="28" cy="12" r="4" class="fill-blue"/>
          </svg>
        </div>
        <span class="logo-text">Kanzaki<span class="highlight">.Blog</span></span>
      </RouterLink>

      <div class="nav-links">
        <RouterLink to="/" class="nav-item">首页</RouterLink>
        <RouterLink to="/tags" class="nav-item">标签</RouterLink>
        
        <div class="auth-actions">
          <template v-if="authStore.isAuthenticated">
            <RouterLink to="/create" class="btn-primary">写文章</RouterLink>
            <button @click="handleLogout" class="btn-text">退出</button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="btn-secondary">登录</RouterLink>
          </template>
        </div>
      </div>
    </div>
  </nav>

  <main>
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </main>

  <footer>
    <p>&copy; 2025 Kanzaki Chiya. <span class="separator">|</span> Designed with <span class="heart">❤</span></p>
  </footer>
</template>

<style>
/* --- 全局变量重构 --- */
:root {
  --primary: #5BCEFA;
  --primary-hover: #4ab8e3;
  --secondary: #F5A9B8;
  --text-main: #1f2937;
  --text-light: #6b7280;
  --bg-body: #f3f4f6;
  --bg-card: #ffffff;
  --nav-height: 70px;
  --radius-std: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: var(--bg-body);
  color: var(--text-main);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased; /* 字体抗锯齿 */
  -moz-osx-font-smoothing: grayscale;
}

a { text-decoration: none; color: inherit; transition: 0.2s; }

/* --- 导航栏优化 --- */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  height: var(--nav-height);
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px); /* 毛玻璃 */
  border-bottom: 1px solid rgba(0,0,0,0.05);
  z-index: 1000;
  transition: all 0.3s ease;
}
.navbar.scrolled {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  height: 100%;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Logo */
.logo-group {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--text-main);
}
.logo-icon svg { display: block; }
.stroke-blue { stroke: var(--primary); opacity: 0.8; }
.fill-pink { fill: var(--secondary); }
.fill-blue { fill: var(--primary); }
.highlight { color: var(--primary); }

/* 导航项 */
.nav-links { display: flex; gap: 2rem; align-items: center; }
.nav-item {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-light);
  position: relative;
}
.nav-item:hover, .nav-item.router-link-active { color: var(--primary); }

/* 按钮样式 */
.auth-actions { display: flex; gap: 1rem; align-items: center; margin-left: 1rem; }

.btn-primary {
  background: var(--primary);
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(91, 206, 250, 0.3);
}
.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-secondary {
  color: var(--text-main);
  font-weight: 500;
  font-size: 0.9rem;
}
.btn-secondary:hover { color: var(--primary); }

.btn-text {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-light);
  font-size: 0.9rem;
}
.btn-text:hover { color: #ef4444; }

/* --- 主内容区 --- */
main {
  padding-top: var(--nav-height);
  min-height: 85vh;
}

/* --- 页脚 --- */
footer {
  padding: 3rem 0;
  text-align: center;
  color: var(--text-light);
  font-size: 0.9rem;
  border-top: 1px solid rgba(0,0,0,0.05);
  background: #fff;
  margin-top: 4rem;
}
.separator { margin: 0 8px; opacity: 0.3; }
.heart { color: var(--secondary); display: inline-block; animation: pulse 1.5s infinite; }

/* --- 过渡动画 --- */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
</style>