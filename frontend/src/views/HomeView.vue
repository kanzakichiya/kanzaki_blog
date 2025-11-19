<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import { RouterLink } from 'vue-router'

const posts = ref([])
const blogTitle = ref('...')
const API_URL = '/api'

const fetchPosts = async () => {
  try {
    const res = await fetch(`${API_URL}/posts`)
    if (res.ok) posts.value = await res.json()
  } catch (e) { console.error(e) }
}

const fetchSiteConfig = async () => {
  try {
    const res = await fetch(`${API_URL}/config`)
    if (res.ok) {
      const data = await res.json()
      blogTitle.value = data.blog_title
    }
  } catch (e) { blogTitle.value = "My Blog" }
}

onMounted(() => {
  fetchPosts()
  fetchSiteConfig()
})

const getSummary = (text) => {
  if (!text) return ''
  const clean = text.replace(/[#*`>]/g, '').substring(0, 120)
  return clean + '...'
}
</script>

<template>
  <div class="home-view">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Hi, I'm <span class="text-gradient">{{ blogTitle }}</span></h1>
        <p class="hero-subtitle">记录技术与生活的碎片。</p>
        <div class="hero-actions">
          <a href="#posts" class="btn-scroll">开始阅读 ↓</a>
        </div>
      </div>
      <div class="bg-decoration"></div>
    </section>

    <section id="posts" class="posts-container">
      <div class="section-header">
        <h2>最新文章</h2>
      </div>

      <div v-if="posts.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p>暂时还没有文章，去写一篇吧！</p>
      </div>

      <div v-else class="post-grid">
        <article v-for="post in posts.slice().reverse()" :key="post.id" class="post-card">
          <div class="card-meta">
            <span class="post-date">{{ new Date(post.created_at).toLocaleDateString('zh-CN') }}</span>
            <div class="tags">
              <RouterLink v-for="tag in post.tags" :key="tag.id" :to="'/tags/' + tag.id" class="tag-pill">
                #{{ tag.name }}
              </RouterLink>
            </div>
          </div>

          <RouterLink :to="'/posts/' + post.id" class="card-content">
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-excerpt">{{ getSummary(post.content) }}</p>
          </RouterLink>

          <div class="card-footer">
            <RouterLink :to="'/posts/' + post.id" class="read-link">阅读全文 &rarr;</RouterLink>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view { width: 100%; }

/* Hero Section */
.hero-section {
  position: relative;
  height: 60vh; /* 稍微减小高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: #fff;
  overflow: hidden;
  margin-bottom: 2rem;
}
.hero-content { z-index: 2; padding: 20px; }
.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}
.text-gradient {
  background: linear-gradient(120deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-subtitle { font-size: 1.2rem; color: var(--text-light); margin-bottom: 2rem; }
.btn-scroll {
  color: var(--text-light);
  font-size: 0.9rem;
  border: 1px solid #e5e7eb;
  padding: 10px 24px;
  border-radius: 50px;
  transition: all 0.2s;
}
.btn-scroll:hover { border-color: var(--primary); color: var(--primary); }

/* 背景装饰圆球 */
.bg-decoration {
  position: absolute;
  top: -10%; right: -5%;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(91,206,250,0.1) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  z-index: 1;
}

/* Content Section */
.posts-container {
  max-width: 1000px; /* 限制最大宽度，增强阅读体验 */
  margin: 0 auto;
  padding: 0 20px 60px;
}
.section-header { margin-bottom: 2rem; border-left: 4px solid var(--primary); padding-left: 1rem; }
.section-header h2 { font-size: 1.5rem; color: var(--text-main); }

/* Grid Layout */
.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

/* Post Card Design */
.post-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid transparent;
}
.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
  border-color: rgba(91, 206, 250, 0.1);
}

/* Card Meta */
.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}
.post-date { color: #9ca3af; }
.tags { display: flex; gap: 8px; }
.tag-pill {
  background: #f3f4f6;
  color: #6b7280;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  transition: all 0.2s;
}
.tag-pill:hover { background: #e0f2fe; color: var(--primary); }

/* Card Body */
.card-content { display: block; flex-grow: 1; margin-bottom: 1.5rem; }
.post-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.75rem;
  line-height: 1.4;
}
.post-excerpt {
  font-size: 0.95rem;
  color: var(--text-light);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Card Footer */
.read-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary);
  transition: gap 0.2s;
}
.read-link:hover { text-decoration: underline; }

/* Empty State */
.empty-state { text-align: center; padding: 60px 0; color: var(--text-light); }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }

/* 移动端适配 */
@media (max-width: 640px) {
  .hero-title { font-size: 2.5rem; }
  .post-grid { grid-template-columns: 1fr; }
}
</style>