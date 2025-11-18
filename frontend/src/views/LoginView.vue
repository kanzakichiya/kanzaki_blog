<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth' // 1. 导入 Pinia Store

const username = ref('')
const password = ref('')
const errorMsg = ref(null) // 用于显示错误信息
const isLoading = ref(false)

const router = useRouter()
const authStore = useAuthStore() // 2. 获取 Store 实例

const handleLogin = async () => {
  isLoading.value = true
  errorMsg.value = null

  // 重点：FastAPI 的 OAuth2PasswordRequestForm 需要 "form-urlencoded" 格式
  // 而不是 JSON! 我们需要用 URLSearchParams 来构建 body。
  const body = new URLSearchParams()
  body.append('username', username.value)
  body.append('password', password.value)

  try {
    const response = await fetch('/api/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: body
    })

    const data = await response.json()

    if (response.ok) {
      // 3. 登录成功！
      // 调用 Pinia Action 存储 token 和用户名
      authStore.login(data.access_token, username.value) 
      
      // 4. 跳转回首页
      router.push('/')
    } else {
      // 登录失败 (例如 "用户名或密码错误")
      errorMsg.value = data.detail || '登录失败'
    }
  } catch (error) {
    console.error('登录请求异常:', error)
    errorMsg.value = '无法连接到服务器'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <form class="login-form" @submit.prevent="handleLogin">
      <h1>管理员登录</h1>
      
      <div class="form-group">
        <label for="username">用户名</label>
        <input 
          id="username" 
          type="text" 
          v-model="username" 
          required 
          autocomplete="username"
        />
      </div>
      
      <div class="form-group">
        <label for="password">密码</label>
        <input 
          id="password" 
          type="password" 
          v-model="password" 
          required 
          autocomplete="current-password"
        />
      </div>
      
      <div v-if="errorMsg" class="error-message">
        {{ errorMsg }}
      </div>
      
      <button type:="submit" class="btn-login" :disabled="isLoading">
        {{ isLoading ? '登录中...' : '登录' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 100px;
  min-height: 80vh;
}

.login-form {
  width: 100%;
  max-width: 400px;
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  border: 1px solid #eee;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--trans-blue);
  box-shadow: 0 0 0 3px rgba(91, 206, 250, 0.2);
}

.error-message {
  color: #ff4d4f;
  background: #fff0f0;
  border: 1px solid #ffccc7;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-login {
  width: 100%;
  padding: 14px;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  background: linear-gradient(90deg, var(--trans-blue), var(--trans-pink));
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-login:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(91, 206, 250, 0.3);
}

.btn-login:disabled {
  background: #ccc;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
