import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useApi } from '@/hooks/useApi'
import { Loader, AlertCircle } from 'lucide-react'

const ticketSchema = z.object({
  subject: z
    .string()
    .min(5, 'Subject must be at least 5 characters')
    .max(255, 'Subject must not exceed 255 characters'),
  description: z
    .string()
    .min(20, 'Description must be at least 20 characters')
    .max(5000, 'Description must not exceed 5000 characters'),
  reporter_name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(255, 'Name must not exceed 255 characters'),
  reporter_email: z
    .string()
    .email('Must be a valid email address'),
  department: z
    .string()
    .min(2, 'Department must be at least 2 characters')
    .max(255, 'Department must not exceed 255 characters'),
})

type TicketFormData = z.infer<typeof ticketSchema>

/**
 * Ticket creation form component
 */
export function TicketForm() {
  const navigate = useNavigate()
  const { createTicket, isLoading } = useApi()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    watch,
  } = useForm<TicketFormData>({
    resolver: zodResolver(ticketSchema),
    mode: 'onChange',
  })

  const watchDescription = watch('description')

  const onSubmit = async (data: TicketFormData) => {
    const ticket = await createTicket(data)
    if (ticket) {
      navigate(`/tickets/${ticket.id}`)
    }
  }

  return (
    <div className="max-w-2xl mx-auto bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
          Create New Ticket
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          Submit a support ticket and our AI agent will classify it automatically
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Subject */}
        <div>
          <label htmlFor="subject" className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
            Subject <span className="text-red-500">*</span>
          </label>
          <input
            {...register('subject')}
            type="text"
            id="subject"
            placeholder="Brief description of the issue"
            className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-slate-700 dark:text-white transition"
          />
          {errors.subject && (
            <div className="flex items-center gap-2 mt-2 text-red-600 dark:text-red-400 text-sm">
              <AlertCircle className="w-4 h-4" />
              {errors.subject.message}
            </div>
          )}
        </div>

        {/* Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
            Description <span className="text-red-500">*</span>
          </label>
          <textarea
            {...register('description')}
            id="description"
            placeholder="Detailed description of the problem"
            rows={6}
            className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-slate-700 dark:text-white transition resize-none"
          />
          <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            {watchDescription?.length || 0} / 5000 characters
          </div>
          {errors.description && (
            <div className="flex items-center gap-2 mt-2 text-red-600 dark:text-red-400 text-sm">
              <AlertCircle className="w-4 h-4" />
              {errors.description.message}
            </div>
          )}
        </div>

        {/* Reporter Name */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="reporter_name" className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
              Your Name <span className="text-red-500">*</span>
            </label>
            <input
              {...register('reporter_name')}
              type="text"
              id="reporter_name"
              placeholder="Full name"
              className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-slate-700 dark:text-white transition"
            />
            {errors.reporter_name && (
              <div className="flex items-center gap-2 mt-2 text-red-600 dark:text-red-400 text-sm">
                <AlertCircle className="w-4 h-4" />
                {errors.reporter_name.message}
              </div>
            )}
          </div>

          {/* Email */}
          <div>
            <label htmlFor="reporter_email" className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
              Email <span className="text-red-500">*</span>
            </label>
            <input
              {...register('reporter_email')}
              type="email"
              id="reporter_email"
              placeholder="your.email@company.com"
              className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-slate-700 dark:text-white transition"
            />
            {errors.reporter_email && (
              <div className="flex items-center gap-2 mt-2 text-red-600 dark:text-red-400 text-sm">
                <AlertCircle className="w-4 h-4" />
                {errors.reporter_email.message}
              </div>
            )}
          </div>
        </div>

        {/* Department */}
        <div>
          <label htmlFor="department" className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
            Department <span className="text-red-500">*</span>
          </label>
          <input
            {...register('department')}
            type="text"
            id="department"
            placeholder="Your department"
            className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-slate-700 dark:text-white transition"
          />
          {errors.department && (
            <div className="flex items-center gap-2 mt-2 text-red-600 dark:text-red-400 text-sm">
              <AlertCircle className="w-4 h-4" />
              {errors.department.message}
            </div>
          )}
        </div>

        {/* Form Actions */}
        <div className="flex gap-4 pt-6">
          <button
            type="submit"
            disabled={isLoading || !isValid}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-slate-400 text-white font-medium rounded-lg transition-colors"
          >
            {isLoading && <Loader className="w-4 h-4 animate-spin" />}
            {isLoading ? 'Creating...' : 'Create Ticket'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/tickets')}
            className="flex-1 px-6 py-3 border border-slate-300 dark:border-slate-600 text-slate-900 dark:text-white font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
