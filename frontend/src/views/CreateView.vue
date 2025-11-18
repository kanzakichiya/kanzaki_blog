<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// --- 1. ByteMD 导入 ---
import { Editor } from '@bytemd/vue-next'
import gfm from '@bytemd/plugin-gfm'
import highlight from '@bytemd/plugin-highlight'

// --- 2. CSS 导入 ---
import 'bytemd/dist/index.css'
import 'highlight.js/styles/default.css'
import 'github-markdown-css/github-markdown-light.css'

// --- 3. 插件配置 ---
const plugins = [ gfm(), highlight() ]

// --- 4. 状态定义 ---
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isEditMode = computed(() => !!route.params.id)
const postId = route.params.id
const title = ref('')
const content = ref('')
const allTags = ref([])
const selectedTagIds = ref([])
const newTagName = ref('')
const isCreatingTag = ref(false)
const isSubmitting = ref(false)
const API_URL = '/api' // 基础 URL
const UPLOAD_URL = '/api/upload-image' // (在 handleUpload 中也修复)

// --- 5. 图片上传 ---
const handleUpload = async (files) => {
  const uploads = Array.from(files).map(async (file) => {
    if (file.size > 5 * 1024 * 1024) return null;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${API_URL}/upload-image`, {
        method: 'POST',
        headers: { ...authStore.authHeader },
        body: formData
      });
      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();
      return { url: data.url, alt: file.name };
    } catch (e) { console.error(e); return null; }
  });
  const results = await Promise.all(uploads);
  return results.filter(item => item !== null);
}

// --- 6. 标签 API: 获取 ---
const fetchAllTags = async () => {
  try {
    const res = await fetch(`${API_URL}/tags`)
    if (res.ok) allTags.value = await res.json()
  } catch (e) { console.error("获取标签失败:", e) }
}

// --- 7. 标签 API: 创建 ---
const handleCreateTag = async () => {
  if (!newTagName.value) return;
  if (allTags.value.some(tag => tag.name.toLowerCase() === newTagName.value.toLowerCase())) {
    alert("这个标签已经存在了！");
    newTagName.value = '';
    return;
  }
  isCreatingTag.value = true;
  try {
    const res = await fetch(`${API_URL}/tags`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authStore.authHeader },
      body: JSON.stringify({ name: newTagName.value })
    })
    if (res.ok) {
      const newTag = await res.json()
      allTags.value.push(newTag)
      selectedTagIds.value.push(newTag.id)
      newTagName.value = ''
    } else {
      const err = await res.json()
      alert(`创建失败: ${err.detail}`)
    }
  } catch (e) { alert("创建标签请求失败") } 
  finally { isCreatingTag.value = false; }
}

// --- 8. 标签 API: 删除 ---
const handleDeleteTag = async (tagId, tagName) => {
  if (!confirm(`确定要删除标签 "${tagName}" 吗？\n如果该标签正被文章使用，删除将失败。`)) return;
  try {
    const res = await fetch(`${API_URL}/tags/${tagId}`, {
      method: 'DELETE',
      headers: { ...authStore.authHeader }
    });
    if (res.ok) {
      allTags.value = allTags.value.filter(tag => tag.id !== tagId);
      selectedTagIds.value = selectedTagIds.value.filter(id => id !== tagId);
    } else {
      const err = await res.json();
      alert(`删除失败: ${err.detail}`);
    }
  } catch (e) {
    alert("删除请求失败");
  }
}

// --- 9. 页面加载逻辑 ---
onMounted(async () => {
  await fetchAllTags()
  if (isEditMode.value) {
    try {
      const res = await fetch(`${API_URL}/posts/${postId}`)
      if (res.ok) {
        const data = await res.json()
        title.value = data.title
        content.value = data.content
        selectedTagIds.value = data.tags.map(tag => tag.id)
      } else {
        alert("加载文章失败")
      }
    } catch (e) { console.error(e) }
  }
})

// --- 10. 提交文章 (创建/更新) ---
const submitPost = async () => {
  if (!title.value || !content.value) return alert("内容不能为空")
  isSubmitting.value = true
  const postData = {
    title: title.value,
    content: content.value,
    tags: selectedTagIds.value
  }
  try {
    const url = isEditMode.value ? `${API_URL}/posts/${postId}` : `${API_URL}/posts`
    const method = isEditMode.value ? 'PUT' : 'POST'
    const res = await fetch(url, {
      method: method,
      headers: { 
        'Content-Type': 'application/json',
        ...authStore.authHeader
      },
      body: JSON.stringify(postData)
    })
    if (res.ok) {
      if (isEditMode.value) router.push(`/posts/${postId}`)
      else router.push('/')
    } else {
       alert("提交失败，请检查是否登录。")
    }
  } catch (e) { console.error(e) } 
  finally { isSubmitting.value = false }
}
</script>

<template>
  <div class="create-page">
    <h1>{{ isEditMode ? '✏️ 编辑文章' : '✍️ 写新文章' }}</h1>
    
    <input v-model="title" placeholder="文章标题" class="input-title"/>
    
    <div class="tag-selector">
      <label>🏷️ 标签管理</label>
      <div class="tag-list">
        <span v-for="tag in allTags" :key="tag.id" class="tag-item">
          <input 
            type="checkbox"
            :id="'tag-' + tag.id"
            :value="tag.id"
            v-model="selectedTagIds"
          />
          <label :for="'tag-' + tag.id">
            <span>{{ tag.name }}</span>
            <button @click.prevent="handleDeleteTag(tag.id, tag.name)" class="btn-delete-tag">
              &times;
            </button>
          </label>
        </span>
      </div>
      
      <div class="tag-creator">
        <input 
          type="text"
          v-model="newTagName"
          placeholder="输入新标签名..."
          @keyup.enter="handleCreateTag" 
        />
        <button @click="handleCreateTag" :disabled="isCreatingTag">
          {{ isCreatingTag ? '...' : '+' }}
        </button>
      </div>
    </div>

    <div class="bytemd-editor-container">
      <Editor
        :value="content"
        :plugins="plugins"
        :upload-images="handleUpload"
        @change="(v) => (content = v)"
        placeholder="在这里输入 Markdown..."
      />
    </div>
    
    <div class="submit-container">
      <button @click="submitPost" :disabled="isSubmitting" class="btn-submit">
        {{ isSubmitting ? '提交中...' : (isEditMode ? '保存修改' : '发布文章') }}
      </button>
    </div>
  </div>
</template>

<style scoped>
/* --- 页面和标题 (保持不变) --- */
.create-page { 
  max-width: 1200px;
  margin: 0 auto; 
  padding: 100px 20px 40px;
}
.input-title { 
  width: 100%;
  padding: 12px; 
  margin-bottom: 20px;
  font-size: 1.2rem; 
  border: 1px solid #ddd; 
  border-radius: 8px; 
  outline: none; 
  transition: border 0.2s; 
}
.input-title:focus { 
  border-color: var(--trans-blue); 
}

/* --- 标签选择器 (保持不变) --- */
.tag-selector {
  margin-bottom: 20px;
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #eee;
}
.tag-selector > label {
  font-weight: bold;
  color: #555;
  display: block;
  margin-bottom: 10px;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

/* --- 
  CSS 修复：
  标签项和删除按钮的样式 
--- */
.tag-item {
  display: inline-block;
}

.tag-item input[type="checkbox"] { 
  display: none;
}

/* <label> 是我们的“按钮” */
.tag-item label {
  display: inline-flex;
  align-items: center;
  background: #fff; /* 默认白色背景 */
  border: 1px solid #ddd;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.tag-item label:hover {
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  border-color: #ccc;
}

/* 标签文本 */
.tag-item label span {
  padding: 5px 10px 5px 12px;
  white-space: nowrap;
  font-size: 0.9rem;
  transition: color 0.2s; /* 添加颜色过渡 */
}

/* 删除按钮 */
.btn-delete-tag {
  background: #fff; /* 关键：默认背景也是白色 */
  border: none;
  border-left: 1px solid #ddd; /* 垂直分割线 */
  padding: 5px 10px;
  cursor: pointer;
  color: #aaa;
  font-size: 1.1rem;
  font-weight: bold;
  line-height: 1;
  transition: all 0.2s;
}
.btn-delete-tag:hover {
  background: #ffeded;
  color: #ff4d4f;
}

/* --- 选中状态 --- */
.tag-item input[type="checkbox"]:checked + label {
  background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink));
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(91, 206, 250, 0.3);
}

/* 选中文本 (自动继承 color: white) */
.tag-item input[type="checkbox"]:checked + label span {
  /* background: transparent; 继承父元素的渐变 */
}

/* 选中删除按钮 */
.tag-item input[type="checkbox"]:checked + label .btn-delete-tag {
  background: transparent; /* 关键：背景透明，透出渐变色 */
  color: white;
  border-left: 1px solid rgba(255, 255, 255, 0.4); /* 分割线变亮 */
  opacity: 0.8;
}
.tag-item input[type="checkbox"]:checked + label .btn-delete-tag:hover {
  background: rgba(0, 0, 0, 0.2); /* 悬停时变暗 */
  opacity: 1;
}
/* --- 修复结束 --- */


/* --- 创建器 (保持不变) --- */
.tag-creator {
  display: flex;
  gap: 10px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}
.tag-creator input { flex-grow: 1; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; }
.tag-creator button { padding: 0 15px; font-size: 1.2rem; background: #fff; border: 1px solid #ccc; border-radius: 6px; cursor: pointer; color: var(--trans-blue); }

/* --- 编辑器 & 提交按钮 (保持不变) --- */
.bytemd-editor-container { height: 60vh; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }
:deep(.bytemd) { height: 100%; }
.submit-container { display: flex; justify-content: flex-end; margin-top: 20px; }
.btn-submit { background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink)); color: white; border: none; padding: 12px 40px; border-radius: 50px; cursor: pointer; font-size: 1rem; font-weight: bold; transition: transform 0.2s; }
.btn-submit:hover { transform: translateY(-2px); opacity: 0.9; }
</style>
