import { create } from 'zustand'
import { Toast } from '@/types'

interface ToastStore {
  toasts: Toast[]
  addToast: (toast: Toast) => void
  removeToast: (id: string) => void
  clearToasts: () => void
}

export const useToastStore = create<ToastStore>((set) => ({
  toasts: [],

  addToast: (toast: Toast) =>
    set((state) => ({
      toasts: [...state.toasts, toast],
    })),

  removeToast: (id: string) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),

  clearToasts: () =>
    set({
      toasts: [],
    }),
}))
