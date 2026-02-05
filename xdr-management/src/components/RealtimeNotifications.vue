<template>
  <div>
    <!-- Connection Status Indicator -->
    <div class="connection-status" :class="{ connected: isConnected }">
      <span class="status-dot"></span>
      <span class="status-text">{{ isConnected ? 'Real-time Connected' : 'Connecting...' }}</span>
    </div>

    <!-- Notifications -->
    <div class="notifications-container">
      <transition-group name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
          :class="notification.type"
          @click="removeNotification(notification.id)"
        >
          <div class="notification-header">
            <span class="notification-icon">🔔</span>
            <span class="notification-title">{{ notification.title }}</span>
            <button class="notification-close" @click.stop="removeNotification(notification.id)">
              ×
            </button>
          </div>
          <div class="notification-body">
            {{ notification.message }}
          </div>
          <div class="notification-footer">
            {{ notification.timestamp }}
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useWebSocket } from '../composables/useWebSocket'
import dayjs from 'dayjs'

const notifications = ref([])
const WS_URL = 'ws://127.0.0.1:8000/ws'

const addNotification = (type, title, message) => {
  const notification = {
    id: Date.now() + Math.random(),
    type,
    title,
    message,
    timestamp: dayjs().format('HH:mm:ss')
  }

  notifications.value.unshift(notification)

  // Auto remove after 10 seconds
  setTimeout(() => {
    removeNotification(notification.id)
  }, 10000)

  // Keep only last 5 notifications
  if (notifications.value.length > 5) {
    notifications.value = notifications.value.slice(0, 5)
  }
}

const removeNotification = (id) => {
  notifications.value = notifications.value.filter(n => n.id !== id)
}

// Initialize WebSocket connection
const { isConnected, on } = useWebSocket(WS_URL)

// Listen for new events
on('new_event', (event) => {
  console.log('Received new event:', event)
  addNotification(
    event.severity,
    `New ${event.severity.toUpperCase()} Event`,
    `${event.type} detected on ${event.source}`
  )
})

// Listen for new incidents
on('new_incident', (incident) => {
  console.log('Received new incident:', incident)
  addNotification(
    incident.severity,
    'New Incident Created',
    incident.title
  )
})
</script>

<style scoped>
.connection-status {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #f59e0b;
  animation: pulse 2s infinite;
}

.connection-status.connected .status-dot {
  background: #10b981;
  animation: none;
}

.status-text {
  color: #6b7280;
  font-weight: 500;
}

.connection-status.connected .status-text {
  color: #10b981;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.notifications-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  width: 350px;
  max-width: 90vw;
}

.notification {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
  border-left: 4px solid #3b82f6;
  transition: all 0.3s ease;
}

.notification:hover {
  transform: translateX(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.notification.critical {
  border-left-color: #dc2626;
  background: #fef2f2;
}

.notification.high {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.notification.medium {
  border-left-color: #3b82f6;
  background: #eff6ff;
}

.notification.low {
  border-left-color: #10b981;
  background: #f0fdf4;
}

.notification-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.notification-icon {
  font-size: 1.2rem;
}

.notification-title {
  font-weight: 600;
  color: #1f2937;
  flex: 1;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.notification-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.notification-body {
  color: #4b5563;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.notification-footer {
  color: #9ca3af;
  font-size: 0.75rem;
}

/* Animation */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(-100px);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>
