import { useToastStore } from '@/store/toastStore'
import { useToast } from '@/hooks/useToast'
import { X, AlertCircle, CheckCircle2, AlertTriangle, Info } from 'lucide-react'
import { Toast as ToastType } from '@/types'

/**
 * Toast notification component
 * Displays alerts and messages to the user
 */
export function ToastContainer() {
  const toasts = useToastStore((state) => state.toasts)
  const { removeToast } = useToast()

  if (toasts.length === 0) return null

  return (
    <div className="fixed bottom-0 right-0 p-4 space-y-2 z-50">
      {toasts.map((toast) => (
        <Toast key={toast.id} toast={toast} onClose={() => removeToast(toast.id)} />
      ))}
    </div>
  )
}

interface ToastProps {
  toast: ToastType
  onClose: () => void
}

function Toast({ toast, onClose }: ToastProps) {
  const bgColorMap: Record<string, string> = {
    success: 'bg-green-50 dark:bg-green-900/20',
    error: 'bg-red-50 dark:bg-red-900/20',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20',
    info: 'bg-blue-50 dark:bg-blue-900/20',
  }
  const bgColor = bgColorMap[toast.type] || bgColorMap.info

  const borderColorMap: Record<string, string> = {
    success: 'border-green-200 dark:border-green-800',
    error: 'border-red-200 dark:border-red-800',
    warning: 'border-yellow-200 dark:border-yellow-800',
    info: 'border-blue-200 dark:border-blue-800',
  }
  const borderColor = borderColorMap[toast.type] || borderColorMap.info

  const textColorMap: Record<string, string> = {
    success: 'text-green-800 dark:text-green-200',
    error: 'text-red-800 dark:text-red-200',
    warning: 'text-yellow-800 dark:text-yellow-200',
    info: 'text-blue-800 dark:text-blue-200',
  }
  const textColor = textColorMap[toast.type] || textColorMap.info

  const iconMap: Record<string, any> = {
    success: CheckCircle2,
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
  }
  const Icon = iconMap[toast.type] || iconMap.info

  return (
    <div
      className={`
        flex items-start gap-3 p-4 rounded-lg border animate-slide-in
        ${bgColor} ${borderColor} ${textColor} shadow-lg max-w-sm
      `}
    >
      <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
      <div className="flex-1 text-sm font-medium">{toast.message}</div>
      <button
        onClick={onClose}
        className="flex-shrink-0 hover:opacity-70 transition-opacity"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}
