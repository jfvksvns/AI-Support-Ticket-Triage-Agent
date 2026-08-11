import axios, { AxiosInstance, AxiosError } from 'axios'

/**
 * API Response Types
 */
export interface Ticket {
  id: number
  subject: string
  description: string
  reporter_name: string
  reporter_email: string
  department: string
  category: string
  urgency: string
  confidence: number
  assigned_team: string
  summary: string
  reasoning: string
  suggested_response: string
  status: string
  requires_human_review: boolean
  created_at: string
  updated_at: string
}

export interface TicketListResponse {
  items: Ticket[]
  total: number
  skip: number
  limit: number
}

export interface Classification {
  category: string
  urgency: string
  confidence: number
  assigned_team: string
  summary: string
  reasoning: string
  suggested_response: string
  requires_human_review: boolean
}

export interface ClassifyResponse {
  classification: Classification
  ticket_id?: number
}

export interface Statistics {
  total_tickets: number
  critical_tickets: number
  high_tickets: number
  medium_tickets: number
  low_tickets: number
  average_confidence: number
  human_review_count: number
  category_distribution: Record<string, number>
  urgency_distribution: Record<string, number>
  team_distribution: Record<string, number>
  status_distribution: Record<string, number>
}

export interface HealthResponse {
  status: string
  version: string
  database: string
  ai_service: string
  timestamp: string
}

/**
 * API Client for backend communication
 */
class ApiClient {
  private client: AxiosInstance

  constructor() {
    const apiUrl = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'
    
    this.client = axios.create({
      baseURL: apiUrl,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    })

    // Add API key if configured
    const apiKey = (import.meta as any).env.VITE_API_KEY
    if (apiKey) {
      this.client.defaults.headers.common['X-API-Key'] = apiKey
    }

    // Error interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error)
        throw error
      }
    )
  }

  /**
   * Classify a ticket without creating it
   */
  async classifyTicket(subject: string, description: string): Promise<ClassifyResponse> {
    const response = await this.client.post<ClassifyResponse>('/api/classify', {
      subject,
      description,
    })
    return response.data
  }

  /**
   * Create a new ticket with AI classification
   */
  async createTicket(data: {
    subject: string
    description: string
    reporter_name: string
    reporter_email: string
    department: string
  }): Promise<Ticket> {
    const response = await this.client.post<Ticket>('/api/tickets', data)
    return response.data
  }

  /**
   * List all tickets with optional filtering and pagination
   */
  async listTickets(
    skip: number = 0,
    limit: number = 50,
    urgency?: string,
    category?: string,
    status?: string,
    requiresReview?: boolean
  ): Promise<TicketListResponse> {
    const params = new URLSearchParams()
    params.append('skip', skip.toString())
    params.append('limit', limit.toString())
    if (urgency) params.append('urgency', urgency)
    if (category) params.append('category', category)
    if (status) params.append('status', status)
    if (requiresReview !== undefined) params.append('requires_review', requiresReview.toString())

    const response = await this.client.get<TicketListResponse>(
      `/api/tickets?${params.toString()}`
    )
    return response.data
  }

  /**
   * Get a specific ticket by ID
   */
  async getTicket(ticketId: number): Promise<Ticket> {
    const response = await this.client.get<Ticket>(`/api/tickets/${ticketId}`)
    return response.data
  }

  /**
   * Update ticket status
   */
  async updateTicketStatus(ticketId: number, status: string): Promise<Ticket> {
    const response = await this.client.patch<Ticket>(`/api/tickets/${ticketId}/status`, {
      status,
    })
    return response.data
  }

  /**
   * Delete a ticket
   */
  async deleteTicket(ticketId: number): Promise<void> {
    await this.client.delete(`/api/tickets/${ticketId}`)
  }

  /**
   * Get statistics and dashboard data
   */
  async getStatistics(): Promise<Statistics> {
    const response = await this.client.get<Statistics>('/api/statistics')
    return response.data
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/api/health')
    return response.data
  }

  /**
   * Get API information
   */
  async getApiInfo(): Promise<{
    name: string
    version: string
    description: string
    docs: string
    health: string
  }> {
    const response = await this.client.get('/')
    return response.data
  }
}

export const apiClient = new ApiClient()
