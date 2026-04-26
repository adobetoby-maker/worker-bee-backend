import React, { useState } from 'react'

const CounterButton: React.FC = () => {
  const [count, setCount] = useState(0)

  return (
    <button
      className="inline-flex items-center justify-center gap-2 min-h-[48px] px-6 py-3 text-sm font-semibold text-white bg-accent-500 rounded-md shadow-md transition-transform duration-200 ease-linear hover:scale-105 focus:outline-2 focus:outline-offset-2 focus:outline-accent-500"
      onClick={() => setCount((count) => count + 1)}
    >
      Count is {count}
    </button>
  )
}

export default CounterButton
