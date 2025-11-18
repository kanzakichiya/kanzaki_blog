<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isScrolled = ref(false)
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
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
      
      <RouterLink to="/" class="logo-icon">
        <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="18" stroke="#5BCEFA" stroke-width="3" stroke-opacity="0.3"/><circle cx="20" cy="20" r="10" fill="#F5A9B8"/><path d="M35 20C35 28.2843 28.2843 35 20 35" stroke="#5BCEFA" stroke-width="3" stroke-linecap="round"/><circle cx="28" cy="12" r="4" fill="#5BCEFA"/></svg>
      </RouterLink>

      <div class="nav-links">
        <RouterLink to="/" class="nav-link-text">首页</RouterLink>
        <RouterLink to="/tags" class="nav-link-text">分类</RouterLink>
        
        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/create" class="btn-nav">写文章</RouterLink>
          <button @click="handleLogout" class="btn-logout">退出登录</button>
        </template>
        
        <template v-else>
          <RouterLink to="/login" class="btn-nav login">登录</RouterLink>
        </template>
        
      </div>
    </div>
  </nav>

  <main>
    <RouterView />
  </main>

  <footer>
    <div class="footer-content">
      <p>&copy; 2025 Kanzaki Chiya. Made with <span class="heart">❤</span> and Vue 3.</p>
    </div>
  </footer>
</template>

<style>
/* --- 全局变量 (保持不变) --- */
:root {
  --trans-blue: #5BCEFA;
  --trans-pink: #F5A9B8;
  --text-main: #2c3e50;
  --text-light: #666;
  --bg-page: #ffffff;
  --bg-soft: #f9fafb;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg-page);
  color: var(--text-main);
  line-height: 1.6;
}

/* --- 导航栏 (保持不变) --- */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  padding: 1.2rem 5%;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  z-index: 1000;
  transition: all 0.3s ease;
}
.navbar.scrolled {
  padding: 0.8rem 5%;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo-icon {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: transform 0.3s ease;
}
.logo-icon:hover {
  transform: rotate(15deg) scale(1.1);
}

/* --- 
  CSS 修复：
  分离“文本链接”和“按钮链接”的样式
--- */

.nav-links { 
  display: flex; 
  gap: 1.5rem;
  align-items: center;
}

/* 1. 基础链接样式 (只管字体和过渡) */
.nav-links a {
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s, border-color 0.3s, transform 0.2s, box-shadow 0.2s;
  /* 关键修复：
    移除了这里的 padding 和 border-bottom！
  */
}

/* 2. 仅“文本链接” (.nav-link-text) */
.nav-link-text {
  color: var(--text-main);
  padding: 5px 0; /* padding 只在这里 */
  border-bottom: 2px solid transparent; /* border 只在这里 */
}
.nav-link-text:hover { 
  color: var(--trans-pink); 
}

/* 3. 激活的“文本链接” */
.nav-link-text.router-link-active {
  color: var(--trans-blue);
  font-weight: 600;
  border-bottom: 2px solid var(--trans-blue);
}

/* 4. “按钮链接” (.btn-nav) (现在它的 padding 不会再被覆盖了) */
.btn-nav {
  padding: 8px 20px; /* 现在这个会生效了！ */
  background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink));
  color: white !important; 
  border-radius: 50px;
  font-weight: bold;
  display: inline-block;
}
.btn-nav:hover { 
  transform: translateY(-2px); 
  opacity: 0.9; 
  color: white !important;
  box-shadow: 0 4px 12px rgba(91, 206, 250, 0.3);
}

/* 5. 激活的“按钮链接” (移除 border) */
.btn-nav.router-link-active {
  color: white !important;
  font-weight: bold;
  box-shadow: 0 0 10px rgba(91, 206, 250, 0.5), 0 0 10px rgba(245, 169, 184, 0.5);
  border-bottom: none !important; /* 确保没有下划线 */
}
/* --- 修复结束 --- */


/* 退出登录按钮 (保持不变) */
.btn-logout {
  background: none;
  border: 1px solid #ddd;
  color: #666;
  padding: 8px 20px;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}
.btn-logout:hover {
  border-color: #ff4d4f;
  color: #ff4d4f;
}

/* --- 页脚 (保持不变) --- */
footer {
  background: var(--bg-soft);
  padding: 3rem 2rem;
  text-align: center;
  margin-top: 4rem;
  color: var(--text-light);
  border-top: 1px solid #eee;
}
.heart { 
  color: var(--trans-pink); 
  display: inline-block;
  animation: pulse 1.5s infinite;
}
main { 
  min-height: 80vh;
}
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
</style>