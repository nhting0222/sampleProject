<template>
  <div class="house-card">
    <div class="card-image">
      <img :src="house.image" :alt="house.name" />
      <div class="card-badge">{{ house.location }}</div>
      <button
        class="favorite-btn"
        :class="{ active: isFavorite(house.id) }"
        @click="handleToggleFavorite"
        :title="isFavorite(house.id) ? '즐겨찾기 해제' : '즐겨찾기 추가'"
      >
        {{ isFavorite(house.id) ? '❤️' : '🤍' }}
      </button>
    </div>

    <div class="card-content">
      <h3>{{ house.name }}</h3>
      <p class="description">{{ house.description }}</p>

      <div class="card-info">
        <div class="info-item">
          <span class="icon">🛏️</span>
          <span>{{ house.rooms }}개 객실</span>
        </div>
        <div class="info-item">
          <span class="icon">👥</span>
          <span>최대 {{ house.maxPeople }}명</span>
        </div>
      </div>

      <div class="card-footer">
        <div class="price">
          <span class="price-value">{{ house.price }}</span>
        </div>
        <router-link :to="`/house/${house.id}`" class="btn-detail">
          자세히 보기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFavorites } from '../composables/useFavorites'
import { useToast } from '../composables/useToast'

const props = defineProps({
  house: {
    type: Object,
    required: true
  }
})

const { isFavorite, toggleFavorite } = useFavorites()
const toast = useToast()

const handleToggleFavorite = (e) => {
  e.preventDefault()
  const isNowFavorite = toggleFavorite(props.house.id)

  if (isNowFavorite) {
    toast.success(`${props.house.name}을(를) 즐겨찾기에 추가했습니다`, 2000)
  } else {
    toast.info(`${props.house.name}을(를) 즐겨찾기에서 제거했습니다`, 2000)
  }
}
</script>

<style scoped>
.house-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.house-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 25px rgba(0,0,0,0.15);
}

.card-image {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.house-card:hover .card-image img {
  transform: scale(1.05);
}

.card-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255,255,255,0.95);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #667eea;
}

.favorite-btn {
  position: absolute;
  top: 15px;
  left: 15px;
  width: 45px;
  height: 45px;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.favorite-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.favorite-btn.active {
  animation: heartBeat 0.3s ease;
}

@keyframes heartBeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.card-content {
  padding: 1.5rem;
}

.card-content h3 {
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  color: #333;
}

.description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  border-top: 1px solid #e9ecef;
  border-bottom: 1px solid #e9ecef;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.95rem;
}

.icon {
  font-size: 1.2rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.btn-detail {
  padding: 10px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: transform 0.3s;
}

.btn-detail:hover {
  transform: translateX(3px);
}
</style>
