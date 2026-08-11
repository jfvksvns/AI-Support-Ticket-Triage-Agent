import { Link } from 'react-router-dom'
import { AlertCircle } from 'lucide-react'

/**
 * 404 Not Found page
 */
export function NotFoundPage() {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <AlertCircle className="w-16 h-16 text-yellow-600 dark:text-yellow-400" />
        </div>
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-2">
          404
        </h1>
        <p className="text-xl text-slate-600 dark:text-slate-400 mb-8">
          Page not found
        </p>
        <Link
          to="/"
          className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
        >
          Go back to Dashboard
        </Link>
      </div>
    </div>
  )
}
