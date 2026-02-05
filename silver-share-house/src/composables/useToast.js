import { useToastStore } from '../stores/toast'

export function useToast() {
  const toastStore = useToastStore()

  return {
    success: (message, duration) => toastStore.success(message, duration),
    error: (message, duration) => toastStore.error(message, duration),
    warning: (message, duration) => toastStore.warning(message, duration),
    info: (message, duration) => toastStore.info(message, duration),
    toast: (message, type, duration) => toastStore.addToast(message, type, duration)
  }
}
