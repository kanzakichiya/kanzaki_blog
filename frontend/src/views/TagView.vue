<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const posts = ref([])
const tagInfo = ref(null)
const loading = ref(true)
const API_URL = '/api'

// --- 摘要生成 (和 HomeView 一样) ---
const getSummary = (text) => {
  if (!text) return '';
  const rawHtml = marked.parse(text)
  const cleanText = rawHtml.replace(/<[^>]+>/g, '')
  return cleanText.substring(0, 100) + (cleanText.length > 100 ? '...' : '')
}

// --- 获取数据 ---
const fetchData = async (tagId) => {
  loading.value = true
  posts.value = []
  tagInfo.value = null

  try {
    // 1. 获取标签信息 (e.g., "Python")
    const tagRes = await fetch(`${API_URL}/tags/${tagId}`)
    if (tagRes.ok) {
      tagInfo.value = await tagRes.json()
    } else {
      throw new Error('Tag not found')
    }

    // 2. 获取该标签下的文章
    const postsRes = await fetch(`${API_URL}/posts/by_tag/${tagId}`)
    if (postsRes.ok) {
      posts.value = await postsRes.json()
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchData(route.params.id)
})

// 监听路由变化 (例如从 /tags/1 切换到 /tags/2)
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchData(newId)
  }
})
</script>

<template>
  <div class="tag-view-container">
    
    <div class="page-header">
      <h1 v-if="tagInfo">
        标签: <span class="highlight">{{ tagInfo.name }}</span>
      </h1>
      <h1 v-else-if="loading">
        正在加载...
      </h1>
      <h1 v-else>
        未找到标签
      </h1>
    </div>

    <div class="content-section">
      <div v-if="loading" class="empty-state">正在加载文章...</div>
      <div v-else-if="posts.length === 0" class="empty-state">
        这个标签下还没有文章。
      </div>

      <div v-else class="blog-grid">
        <article v-for="post in posts.slice().reverse()" :key="post.id" class="blog-card">
          <div class="card-header">
            <div class="tags-container">
              <span v-for="tag in post.tags" :key="tag.id" class="tag">
                {{ tag.name }}
              </span>
            </div>
            <span class="date">{{ new Date(post.created_at).toLocaleDateString() }}</span>
          </div>
          <h3>
            <RouterLink :to="'/posts/' + post.id" class="post-title-link">
              {{ post.title }}
            </RouterLink>
          </h3>
          <p class="summary">{{ getSummary(post.content) }}</p>
          <RouterLink :to="'/posts/' + post.id" class="read-more">
            阅读全文 &rarr;
          </RouterLink>
        </article>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag-view-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 100px 20px 40px; /* 留出导航栏高度 */
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}
.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
}
.highlight {
  background: linear-gradient(120deg, var(--trans-blue), var(--trans-pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* --- 复用 HomeView 的文章列表样式 --- */
.content-section {
  padding: 0 2rem;
}
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}
.blog-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  border: 1px solid rgba(0,0,0,0.03);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}
.blog-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(91, 206, 250, 0.15);
  border-color: rgba(91, 206, 250, 0.3);
}
.card-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 1rem;
  align-items: center;
  min-height: 22px;
}
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.tag {
  color: var(--trans-blue);
  font-weight: 600;
  background: rgba(91, 206, 250, 0.1);
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
}
.blog-card h3 { margin-bottom: 1rem; font-size: 1.4rem; line-height: 1.4; }
.post-title-link { text-decoration: none; color: #2c3e50; transition: color 0.2s; }
.post-title-link:hover { color: var(--trans-pink); }
.summary { color: #666; line-height: 1.6; margin-bottom: 1.5rem; flex-grow: 1; }
.read-more {
  text-decoration: none;
  color: var(--trans-blue);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  transition: gap 0.2s;
}
.read-more:hover { gap: 5px; color: var(--trans-pink); }
.empty-state { text-align: center; color: #999; padding: 40px; font-size: 1.2rem; }
</style>
