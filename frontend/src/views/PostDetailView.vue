<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const post = ref(null)
const loading = ref(true)

const fetchPost = async () => {
  try {
    const res = await fetch(`/api/posts/${route.params.id}`)
    if (res.ok) post.value = await res.json()
    else router.push('/')
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const deletePost = async () => {
  if (!confirm('确定删除?')) return
  try {
    const res = await fetch(`/api/posts/${route.params.id}`, {
      method: 'DELETE',
      headers: { ...authStore.authHeader }
    })
    if (res.ok) router.push('/')
  } catch (e) { alert('Error') }
}

const renderContent = (text) => DOMPurify.sanitize(marked.parse(text || ''))
onMounted(fetchPost)
</script>

<template>
  <div class="detail-container">
    <div v-if="loading" class="loading-spinner"></div>
    
    <article v-else-if="post" class="article-wrapper">
      <div class="post-nav">
        <button @click="router.push('/')" class="btn-back">
          <span class="icon">←</span> 返回首页
        </button>
        <div v-if="authStore.isAuthenticated" class="admin-controls">
          <button @click="router.push(`/edit/${post.id}`)" class="btn-icon">✎</button>
          <button @click="deletePost" class="btn-icon delete">🗑</button>
        </div>
      </div>

      <header class="post-header">
        <div class="post-tags">
          <span v-for="tag in post.tags" :key="tag.id" class="hash-tag">#{{ tag.name }}</span>
        </div>
        <h1 class="post-h1">{{ post.title }}</h1>
        <div class="post-meta">
          <span class="date">发布于 {{ new Date(post.created_at).toLocaleDateString() }}</span>
        </div>
      </header>

      <div class="markdown-body" v-html="renderContent(post.content)"></div>
    </article>
  </div>
</template>

<style scoped>
.detail-container {
  background-color: #fff;
  min-height: 100vh;
}

.article-wrapper {
  max-width: 720px; /* 最佳阅读宽度 */
  margin: 0 auto;
  padding: 40px 20px 100px;
}

/* 顶部导航 */
.post-nav {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3rem;
}
.btn-back {
  background: none;
  border: none;
  color: var(--text-light);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background 0.2s;
}
.btn-back:hover { background: #f3f4f6; color: var(--text-main); }

.admin-controls { display: flex; gap: 10px; }
.btn-icon {
  width: 36px; height: 36px;
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 50%;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-light);
  transition: all 0.2s;
}
.btn-icon:hover { border-color: var(--primary); color: var(--primary); }
.btn-icon.delete:hover { border-color: #ef4444; color: #ef4444; }

/* 文章头部 */
.post-header { text-align: center; margin-bottom: 4rem; }
.post-tags { margin-bottom: 1rem; color: var(--primary); font-weight: 600; font-size: 0.9rem; }
.hash-tag { margin: 0 5px; }
.post-h1 {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
  color: #111;
  margin-bottom: 1rem;
}
.post-meta { color: var(--text-light); font-size: 0.9rem; }

/* 正文优化 */
.markdown-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #374151;
}

/* 针对 Markdown 内容的特定样式覆盖 */
:deep(h2) { margin-top: 3rem; margin-bottom: 1rem; font-size: 1.8rem; font-weight: 700; color: #111; }
:deep(p) { margin-bottom: 1.5rem; }
:deep(img) { border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 100%; }
:deep(blockquote) { border-left: 4px solid var(--primary); background: #f9fafb; padding: 1rem; color: var(--text-light); }
:deep(pre) { background: #1f2937 !important; border-radius: 8px; padding: 1.5rem; }
</style>