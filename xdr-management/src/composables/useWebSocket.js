import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket(url) {
  const socket = ref(null)
  const isConnected = ref(false)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5
  const reconnectDelay = 3000
  const listeners = new Map()

  const connect = () => {
    try {
      socket.value = new WebSocket(url)

      socket.value.onopen = () => {
        console.log('WebSocket connected')
        isConnected.value = true
        reconnectAttempts.value = 0
      }

      socket.value.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          console.log('WebSocket message received:', message)

          // Notify all listeners for this message type
          const typeListeners = listeners.get(message.type) || []
          typeListeners.forEach(callback => callback(message.data))

          // Also notify wildcard listeners
          const wildcardListeners = listeners.get('*') || []
          wildcardListeners.forEach(callback => callback(message))
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      socket.value.onclose = () => {
        console.log('WebSocket disconnected')
        isConnected.value = false

        // Attempt to reconnect
        if (reconnectAttempts.value < maxReconnectAttempts) {
          reconnectAttempts.value++
          console.log(`Reconnecting... (attempt ${reconnectAttempts.value}/${maxReconnectAttempts})`)
          setTimeout(() => connect(), reconnectDelay)
        } else {
          console.error('Max reconnection attempts reached')
        }
      }

      socket.value.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
    }
  }

  const disconnect = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
    }
  }

  const send = (data) => {
    if (socket.value && isConnected.value) {
      socket.value.send(typeof data === 'string' ? data : JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  const on = (type, callback) => {
    if (!listeners.has(type)) {
      listeners.set(type, [])
    }
    listeners.get(type).push(callback)
  }

  const off = (type, callback) => {
    if (listeners.has(type)) {
      const typeListeners = listeners.get(type)
      const index = typeListeners.indexOf(callback)
      if (index > -1) {
        typeListeners.splice(index, 1)
      }
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    send,
    on,
    off,
    connect,
    disconnect
  }
}
