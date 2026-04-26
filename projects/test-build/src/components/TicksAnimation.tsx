import React from 'react'

const TicksAnimation: React.FC = () => {
  return (
    <div className="absolute top-0 left-0 w-full h-full bg-[conic-gradient(from_180deg_at_50%_50%,var(--accent-500)_20%,hsl(280,_80%,_40%)_100%)] opacity-20 animate-pulse duration-3000"></div>
  )
}

export default TicksAnimation
