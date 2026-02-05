<template>
  <div class="favorites">
    <div class="page-header">
      <h1>즐겨찾기</h1>
      <p>관심있는 하우스 목록</p>
    </div>

    <div class="container">
      <div v-if="favoriteHouses.length > 0">
        <div class="favorites-info">
          <p>총 <strong>{{ favoriteCount }}</strong>개의 하우스를 저장했습니다</p>
          <button @click="handleClearAll" class="btn-clear">모두 삭제</button>
        </div>

        <div class="houses-grid">
          <HouseCard
            v-for="house in favoriteHouses"
            :key="house.id"
            :house="house"
          />
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">💙</div>
        <h2>아직 저장한 하우스가 없습니다</h2>
        <p>마음에 드는 하우스를 찾아 ❤️ 버튼을 눌러보세요</p>
        <router-link to="/houses" class="btn-browse">하우스 둘러보기</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFavorites } from '../composables/useFavorites'
import { useToast } from '../composables/useToast'
import HouseCard from '../components/HouseCard.vue'

const { favoriteHouses, favoriteCount, clearFavorites } = useFavorites()
const toast = useToast()

const handleClearAll = () => {
  if (confirm('모든 즐겨찾기를 삭제하시겠습니까?')) {
    clearFavorites()
    toast.success('즐겨찾기가 모두 삭제되었습니다')
  }
}
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.favorites-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.favorites-info p {
  color: #666;
}

.favorites-info strong {
  color: #667eea;
  font-size: 1.1rem;
}

.btn-clear {
  padding: 10px 20px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-clear:hover {
  background: #dc2626;
  transform: translateY(-2px);
}

.houses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.empty-state h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.empty-state p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 2rem;
}

.btn-browse {
  display: inline-block;
  padding: 15px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 600;
  transition: transform 0.3s;
}

.btn-browse:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .houses-grid {
    grid-template-columns: 1fr;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .favorites-info {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
