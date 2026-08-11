import { useEffect, useState } from 'react'

/**
 * Hook for managing dark mode
 */
export function useDarkMode() {
  const [isDark, setIsDark] = useState(() => {
    // Check localStorage first
    const saved = localStorage.getItem('darkMode')
    if (saved !== null) {
      return saved === 'true'
    }

    // Check system preference
    if (typeof window !== 'undefined') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }

    return false
  })

  useEffect(() => {
    // Update document class
    if (isDark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }

    // Save to localStorage
    localStorage.setItem('darkMode', isDark.toString())
  }, [isDark])

  const toggle = () => {
    setIsDark((prev) => !prev)
  }

  return { isDark, toggle }
}
