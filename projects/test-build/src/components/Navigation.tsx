import React, { useState } from 'react'
import { Menu } from 'lucide-react'

const Navigation: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isOpen, setIsOpen] = useState(false)

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      setIsScrolled(true)
    } else {
      setIsScrolled(false)
    }
  })

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-white/90 transition-all duration-300 ${isScrolled ? 'border-b border-border' : ''}`}>
      <div className="max-w-7xl mx-auto px-6 lg:px-8 h-20 flex justify-between items-center">
        <div className="flex gap-2 items-center font-bold text-xl text-primary">
          <span>AI Websites</span>
        </div>
        <div className="hidden md:flex gap-8 text-sm font-medium">
          <a href="#features" className="hover:text-accent-primary">Features</a>
          <a href="#pricing" className="hover:text-accent-primary">Pricing</a>
          <a href="#examples" className="hover:text-accent-primary">Examples</a>
        </div>
        <button className="px-8 py-2.5 bg-gradient-to-r from-accent-primary to-accent-secondary text-white font-semibold rounded-md shadow-lg transition-transform duration-300 ease-out hover:brightness-110 hover:translate-y-[-2px] active:translate-y-0 active:brightness-95">
          Get Started
        </button>
        <div className="md:hidden">
          <button onClick={() => setIsOpen(!isOpen)} className="text-primary">
            <Menu size={24} />
          </button>
          {isOpen && (
            <div className="absolute top-full left-0 right-0 bg-surface-elevated backdrop-filter backdrop-blur-lg p-6 rounded-b-xl shadow-lg">
              <a href="#features" className="block mb-4 hover:text-accent-primary">Features</a>
              <a href="#pricing" className="block mb-4 hover:text-accent-primary">Pricing</a>
              <a href="#examples" className="block mb-4 hover:text-accent-primary">Examples</a>
              <button className="w-full px-8 py-2.5 bg-gradient-to-r from-accent-primary to-accent-secondary text-white font-semibold rounded-md shadow-lg transition-transform duration-300 ease-out hover:brightness-110 hover:translate-y-[-2px] active:translate-y-0 active:brightness-95">
                Get Started
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navigation