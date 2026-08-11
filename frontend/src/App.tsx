import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Header } from '@/components/Header'
import { ToastContainer } from '@/components/Toast'
import { DashboardPage } from '@/pages/DashboardPage'
import { TicketsPage } from '@/pages/TicketsPage'
import { NewTicketPage } from '@/pages/NewTicketPage'
import { TicketDetailsPage } from '@/pages/TicketDetailsPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

/**
 * Main App component
 * Sets up routing and layout
 */
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white dark:bg-slate-900 text-slate-900 dark:text-white">
        <Header />
        
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/tickets" element={<TicketsPage />} />
            <Route path="/tickets/:id" element={<TicketDetailsPage />} />
            <Route path="/new" element={<NewTicketPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>

        <ToastContainer />
      </div>
    </Router>
  )
}

export default App
