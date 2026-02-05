<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </div>
        <h1>XDR Management</h1>
        <p>Security Operations Platform</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter username"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter password"
            required
            :disabled="loading"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="loading">Logging in...</span>
          <span v-else>Login</span>
        </button>
      </form>

      <div class="demo-accounts">
        <p>Demo Accounts:</p>
        <div class="account-list">
          <div class="account" @click="fillDemo('admin', 'admin123')">
            <span class="role admin">Admin</span>
            <span class="credentials">admin / admin123</span>
          </div>
          <div class="account" @click="fillDemo('analyst', 'analyst123')">
            <span class="role analyst">Analyst</span>
            <span class="credentials">analyst / analyst123</span>
          </div>
          <div class="account" @click="fillDemo('viewer', 'viewer123')">
            <span class="role viewer">Viewer</span>
            <span class="credentials">viewer / viewer123</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}

const fillDemo = (user, pass) => {
  username.value = user
  password.value = pass
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

.login-card {
  background: #1e1e2d;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
}

.login-header h1 {
  color: #fff;
  font-size: 24px;
  margin: 0 0 8px;
}

.login-header p {
  color: #888;
  margin: 0;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #ccc;
  font-size: 14px;
  font-weight: 500;
}

.form-group input {
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: #2a2a3d;
  color: #fff;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.form-group input::placeholder {
  color: #666;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.login-btn {
  padding: 14px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.demo-accounts {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.demo-accounts > p {
  color: #888;
  font-size: 12px;
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.account-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.account {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #2a2a3d;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.account:hover {
  background: #3a3a4d;
}

.role {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.role.admin {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.role.analyst {
  background: rgba(234, 179, 8, 0.2);
  color: #eab308;
}

.role.viewer {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.credentials {
  color: #aaa;
  font-size: 13px;
  font-family: monospace;
}
</style>
