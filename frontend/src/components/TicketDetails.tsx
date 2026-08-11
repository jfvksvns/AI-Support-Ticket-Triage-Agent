import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useApi } from '@/hooks/useApi'
import { Ticket } from '@/services/api'
import { TicketStatus, TicketUrgency } from '@/types'
import {
  ArrowLeft,
  Calendar,
  User,
  Mail,
  Building,
  Tag,
  AlertCircle,
  CheckCircle2,
  Loader,
  Copy,
} from 'lucide-react'
import { useToast } from '@/hooks/useToast'
import { formatDistanceToNow } from 'date-fns'

const STATUS_OPTIONS: TicketStatus[] = [
  'Open',
  'Assigned',
  'In Progress',
  'Pending Human Review',
  'Resolved',
  'Closed',
]

const URGENCY_COLORS = {
  Low: 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200',
  Medium: 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200',
  High: 'bg-orange-100 dark:bg-orange-900/20 text-orange-800 dark:text-orange-200',
  Critical: 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200',
}

/**
 * Ticket details page component
 */
export function TicketDetails() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { getTicket, updateStatus, isLoading } = useApi()
  const { showToast } = useToast()
  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [selectedStatus, setSelectedStatus] = useState('')
  const [updating, setUpdating] = useState(false)

  useEffect(() => {
    const fetchTicket = async () => {
      if (id) {
        const result = await getTicket(Number(id))
        if (result) {
          setTicket(result)
          setSelectedStatus(result.status)
        }
      }
    }

    fetchTicket()
  }, [id, getTicket])

  const handleStatusChange = async (newStatus: string) => {
    if (!ticket) return

    setUpdating(true)
    const updated = await updateStatus(ticket.id, newStatus)
    setUpdating(false)

    if (updated) {
      setTicket(updated)
      setSelectedStatus(updated.status)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    showToast('Copied to clipboard!', 'success')
  }

  if (isLoading || !ticket) {
    return (
      <div className="flex items-center justify-center p-12">
        <Loader className="w-8 h-8 text-primary-600 animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/tickets')}
          className="flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Tickets
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Ticket Header */}
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-8">
            <div className="flex items-start justify-between gap-4 mb-6">
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
                  {ticket.subject}
                </h1>
                <p className="text-slate-600 dark:text-slate-400">
                  Ticket #{ticket.id}
                </p>
              </div>
              <span
                className={`inline-block px-4 py-2 rounded-full text-sm font-medium ${
                  URGENCY_COLORS[ticket.urgency as TicketUrgency]
                }`}
              >
                {ticket.urgency}
              </span>
            </div>

            {/* Description */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-2">
                Description
              </h3>
              <p className="text-slate-600 dark:text-slate-400 whitespace-pre-wrap">
                {ticket.description}
              </p>
            </div>

            {/* Reporter Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
              <div className="flex items-center gap-3">
                <User className="w-5 h-5 text-slate-400" />
                <div>
                  <p className="text-xs text-slate-600 dark:text-slate-400">
                    Reporter
                  </p>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">
                    {ticket.reporter_name}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-slate-400" />
                <div>
                  <p className="text-xs text-slate-600 dark:text-slate-400">
                    Email
                  </p>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">
                    {ticket.reporter_email}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Building className="w-5 h-5 text-slate-400" />
                <div>
                  <p className="text-xs text-slate-600 dark:text-slate-400">
                    Department
                  </p>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">
                    {ticket.department}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Calendar className="w-5 h-5 text-slate-400" />
                <div>
                  <p className="text-xs text-slate-600 dark:text-slate-400">
                    Created
                  </p>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">
                    {formatDistanceToNow(new Date(ticket.created_at), {
                      addSuffix: true,
                    })}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* AI Classification */}
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-8">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">
              AI Classification
            </h2>

            <div className="space-y-6">
              {/* Summary */}
              <div>
                <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-2">
                  Summary
                </h3>
                <p className="text-slate-600 dark:text-slate-400">
                  {ticket.summary}
                </p>
              </div>

              {/* Reasoning */}
              <div>
                <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-2">
                  Classification Reasoning
                </h3>
                <p className="text-slate-600 dark:text-slate-400">
                  {ticket.reasoning}
                </p>
              </div>

              {/* Suggested Response */}
              <div>
                <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-2">
                  Suggested Response
                </h3>
                <div className="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-4 text-slate-600 dark:text-slate-400">
                  <p className="whitespace-pre-wrap">{ticket.suggested_response}</p>
                  <button
                    onClick={() => copyToClipboard(ticket.suggested_response)}
                    className="mt-3 flex items-center gap-2 text-primary-600 dark:text-primary-400 hover:underline text-sm font-medium"
                  >
                    <Copy className="w-4 h-4" />
                    Copy response
                  </button>
                </div>
              </div>

              {/* Human Review Flag */}
              {ticket.requires_human_review && (
                <div className="flex items-center gap-3 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-yellow-800 dark:text-yellow-200">
                      Flagged for Human Review
                    </p>
                    <p className="text-sm text-yellow-700 dark:text-yellow-300">
                      This ticket requires manual review due to low confidence or ambiguous content
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status */}
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-6">
            <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">
              Status
            </h3>
            <select
              value={selectedStatus}
              onChange={(e) => handleStatusChange(e.target.value)}
              disabled={updating}
              className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg dark:bg-slate-700 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition disabled:opacity-50"
            >
              {STATUS_OPTIONS.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>

          {/* Classification Info */}
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-6 space-y-4">
            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">
                Category
              </p>
              <p className="text-sm font-medium text-slate-900 dark:text-white flex items-center gap-2">
                <Tag className="w-4 h-4" />
                {ticket.category}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">
                Assigned Team
              </p>
              <p className="text-sm font-medium text-slate-900 dark:text-white">
                {ticket.assigned_team}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">
                AI Confidence
              </p>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-primary-600 h-full transition-all"
                    style={{ width: `${ticket.confidence}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-slate-900 dark:text-white w-12">
                  {ticket.confidence}%
                </span>
              </div>
            </div>

            {ticket.confidence >= 70 && (
              <div className="flex items-center gap-2 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                <CheckCircle2 className="w-4 h-4 text-green-600 dark:text-green-400 flex-shrink-0" />
                <p className="text-xs text-green-700 dark:text-green-300 font-medium">
                  High confidence classification
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
