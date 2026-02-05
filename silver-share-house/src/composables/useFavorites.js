import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useFavoritesStore } from '../stores/favorites'
import { houses } from '../data/houses'

export function useFavorites() {
  const favoritesStore = useFavoritesStore()
  const { favoriteIds, favoriteCount, isFavorite } = storeToRefs(favoritesStore)

  const favoriteHouses = computed(() => {
    return houses.filter(house =>
      isFavorite.value(house.id)
    )
  })

  return {
    favoriteIds,
    favoriteCount,
    favoriteHouses,
    isFavorite: (houseId) => isFavorite.value(houseId),
    toggleFavorite: favoritesStore.toggleFavorite,
    clearFavorites: favoritesStore.clearFavorites
  }
}
