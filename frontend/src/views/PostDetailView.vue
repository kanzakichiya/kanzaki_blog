<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router' // 确保导入 RouterLink
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const post = ref(null)
const loading = ref(true)
const postId = route.params.id

// --- 获取文章详情 (公开) ---
const fetchPost = async () => {
  try {
    const res = await fetch(`/api/posts/${postId}`)
    if (res.ok) {
      post.value = await res.json()
    } else {
      alert("文章不存在")
      router.push('/')
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// --- 删除文章逻辑 (需要 Token) ---
const deletePost = async () => {
  if (!confirm('确定要删除这篇文章吗？删除后无法恢复！')) return
  try {
    const res = await fetch(`http://127.0.0.1:8081/posts/${postId}`, {
      method: 'DELETE',
      headers: { ...authStore.authHeader }
    })
    if (res.ok) {
      alert("删除成功")
      router.push('/')
    } else {
      if (res.status === 401) {
        alert("认证失败，请重新登录。")
        authStore.logout()
        router.push('/login')
      } else {
        alert("删除失败")
      }
    }
  } catch (error) {
    console.error("删除出错:", error)
    alert("网络错误")
  }
}

// --- Markdown 渲染 ---
const renderContent = (text) => {
  if (!text) return ''
  return DOMPurify.sanitize(marked.parse(text))
}

onMounted(fetchPost)
</script>

<template>
  <div class="detail-page">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>
    
    <div v-else-if="post" class="article-container">
      
      <div v-if="authStore.isAuthenticated" class="action-bar">
        <button @click="router.push('/')" class="btn-back">← 返回</button>
        <div class="right-actions">
          <button @click="router.push(`/edit/${postId}`)" class="btn-edit">
            ✏️ 编辑
          </button>
          <button @click="deletePost" class="btn-delete">
            🗑️ 删除
          </button>
        </div>
      </div>
      <div v-else class="action-bar">
        <button @click="router.push('/')" class="btn-back">← 返回</button>
      </div>

      <h1 class="title">{{ post.title }}</h1>
      
      <div class="meta">
        <span>📅 {{ new Date(post.created_at).toLocaleString() }}</span>
      </div>

      <div class="tags-container-detail">
        <RouterLink v-for="tag in post.tags" :key="tag.id" :to="'/tags/' + tag.id" class="tag-link">
          <span class="tag">
            🏷️ {{ tag.name }}
          </span>
        </RouterLink>
      </div>
      <hr class="divider" />

      <div class="markdown-body content" v-html="renderContent(post.content)"></div>
    </div>
  </div>
</template>

<style scoped>
.detail-page { 
  max-width: 800px; 
  margin: 0 auto; 
  padding: 100px 20px 40px; 
}

/* --- 加载动画 --- */
.loading { 
  display: flex; 
  justify-content: center; 
  padding: 50px; 
}
.spinner {
  width: 40px; 
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--trans-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { 
  0% { transform: rotate(0deg); } 
  100% { transform: rotate(360deg); } 
}

/* --- 操作栏 --- */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  min-height: 38px; 
}
.right-actions { 
  display: flex; 
  gap: 10px;
}
.btn-back {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  transition: color 0.2s;
}
.btn-back:hover { 
  color: var(--trans-blue); 
}
.btn-edit {
  background-color: white;
  color: var(--trans-blue);
  border: 1px solid var(--trans-blue);
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  font-weight: 500;
}
.btn-edit:hover {
  background-color: var(--trans-blue);
  color: white;
}
.btn-delete {
  background-color: #fff0f0;
  color: #ff4d4f;
  border: 1px solid #ffccc7;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  font-weight: 500;
}
.btn-delete:hover {
  background-color: #ff4d4f;
  color: white;
  border-color: #ff4d4f;
}

/* --- 文章内容 --- */
.title { 
  font-size: 2.5rem; 
  color: #333; 
  margin-bottom: 10px; 
  line-height: 1.3; 
}
.meta { 
  color: #999; 
  font-size: 14px; 
  margin-bottom: 15px;
}

/* --- 新增：详情页标签样式 --- */
.tags-container-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
}
.tag-link {
  text-decoration: none;
}
.tags-container-detail .tag {
  background-color: #f0f9ff;
  color: var(--trans-blue);
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(91, 206, 250, 0.3);
  transition: all 0.2s;
}
.tags-container-detail .tag-link:hover .tag {
  background: rgba(91, 206, 250, 0.2);
  border-color: rgba(91, 206, 250, 0.5);
  box-shadow: 0 2px 4px rgba(91, 206, 250, 0.1);
}

.divider { 
  border: 0; 
  border-top: 1px solid #eee; 
  margin: 30px 0; 
}
.content { 
  line-height: 1.8; 
  font-size: 17px; 
  color: #2c3e50; 
}

/* Markdown 样式穿透 */
:deep(.markdown-body h2) {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-top: 30px;
}
:deep(.markdown-body img) { 
  max-width: 100%; 
  border-radius: 8px; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
}
:deep(.markdown-body pre) {
  background-color: #f6f8fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}
</style>
