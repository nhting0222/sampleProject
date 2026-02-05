<template>
  <header class="header">
    <div class="container">
      <router-link to="/" class="logo">
        <span class="logo-icon">🏡</span>
        <span class="logo-text">실버쉐어하우스</span>
      </router-link>

      <nav class="nav">
        <router-link to="/" class="nav-link">홈</router-link>
        <router-link to="/houses" class="nav-link">하우스 둘러보기</router-link>
        <router-link to="/favorites" class="nav-link favorites-link">
          💙 즐겨찾기
          <span v-if="favoriteCount > 0" class="badge">{{ favoriteCount }}</span>
        </router-link>
        <router-link to="/contact" class="nav-link">문의하기</router-link>
      </nav>

      <button class="mobile-menu-btn" @click="toggleMenu">
        <span v-if="!menuOpen">☰</span>
        <span v-else>✕</span>
      </button>
    </div>

    <div class="mobile-nav" :class="{ open: menuOpen }">
      <router-link to="/" class="mobile-nav-link" @click="closeMenu">홈</router-link>
      <router-link to="/houses" class="mobile-nav-link" @click="closeMenu">하우스 둘러보기</router-link>
      <router-link to="/favorites" class="mobile-nav-link" @click="closeMenu">
        💙 즐겨찾기
        <span v-if="favoriteCount > 0" class="badge">{{ favoriteCount }}</span>
      </router-link>
      <router-link to="/contact" class="mobile-nav-link" @click="closeMenu">문의하기</router-link>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useFavorites } from '../composables/useFavorites'

const menuOpen = ref(false)
const { favoriteCount } = useFavorites()

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}
</script>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #333;
  font-weight: 700;
  font-size: 1.3rem;
}

.logo-icon {
  font-size: 1.8rem;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #666;
  font-weight: 500;
  transition: color 0.3s;
  padding: 0.5rem 0;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #667eea;
}

.favorites-link {
  position: relative;
}

.badge {
  position: absolute;
  top: -8px;
  right: -12px;
  background: #ef4444;
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 700;
  min-width: 18px;
  text-align: center;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.mobile-nav {
  display: none;
  background: white;
  border-top: 1px solid #e9ecef;
}

.mobile-nav.open {
  display: block;
}

.mobile-nav-link {
  display: block;
  padding: 1rem 20px;
  text-decoration: none;
  color: #666;
  font-weight: 500;
  border-bottom: 1px solid #e9ecef;
  transition: background 0.3s;
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  background: #f8f9fa;
  color: #667eea;
}

@media (max-width: 768px) {
  .nav {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }
}
</style>
