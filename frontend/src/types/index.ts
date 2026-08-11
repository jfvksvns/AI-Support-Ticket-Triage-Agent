/**
 * Ticket related types
 */
export type TicketCategory = 
  | 'Software'
  | 'Hardware'
  | 'Network'
  | 'Security'
  | 'Cloud'
  | 'Database'
  | 'Email'
  | 'Printer'
  | 'Access Management'
  | 'Other'

export type TicketUrgency = 'Low' | 'Medium' | 'High' | 'Critical'

export type TicketStatus = 
  | 'Open'
  | 'Assigned'
  | 'In Progress'
  | 'Pending Human Review'
  | 'Resolved'
  | 'Closed'

export type AssignedTeam =
  | 'IT Support'
  | 'Network Team'
  | 'Security Team'
  | 'Cloud Team'
  | 'Database Team'
  | 'Application Team'
  | 'Service Desk'

/**
 * Toast notification types
 */
export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: string
  message: string
  type: ToastType
  duration?: number
}

/**
 * Form submission states
 */
export type LoadingState = 'idle' | 'loading' | 'success' | 'error'

/**
 * Pagination
 */
export interface PaginationParams {
  skip: number
  limit: number
}

/**
 * Filter options
 */
export interface FilterOptions {
  urgency?: TicketUrgency
  category?: TicketCategory
  status?: TicketStatus
  requiresReview?: boolean
}

/**
 * Sort options
 */
export type SortField = 'created_at' | 'urgency' | 'confidence' | 'status'
export type SortOrder = 'asc' | 'desc'

export interface SortOptions {
  field: SortField
  order: SortOrder
}
