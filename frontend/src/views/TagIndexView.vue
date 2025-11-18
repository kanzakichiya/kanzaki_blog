<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const allTags = ref([])
const loading = ref(true)
const API_URL = '/api'

// 获取所有标签
const fetchAllTags = async () => {
  try {
    const res = await fetch(`${API_URL}/tags`)
    if (res.ok) {
      allTags.value = await res.json()
    }
  } catch (e) {
    console.error("获取标签失败:", e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchAllTags)
</script>

<template>
  <div class="tag-index-container">
    <div class="page-header">
      <h1>标签索引</h1>
      <p>点击标签查看该分类下的所有文章</p>
    </div>

    <div v-if="loading" class="empty-state">正在加载...</div>
    
    <div v-else class="tag-cloud">
      <RouterLink 
        v-for="tag in allTags" 
        :key="tag.id" 
        :to="'/tags/' + tag.id" 
        class="tag-link"
      >
        <span class="tag">
          🏷️ {{ tag.name }}
        </span>
      </RouterLink>
      <div v-if="allTags.length === 0" class="empty-state">
        还没有创建任何标签。
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag-index-container {
  max-width: 900px;
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
.page-header p {
  font-size: 1.1rem;
  color: #666;
  margin-top: 0.5rem;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  padding: 2rem;
}

.tag-link {
  text-decoration: none;
}
.tag {
  display: inline-block;
  background-color: #f0f9ff;
  color: var(--trans-blue);
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 500;
  border: 1px solid rgba(91, 206, 250, 0.3);
  transition: all 0.2s;
}
.tag-link:hover .tag {
  background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink));
  color: white;
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(91, 206, 250, 0.3);
}

.empty-state {
  text-align: center;
  color: #999;
  padding: 40px;
  font-size: 1.2rem;
}
</style>
