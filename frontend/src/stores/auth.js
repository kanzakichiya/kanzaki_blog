// frontend/src/stores/auth.js
import { defineStore } from 'pinia'

// 定义一个叫 'auth' 的储物柜 (store)
export const useAuthStore = defineStore('auth', {
  // 1. 状态 (数据)
  state: () => ({
    token: localStorage.getItem('token') || null, // 尝试从本地存储恢复 token
    username: localStorage.getItem('username') || null,
  }),

  // 2. Getters (计算属性，方便我们调用)
  getters: {
    // !!this.token 会把字符串(有值)或null(空)转换成 true/false
    isAuthenticated: (state) => !!state.token,
    
    // 返回 axios/fetch 需要的认证头
    authHeader: (state) => {
      return { 'Authorization': `Bearer ${state.token}` }
    }
  },

  // 3. Actions (方法，用于修改数据)
  actions: {
    // 登录成功后调用
    login(token, username) {
      this.token = token
      this.username = username
      
      // 把 token 存入 localStorage，防止刷新页面就丢失
      localStorage.setItem('token', token)
      localStorage.setItem('username', username)
    },

    // 退出登录时调用
    logout() {
      this.token = null
      this.username = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    },
  },
})