import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'

// Mock the stores
vi.mock('../stores/auth', () => ({
  useAuthStore: () => ({
    login: vi.fn(),
    isAuthenticated: false,
    user: null,
    loading: false,
    error: null
  })
}))

describe('Login Component', () => {
  let wrapper
  let router

  beforeEach(() => {
    setActivePinia(createPinia())

    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/login', component: Login },
        { path: '/', component: { template: '<div>Dashboard</div>' } }
      ]
    })

    wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })
  })

  it('should render login form', () => {
    expect(wrapper.find('.login-card').exists()).toBe(true)
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('should render demo accounts', () => {
    const accounts = wrapper.findAll('.account')
    expect(accounts.length).toBe(3)
  })

  it('should fill demo credentials on click', async () => {
    const adminAccount = wrapper.findAll('.account')[0]
    await adminAccount.trigger('click')

    const usernameInput = wrapper.find('input#username')
    const passwordInput = wrapper.find('input#password')

    expect(usernameInput.element.value).toBe('admin')
    expect(passwordInput.element.value).toBe('admin123')
  })

  it('should have correct header text', () => {
    expect(wrapper.find('.login-header h1').text()).toBe('XDR Management')
    expect(wrapper.find('.login-header p').text()).toBe('Security Operations Platform')
  })

  it('should show role badges for demo accounts', () => {
    const roles = wrapper.findAll('.role')
    expect(roles[0].text()).toBe('Admin')
    expect(roles[1].text()).toBe('Analyst')
    expect(roles[2].text()).toBe('Viewer')
  })
})
