<template>
  <div id="app">
    <!-- Authenticated layout -->
    <template v-if="authStore.isAuthenticated">
      <Sidebar />
      <div class="main-content">
        <Header />
        <div class="page-content">
          <router-view />
        </div>
      </div>
      <RealtimeNotifications />
    </template>

    <!-- Unauthenticated layout (Login page) -->
    <template v-else>
      <router-view />
    </template>

    <!-- Toast notifications (always visible) -->
    <ToastContainer />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import RealtimeNotifications from './components/RealtimeNotifications.vue'
import ToastContainer from './components/ToastContainer.vue'

const authStore = useAuthStore()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f3f4f6;
  color: #1f2937;
}

#app {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.page-content {
  flex: 1;
  background: #f3f4f6;
  overflow-y: auto;
  overflow-x: hidden;
  height: calc(100vh - 70px);
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }

  .page-content {
    padding-top: 60px;
    height: calc(100vh - 130px);
  }
}
</style>
