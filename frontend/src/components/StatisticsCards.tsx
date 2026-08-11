import { AlertTriangle, CheckCircle2, TrendingUp, AlertCircle } from 'lucide-react'
import { Statistics } from '@/services/api'

interface StatisticsCardsProps {
  statistics: Statistics | null
  isLoading?: boolean
}

/**
 * Statistics cards display key metrics
 */
export function StatisticsCards({ statistics, isLoading }: StatisticsCardsProps) {
  if (isLoading || !statistics) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700 animate-pulse">
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-24 mb-4"></div>
            <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-16"></div>
          </div>
        ))}
      </div>
    )
  }

  const cards = [
    {
      title: 'Total Tickets',
      value: statistics.total_tickets,
      icon: CheckCircle2,
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
    },
    {
      title: 'Critical Issues',
      value: statistics.critical_tickets,
      icon: AlertTriangle,
      color: 'text-red-600 dark:text-red-400',
      bgColor: 'bg-red-50 dark:bg-red-900/20',
    },
    {
      title: 'Avg Confidence',
      value: `${statistics.average_confidence}%`,
      icon: TrendingUp,
      color: 'text-green-600 dark:text-green-400',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
    },
    {
      title: 'Need Review',
      value: statistics.human_review_count,
      icon: AlertCircle,
      color: 'text-yellow-600 dark:text-yellow-400',
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <div
            key={card.title}
            className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400">
                  {card.title}
                </p>
                <p className="text-2xl font-bold text-slate-900 dark:text-white mt-2">
                  {card.value}
                </p>
              </div>
              <div className={`p-3 rounded-lg ${card.bgColor}`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
