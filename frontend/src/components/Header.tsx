import { Link } from 'react-router-dom'
import { useDarkMode } from '@/hooks/useDarkMode'
import { Moon, Sun, Menu, X } from 'lucide-react'
import { useState } from 'react'

/**
 * Header component with navigation and dark mode toggle
 */
export function Header() {
  const { isDark, toggle } = useDarkMode()
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 shadow-sm sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 font-bold text-xl text-primary-600 dark:text-primary-400 hover:opacity-80 transition-opacity"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center text-white text-sm font-bold">
              AI
            </div>
            <span className="hidden sm:inline">Ticket Triage</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/"
              className="text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors text-sm font-medium"
            >
              Dashboard
            </Link>
            <Link
              to="/tickets"
              className="text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors text-sm font-medium"
            >
              Tickets
            </Link>
            <Link
              to="/new"
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors"
            >
              New Ticket
            </Link>
          </nav>

          {/* Right actions */}
          <div className="flex items-center gap-3">
            {/* Dark mode toggle */}
            <button
              onClick={toggle}
              className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
              aria-label="Toggle dark mode"
            >
              {isDark ? (
                <Sun className="w-5 h-5 text-yellow-500" />
              ) : (
                <Moon className="w-5 h-5 text-slate-600" />
              )}
            </button>

            {/* Mobile menu button */}
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="md:hidden p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
              aria-label="Toggle menu"
            >
              {menuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {menuOpen && (
          <nav className="md:hidden border-t border-slate-200 dark:border-slate-700 py-4 space-y-2">
            <Link
              to="/"
              className="block px-4 py-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
              onClick={() => setMenuOpen(false)}
            >
              Dashboard
            </Link>
            <Link
              to="/tickets"
              className="block px-4 py-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
              onClick={() => setMenuOpen(false)}
            >
              Tickets
            </Link>
            <Link
              to="/new"
              className="block px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
              onClick={() => setMenuOpen(false)}
            >
              New Ticket
            </Link>
          </nav>
        )}
      </div>
    </header>
  )
}
