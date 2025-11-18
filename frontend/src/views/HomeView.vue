<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { RouterLink } from 'vue-router' // 确保导入 RouterLink

const posts = ref([])
const API_URL = 'http://127.0.0.1:8081/posts'
const typingText = ref('')

// --- 获取文章列表 ---
const fetchPosts = async () => {
  try {
    const response = await fetch(API_URL)
    posts.value = await response.json()
  } catch (error) { console.error(error) }
}

// --- 摘要生成 ---
const getSummary = (text) => {
  if (!text) return '';
  const rawHtml = marked.parse(text)
  const cleanText = rawHtml.replace(/<[^>]+>/g, '') // 去掉 HTML 标签只留纯文本
  return cleanText.substring(0, 100) + (cleanText.length > 100 ? '...' : '')
}

// --- 打字机动画逻辑 ---
const startTyping = () => {
  const text = "全栈开发者 & 开源贡献者"
  let i = 0
  const timer = setInterval(() => {
    typingText.value += text.charAt(i)
    i++
    if (i > text.length) clearInterval(timer)
  }, 100)
}

onMounted(() => {
  fetchPosts()
  startTyping()
})
</script>

<template>
  <div class="home-container">
    
    <section class="hero">
      <div class="hero-content">
        <h1>Hi, I'm <span class="highlight">Kanzaki Chiya</span></h1>
        <p class="subtitle">{{ typingText }}<span class="cursor">|</span></p>
        <div class="hero-btns">
          <a href="#blog-section" class="btn primary">阅读博客</a>
          <a href="https://github.com" target="_blank" class="btn secondary">Github</a>
        </div>
      </div>
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
    </section>

    <section id="blog-section" class="content-section">
      <h2 class="section-title">最新文章</h2>
      
      <div v-if="posts.length === 0" class="empty-state">暂无文章，快去发布第一篇吧！</div>

      <div class="blog-grid">
        <article v-for="post in posts.slice().reverse()" :key="post.id" class="blog-card">
          
          <div class="card-header">
            <div class="tags-container">
              <RouterLink v-for="tag in post.tags" :key="tag.id" :to="'/tags/' + tag.id" class="tag-link">
                <span class="tag">
                  {{ tag.name }}
                </span>
              </RouterLink>
              <span v-if="post.tags.length === 0" class="tag-placeholder"></span>
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
    </section>

  </div>
</template>

<style scoped>
/* --- 1. Hero 区域样式 --- */
.hero {
  position: relative;
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: linear-gradient(135deg, #fefefe 0%, #f0f9ff 100%);
  overflow: hidden;
}
.hero-content { z-index: 2; }
h1 {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #2c3e50;
  letter-spacing: -1px;
}
.highlight {
  background: linear-gradient(120deg, var(--trans-blue), var(--trans-pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.subtitle {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 2rem;
  min-height: 1.5em;
}
.cursor { animation: blink 1s infinite; }
@keyframes blink { 50% { opacity: 0; } }
.hero-btns { display: flex; gap: 1rem; justify-content: center; }
.btn {
  padding: 12px 30px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}
.btn.primary {
  background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink));
  color: white;
  box-shadow: 0 10px 20px rgba(91, 206, 250, 0.3);
}
.btn.primary:hover { transform: translateY(-3px); box-shadow: 0 15px 30px rgba(91, 206, 250, 0.4); }
.btn.secondary {
  background: white;
  color: #666;
  border: 1px solid #eee;
}
.btn.secondary:hover { border-color: var(--trans-pink); color: var(--trans-pink); }
.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 1;
  opacity: 0.6;
  animation: float 10s infinite ease-in-out;
}
.shape-1 {
  width: 300px; height: 300px;
  background: var(--trans-blue);
  top: -50px; left: -100px;
}
.shape-2 {
  width: 400px; height: 400px;
  background: var(--trans-pink);
  bottom: -100px; right: -100px;
  animation-delay: -5s;
}
@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, 50px); }
}

/* --- 2. 博客列表样式 --- */
.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem;
}
.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}
.section-title::after {
  content: '';
  display: block;
  width: 50%;
  height: 4px;
  background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink));
  margin: 10px auto 0;
  border-radius: 2px;
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

/* --- 卡片头部样式 --- */
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

/* --- 新增：标签链接样式 --- */
.tag-link {
  text-decoration: none;
}
.tag {
  color: var(--trans-blue);
  font-weight: 600;
  background: rgba(91, 206, 250, 0.1);
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  transition: all 0.2s;
}
.tag-link:hover .tag {
  background: rgba(91, 206, 250, 0.3);
  box-shadow: 0 2px 4px rgba(91, 206, 250, 0.2);
}

/* --- 剩余卡片样式 --- */
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
.empty-state { text-align: center; color: #999; padding: 40px; }
</style>