import { useCallback } from 'react'
import { useToastStore } from '@/store/toastStore'
import { Toast, ToastType } from '@/types'

/**
 * Hook for managing toast notifications
 */
export function useToast() {
  const { addToast, removeToast } = useToastStore()

  const showToast = useCallback(
    (message: string, type: ToastType = 'info', duration: number = 4000) => {
      const id = Date.now().toString()
      const toast: Toast = {
        id,
        message,
        type,
        duration,
      }

      addToast(toast)

      if (duration > 0) {
        setTimeout(() => {
          removeToast(id)
        }, duration)
      }

      return id
    },
    [addToast, removeToast]
  )

  const removeToastById = useCallback(
    (id: string) => {
      removeToast(id)
    },
    [removeToast]
  )

  return { showToast, removeToast: removeToastById }
}
