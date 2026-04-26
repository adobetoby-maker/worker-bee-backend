import React from 'react'
import { ArrowRight } from 'lucide-react'

const Hero: React.FC = () => {
  return (
    <section className="relative pt-32 pb-24 lg:pt-40 lg:pb-32">
      <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-border bg-surface text-sm font-medium mb-8 relative overflow-hidden">
          <span>AI-Powered Websites</span>
          <div className="absolute inset-0 bg-gradient-to-r from-accent-primary to-accent-secondary animate-shimmer"></div>
        </div>
        <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight text-center text-transparent bg-clip-text bg-gradient-to-r from-accent-gradient-start to-accent-gradient-end">
          Create Websites with AI
        </h1>
        <p className="text-secondary body-large mb-12 max-w-2xl mx-auto">
          Revolutionize your online presence with our cutting-edge AI website generator.
        </p>
        <div className="flex gap-4 justify-center flex-col sm:flex-row">
          <button className="px-8 py-4 bg-gradient-to-r from-accent-primary to-accent-secondary text-white font-semibold rounded-xl shadow-lg transition-transform duration-300 ease-out hover:brightness-110 hover:translate-y-[-2px] active:translate-y-0 active:brightness-95">
            Get Started
          </button>
          <button className="px-8 py-4 border-2 border-border-strong text-accent-primary font-semibold rounded-xl shadow-lg transition-transform duration-300 ease-out hover:bg-surface hover:border-accent-primary">
            View Examples
          </button>
        </div>
      </div>
    </section>
  )
}

export default Hero