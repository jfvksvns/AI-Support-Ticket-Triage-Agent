import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Statistics } from '@/services/api'

interface ChartsProps {
  statistics: Statistics | null
  isLoading?: boolean
}

const COLORS = ['#0ea5e9', '#f59e0b', '#ef4444', '#8b5cf6', '#10b981', '#ec4899']

/**
 * Chart components for dashboard
 */
export function Charts({ statistics, isLoading }: ChartsProps) {
  if (isLoading || !statistics) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700 animate-pulse">
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-32 mb-4"></div>
          <div className="h-64 bg-slate-200 dark:bg-slate-700 rounded"></div>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700 animate-pulse">
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-32 mb-4"></div>
          <div className="h-64 bg-slate-200 dark:bg-slate-700 rounded"></div>
        </div>
      </div>
    )
  }

  // Prepare data for category pie chart
  const categoryData = Object.entries(statistics.category_distribution).map(([name, value]) => ({
    name,
    value,
  }))

  // Prepare data for urgency bar chart
  const urgencyData = [
    { name: 'Low', value: statistics.low_tickets },
    { name: 'Medium', value: statistics.medium_tickets },
    { name: 'High', value: statistics.high_tickets },
    { name: 'Critical', value: statistics.critical_tickets },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Category Distribution Pie Chart */}
      <div className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
          Tickets by Category
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={categoryData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {categoryData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Urgency Distribution Bar Chart */}
      <div className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
          Tickets by Urgency
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={urgencyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Team Distribution */}
      <div className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
          Tickets by Team
        </h3>
        <div className="space-y-3">
          {Object.entries(statistics.team_distribution).map(([team, count], index) => (
            <div key={team} className="flex items-center gap-4">
              <div
                className="w-3 h-3 rounded-full flex-shrink-0"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              ></div>
              <span className="text-sm text-slate-600 dark:text-slate-400 flex-1">
                {team}
              </span>
              <span className="font-semibold text-slate-900 dark:text-white">
                {count}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Status Distribution */}
      <div className="bg-white dark:bg-slate-800 rounded-lg p-6 border border-slate-200 dark:border-slate-700">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
          Tickets by Status
        </h3>
        <div className="space-y-3">
          {Object.entries(statistics.status_distribution).map(([status, count], index) => (
            <div key={status} className="flex items-center gap-4">
              <div
                className="w-3 h-3 rounded-full flex-shrink-0"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              ></div>
              <span className="text-sm text-slate-600 dark:text-slate-400 flex-1">
                {status}
              </span>
              <span className="font-semibold text-slate-900 dark:text-white">
                {count}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
