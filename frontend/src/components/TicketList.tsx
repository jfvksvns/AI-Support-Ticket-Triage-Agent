import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useApi } from '@/hooks/useApi'
import { Ticket } from '@/services/api'
import { TicketUrgency, TicketCategory, TicketStatus } from '@/types'
import { Search, Filter, ChevronLeft, ChevronRight, Trash2, Eye, Loader } from 'lucide-react'

const URGENCY_COLORS = {
  Low: 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200',
  Medium: 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200',
  High: 'bg-orange-100 dark:bg-orange-900/20 text-orange-800 dark:text-orange-200',
  Critical: 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200',
}

const CATEGORY_OPTIONS: TicketCategory[] = [
  'Software',
  'Hardware',
  'Network',
  'Security',
  'Cloud',
  'Database',
  'Email',
  'Printer',
  'Access Management',
  'Other',
]

const URGENCY_OPTIONS: TicketUrgency[] = ['Low', 'Medium', 'High', 'Critical']

const STATUS_OPTIONS: TicketStatus[] = [
  'Open',
  'Assigned',
  'In Progress',
  'Pending Human Review',
  'Resolved',
  'Closed',
]

/**
 * Ticket list component with search, filter, sort, and pagination
 */
export function TicketList() {
  const { getTickets, deleteTicket, isLoading } = useApi()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [totalTickets, setTotalTickets] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({
    urgency: '',
    category: '',
    status: '',
  })
  const [showFilters, setShowFilters] = useState(false)
  const [deleteLoading, setDeleteLoading] = useState<number | null>(null)

  // Fetch tickets
  const fetchTickets = async () => {
    const skip = (currentPage - 1) * pageSize
    const result = await getTickets(skip, pageSize, {
      urgency: filters.urgency || undefined,
      category: filters.category || undefined,
      status: filters.status || undefined,
    })

    if (result) {
      setTickets(result.items)
      setTotalTickets(result.total)
    }
  }

  useEffect(() => {
    fetchTickets()
  }, [currentPage, pageSize, filters])

  const handleDelete = async (ticketId: number) => {
    if (confirm('Are you sure you want to delete this ticket?')) {
      setDeleteLoading(ticketId)
      const success = await deleteTicket(ticketId)
      setDeleteLoading(null)
      if (success) {
        fetchTickets()
      }
    }
  }

  const totalPages = Math.ceil(totalTickets / pageSize)

  // Filter tickets by search query
  const filteredTickets = tickets.filter(
    (ticket) =>
      ticket.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ticket.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
            Support Tickets
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            Total: {totalTickets} tickets
          </p>
        </div>
        <Link
          to="/new"
          className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
        >
          New Ticket
        </Link>
      </div>

      {/* Search Bar */}
      <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-4">
        <div className="flex gap-4 flex-col sm:flex-row">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search by subject or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg dark:bg-slate-700 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
          </div>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 px-4 py-2 border border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
          >
            <Filter className="w-4 h-4" />
            Filters
          </button>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <select
                value={filters.urgency}
                onChange={(e) =>
                  setFilters({ ...filters, urgency: e.target.value })
                }
                className="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg dark:bg-slate-700 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              >
                <option value="">All Urgencies</option>
                {URGENCY_OPTIONS.map((urgency) => (
                  <option key={urgency} value={urgency}>
                    {urgency}
                  </option>
                ))}
              </select>

              <select
                value={filters.category}
                onChange={(e) =>
                  setFilters({ ...filters, category: e.target.value })
                }
                className="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg dark:bg-slate-700 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              >
                <option value="">All Categories</option>
                {CATEGORY_OPTIONS.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>

              <select
                value={filters.status}
                onChange={(e) =>
                  setFilters({ ...filters, status: e.target.value })
                }
                className="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg dark:bg-slate-700 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              >
                <option value="">All Statuses</option>
                {STATUS_OPTIONS.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={() =>
                setFilters({ urgency: '', category: '', status: '' })
              }
              className="text-sm text-primary-600 dark:text-primary-400 hover:underline"
            >
              Clear filters
            </button>
          </div>
        )}
      </div>

      {/* Ticket Table */}
      <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
        {isLoading ? (
          <div className="flex items-center justify-center p-12">
            <Loader className="w-8 h-8 text-primary-600 animate-spin" />
          </div>
        ) : filteredTickets.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-slate-500 dark:text-slate-400 text-lg">
              {searchQuery || Object.values(filters).some((f) => f)
                ? 'No tickets match your search'
                : 'No tickets yet'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 dark:bg-slate-700 border-b border-slate-200 dark:border-slate-600">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-300 uppercase tracking-wider">
                    Subject
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-300 uppercase tracking-wider">
                    Urgency
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-300 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-300 uppercase tracking-wider">
                    Confidence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                {filteredTickets.map((ticket) => (
                  <tr
                    key={ticket.id}
                    className="hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
                  >
                    <td className="px-6 py-4 text-sm font-medium text-slate-900 dark:text-white max-w-xs truncate">
                      {ticket.subject}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span
                        className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                          URGENCY_COLORS[ticket.urgency as TicketUrgency]
                        }`}
                      >
                        {ticket.urgency}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
                      {ticket.category}
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
                      {ticket.status}
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-900 dark:text-white">
                      {ticket.confidence}%
                    </td>
                    <td className="px-6 py-4 text-sm flex gap-2">
                      <Link
                        to={`/tickets/${ticket.id}`}
                        className="p-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded transition-colors"
                        title="View details"
                      >
                        <Eye className="w-4 h-4" />
                      </Link>
                      <button
                        onClick={() => handleDelete(ticket.id)}
                        disabled={deleteLoading === ticket.id}
                        className="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors disabled:opacity-50"
                        title="Delete"
                      >
                        {deleteLoading === ticket.id ? (
                          <Loader className="w-4 h-4 animate-spin" />
                        ) : (
                          <Trash2 className="w-4 h-4" />
                        )}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-slate-600 dark:text-slate-400">
            Showing {(currentPage - 1) * pageSize + 1} to{' '}
            {Math.min(currentPage * pageSize, totalTickets)} of {totalTickets}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="p-2 border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>

            {Array.from({ length: totalPages }, (_, i) => i + 1)
              .slice(Math.max(0, currentPage - 2), Math.min(totalPages, currentPage + 1))
              .map((page) => (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={`px-3 py-2 rounded-lg transition-colors ${
                    currentPage === page
                      ? 'bg-primary-600 text-white'
                      : 'border border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700'
                  }`}
                >
                  {page}
                </button>
              ))}

            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="p-2 border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value))
              setCurrentPage(1)
            }}
            className="px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg dark:bg-slate-700 dark:text-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
          >
            <option value={10}>10 per page</option>
            <option value={20}>20 per page</option>
            <option value={50}>50 per page</option>
          </select>
        </div>
      )}
    </div>
  )
}
