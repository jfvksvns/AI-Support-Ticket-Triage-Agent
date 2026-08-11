import { useState, useEffect } from 'react'
import { useApi } from '@/hooks/useApi'
import { StatisticsCards } from '@/components/StatisticsCards'
import { Charts } from '@/components/Charts'
import { Statistics } from '@/services/api'

/**
 * Dashboard page with statistics and charts
 */
export function DashboardPage() {
  const { getStatistics, isLoading } = useApi()
  const [statistics, setStatistics] = useState<Statistics | null>(null)

  useEffect(() => {
    const fetchStatistics = async () => {
      const result = await getStatistics()
      if (result) {
        setStatistics(result)
      }
    }

    fetchStatistics()
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchStatistics, 30000)
    return () => clearInterval(interval)
  }, [getStatistics])

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white">
          Dashboard
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Real-time overview of your support tickets
        </p>
      </div>

      {/* Statistics Cards */}
      <StatisticsCards statistics={statistics} isLoading={isLoading} />

      {/* Charts */}
      <Charts statistics={statistics} isLoading={isLoading} />

      {/* Footer Note */}
      <div className="text-sm text-slate-600 dark:text-slate-400 italic">
        Dashboard data auto-refreshes every 30 seconds
      </div>
    </div>
  )
}
