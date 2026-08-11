import { useState, useCallback } from 'react'
import { apiClient, Ticket, TicketListResponse, Statistics, ClassifyResponse } from '@/services/api'
import { useToast } from './useToast'

/**
 * Hook for API calls with loading and error states
 */
export function useApi() {
  const { showToast } = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const resetState = useCallback(() => {
    setError(null)
    setIsLoading(false)
  }, [])

  const classifyTicket = useCallback(
    async (subject: string, description: string): Promise<ClassifyResponse | null> => {
      setIsLoading(true)
      setError(null)
      try {
        const result = await apiClient.classifyTicket(subject, description)
        return result
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to classify ticket'
        setError(message)
        showToast(message, 'error')
        return null
      } finally {
        setIsLoading(false)
      }
    },
    [showToast]
  )

  const createTicket = useCallback(
    async (data: {
      subject: string
      description: string
      reporter_name: string
      reporter_email: string
      department: string
    }): Promise<Ticket | null> => {
      setIsLoading(true)
      setError(null)
      try {
        const result = await apiClient.createTicket(data)
        showToast('Ticket created successfully!', 'success')
        return result
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to create ticket'
        setError(message)
        showToast(message, 'error')
        return null
      } finally {
        setIsLoading(false)
      }
    },
    [showToast]
  )

  const getTickets = useCallback(
    async (skip = 0, limit = 50, filters?: any): Promise<TicketListResponse | null> => {
      setIsLoading(true)
      setError(null)
      try {
        const result = await apiClient.listTickets(
          skip,
          limit,
          filters?.urgency,
          filters?.category,
          filters?.status,
          filters?.requiresReview
        )
        return result
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to fetch tickets'
        setError(message)
        return null
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const getTicket = useCallback(async (ticketId: number): Promise<Ticket | null> => {
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiClient.getTicket(ticketId)
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch ticket'
      setError(message)
      return null
    } finally {
      setIsLoading(false)
    }
  }, [])

  const updateStatus = useCallback(
    async (ticketId: number, status: string): Promise<Ticket | null> => {
      setIsLoading(true)
      setError(null)
      try {
        const result = await apiClient.updateTicketStatus(ticketId, status)
        showToast('Status updated successfully!', 'success')
        return result
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to update status'
        setError(message)
        showToast(message, 'error')
        return null
      } finally {
        setIsLoading(false)
      }
    },
    [showToast]
  )

  const deleteTicket = useCallback(
    async (ticketId: number): Promise<boolean> => {
      setIsLoading(true)
      setError(null)
      try {
        await apiClient.deleteTicket(ticketId)
        showToast('Ticket deleted successfully!', 'success')
        return true
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to delete ticket'
        setError(message)
        showToast(message, 'error')
        return false
      } finally {
        setIsLoading(false)
      }
    },
    [showToast]
  )

  const getStatistics = useCallback(async (): Promise<Statistics | null> => {
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiClient.getStatistics()
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch statistics'
      setError(message)
      return null
    } finally {
      setIsLoading(false)
    }
  }, [])

  const checkHealth = useCallback(async (): Promise<boolean> => {
    try {
      const result = await apiClient.healthCheck()
      return result.status === 'healthy' || result.status === 'degraded'
    } catch {
      return false
    }
  }, [])

  return {
    isLoading,
    error,
    resetState,
    classifyTicket,
    createTicket,
    getTickets,
    getTicket,
    updateStatus,
    deleteTicket,
    getStatistics,
    checkHealth,
  }
}
