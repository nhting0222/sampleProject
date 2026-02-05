import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import HouseList from '../views/HouseList.vue'
import HouseDetail from '../views/HouseDetail.vue'
import Contact from '../views/Contact.vue'
import Favorites from '../views/Favorites.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/houses',
    name: 'HouseList',
    component: HouseList
  },
  {
    path: '/house/:id',
    name: 'HouseDetail',
    component: HouseDetail
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: Favorites
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
