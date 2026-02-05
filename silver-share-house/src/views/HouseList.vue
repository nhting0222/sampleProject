<template>
  <div class="house-list">
    <div class="page-header">
      <h1>실버 쉐어하우스 둘러보기</h1>
      <p>당신에게 맞는 완벽한 공간을 찾아보세요</p>
    </div>

    <div class="container">
      <!-- Search and Filter Section -->
      <div class="filter-section">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="🔍 하우스 이름이나 지역으로 검색..."
            class="search-input"
          />
        </div>

        <div class="filters">
          <select v-model="selectedLocation" class="filter-select">
            <option value="">모든 지역</option>
            <option v-for="location in locations" :key="location" :value="location">
              {{ location }}
            </option>
          </select>

          <select v-model="selectedPriceRange" class="filter-select">
            <option value="">모든 가격대</option>
            <option value="low">60만원 이하</option>
            <option value="mid">60만원 - 80만원</option>
            <option value="high">80만원 이상</option>
          </select>

          <select v-model="sortBy" class="filter-select">
            <option value="">정렬 기준</option>
            <option value="price-low">가격 낮은 순</option>
            <option value="price-high">가격 높은 순</option>
            <option value="rooms">객실 많은 순</option>
          </select>

          <button @click="resetFilters" class="reset-btn">
            초기화
          </button>
        </div>
      </div>

      <!-- Results Info -->
      <div class="results-info">
        <p>총 <strong>{{ filteredHouses.length }}</strong>개의 하우스</p>
      </div>

      <!-- Houses Grid -->
      <transition-group
        name="list"
        tag="div"
        class="houses-grid"
        v-if="filteredHouses.length > 0"
      >
        <HouseCard
          v-for="house in filteredHouses"
          :key="house.id"
          :house="house"
        />
      </transition-group>

      <!-- No Results -->
      <div class="no-results" v-else>
        <div class="no-results-icon">🔍</div>
        <h3>검색 결과가 없습니다</h3>
        <p>다른 조건으로 검색해보세요</p>
        <button @click="resetFilters" class="btn-reset">필터 초기화</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { houses } from '../data/houses'
import HouseCard from '../components/HouseCard.vue'

// Filter states
const searchQuery = ref('')
const selectedLocation = ref('')
const selectedPriceRange = ref('')
const sortBy = ref('')

// Get unique locations
const locations = computed(() => {
  return [...new Set(houses.map(h => h.location))]
})

// Parse price from string (e.g., "80만원/월" -> 80)
const parsePrice = (priceStr) => {
  return parseInt(priceStr.replace(/[^0-9]/g, ''))
}

// Filtered and sorted houses
const filteredHouses = computed(() => {
  let result = [...houses]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(house =>
      house.name.toLowerCase().includes(query) ||
      house.location.toLowerCase().includes(query) ||
      house.description.toLowerCase().includes(query)
    )
  }

  // Location filter
  if (selectedLocation.value) {
    result = result.filter(house => house.location === selectedLocation.value)
  }

  // Price range filter
  if (selectedPriceRange.value) {
    result = result.filter(house => {
      const price = parsePrice(house.price)
      if (selectedPriceRange.value === 'low') return price <= 60
      if (selectedPriceRange.value === 'mid') return price > 60 && price <= 80
      if (selectedPriceRange.value === 'high') return price > 80
      return true
    })
  }

  // Sorting
  if (sortBy.value) {
    result.sort((a, b) => {
      if (sortBy.value === 'price-low') {
        return parsePrice(a.price) - parsePrice(b.price)
      }
      if (sortBy.value === 'price-high') {
        return parsePrice(b.price) - parsePrice(a.price)
      }
      if (sortBy.value === 'rooms') {
        return b.rooms - a.rooms
      }
      return 0
    })
  }

  return result
})

// Reset all filters
const resetFilters = () => {
  searchQuery.value = ''
  selectedLocation.value = ''
  selectedPriceRange.value = ''
  sortBy.value = ''
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

/* Filter Section */
.filter-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.search-box {
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 14px 20px;
  font-size: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 50px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.filter-select {
  padding: 12px 16px;
  font-size: 0.95rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

.reset-btn {
  padding: 12px 24px;
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: #666;
  transition: all 0.3s;
}

.reset-btn:hover {
  background: #e9ecef;
  border-color: #dee2e6;
}

/* Results Info */
.results-info {
  margin-bottom: 2rem;
  color: #666;
}

.results-info strong {
  color: #667eea;
  font-size: 1.1rem;
}

/* Houses Grid */
.houses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

/* No Results */
.no-results {
  text-align: center;
  padding: 4rem 2rem;
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.no-results p {
  color: #666;
  margin-bottom: 2rem;
}

.btn-reset {
  padding: 12px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.3s;
}

.btn-reset:hover {
  transform: translateY(-2px);
}

/* List animations */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

@media (max-width: 768px) {
  .houses-grid {
    grid-template-columns: 1fr;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .filters {
    grid-template-columns: 1fr;
  }

  .filter-section {
    padding: 1.5rem;
  }
}
</style>
