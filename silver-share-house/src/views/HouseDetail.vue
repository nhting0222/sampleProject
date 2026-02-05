<template>
  <div class="house-detail" v-if="house">
    <div class="detail-header">
      <img :src="house.image" :alt="house.name" />
      <div class="header-overlay">
        <div class="container">
          <h1>{{ house.name }}</h1>
          <p class="location">📍 {{ house.location }}</p>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="detail-content">
        <div class="main-info">
          <section class="info-section">
            <h2>소개</h2>
            <p>{{ house.description }}</p>
          </section>

          <section class="info-section">
            <h2>기본 정보</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">월 이용료</span>
                <span class="value">{{ house.price }}</span>
              </div>
              <div class="info-item">
                <span class="label">객실 수</span>
                <span class="value">{{ house.rooms }}개</span>
              </div>
              <div class="info-item">
                <span class="label">수용 인원</span>
                <span class="value">최대 {{ house.maxPeople }}명</span>
              </div>
              <div class="info-item">
                <span class="label">주소</span>
                <span class="value">{{ house.address }}</span>
              </div>
            </div>
          </section>

          <section class="info-section">
            <h2>제공 서비스</h2>
            <ul class="amenities-list">
              <li v-for="amenity in house.amenities" :key="amenity">
                ✅ {{ amenity }}
              </li>
            </ul>
          </section>
        </div>

        <div class="sidebar">
          <div class="contact-card">
            <h3>문의하기</h3>
            <p class="price">{{ house.price }}</p>

            <button
              class="btn-favorite"
              :class="{ active: isFavorite(house.id) }"
              @click="handleToggleFavorite"
            >
              {{ isFavorite(house.id) ? '❤️ 즐겨찾기 해제' : '🤍 즐겨찾기 추가' }}
            </button>

            <router-link to="/contact" class="btn-contact">입주 문의</router-link>
            <div class="contact-info">
              <p>📞 1588-1234</p>
              <p>⏰ 평일 09:00 - 18:00</p>
            </div>
          </div>
        </div>
      </div>

      <div class="back-button">
        <router-link to="/houses" class="btn-back">← 목록으로 돌아가기</router-link>
      </div>
    </div>
  </div>

  <div v-else class="not-found">
    <h2>하우스를 찾을 수 없습니다</h2>
    <router-link to="/houses">목록으로 돌아가기</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { houses } from '../data/houses'
import { useFavorites } from '../composables/useFavorites'
import { useToast } from '../composables/useToast'

const route = useRoute()
const house = ref(null)
const { isFavorite, toggleFavorite } = useFavorites()
const toast = useToast()

onMounted(() => {
  const houseId = parseInt(route.params.id)
  house.value = houses.find(h => h.id === houseId)
})

const handleToggleFavorite = () => {
  const isNowFavorite = toggleFavorite(house.value.id)

  if (isNowFavorite) {
    toast.success(`${house.value.name}을(를) 즐겨찾기에 추가했습니다`, 2000)
  } else {
    toast.info(`${house.value.name}을(를) 즐겨찾기에서 제거했습니다`, 2000)
  }
}
</script>

<style scoped>
.detail-header {
  position: relative;
  height: 400px;
  overflow: hidden;
}

.detail-header img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  color: white;
  padding: 40px 0;
}

.header-overlay h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.location {
  font-size: 1.2rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.detail-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 3rem;
  margin: 40px 0;
}

.main-info {
  flex: 1;
}

.info-section {
  margin-bottom: 3rem;
}

.info-section h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.info-section p {
  line-height: 1.8;
  color: #666;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.amenities-list {
  list-style: none;
  padding: 0;
}

.amenities-list li {
  padding: 0.8rem;
  margin-bottom: 0.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  font-size: 1.1rem;
}

.sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.contact-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  text-align: center;
}

.contact-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.price {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 1.5rem;
}

.btn-favorite {
  display: block;
  width: 100%;
  padding: 15px;
  background: white;
  color: #333;
  border: 2px solid #e9ecef;
  border-radius: 50px;
  font-weight: 600;
  margin-bottom: 1rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-favorite:hover {
  background: #f8f9fa;
  border-color: #dee2e6;
}

.btn-favorite.active {
  background: #fff0f0;
  border-color: #ef4444;
  color: #ef4444;
}

.btn-contact {
  display: block;
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 600;
  margin-bottom: 1.5rem;
  transition: transform 0.3s;
}

.btn-contact:hover {
  transform: translateY(-2px);
}

.contact-info {
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.contact-info p {
  margin: 0.5rem 0;
  color: #666;
}

.back-button {
  margin: 40px 0;
}

.btn-back {
  display: inline-block;
  padding: 12px 30px;
  background: #f8f9fa;
  color: #333;
  text-decoration: none;
  border-radius: 50px;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #e9ecef;
}

.not-found {
  text-align: center;
  padding: 100px 20px;
}

.not-found h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.not-found a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

@media (max-width: 768px) {
  .detail-content {
    grid-template-columns: 1fr;
  }

  .header-overlay h1 {
    font-size: 1.8rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }
}
</style>
