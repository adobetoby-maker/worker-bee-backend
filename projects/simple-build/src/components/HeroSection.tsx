import { useState } from 'react'
import heroImg from '../assets/images/hero.png'
import reactLogo from '../assets/react.svg'
import viteLogo from '../assets/vite.svg'

const HeroSection = () => {
  const [count, setCount] = useState(0)

  return (
    <section className="container mx-auto px-4 sm:px-6 lg:px-8 mt-12 relative z-10">
      <div className="hero relative w-full max-w-[300px] mx-auto mb-12 shadow-2 hover:scale-105 transition-transform duration-300 ease-in-out">
        <img
          src={heroImg}
          alt="Hero"
          className="w-full h-full object-cover rounded-lg"
        />
        <div className="logos-overlay absolute inset-0 flex justify-center items-end space-x-4 pb-4">
          <img
            src={reactLogo}
            alt="React logo"
            className="image-base w-[170px] h-[179px] transform perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg) scale-1.4"
          />
          <img
            src={viteLogo}
            alt="Vite logo"
            className="image-base w-[170px] h-[179px] transform perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg) scale-0.8"
          />
        </div>
      </div>
      <div className="text-center">
        <h1 className="text-4xl sm:text-5xl font-bold text-[#111827] mb-4">Get started</h1>
        <p className="text-lg sm:text-xl text-[#334155] mb-6">
          Edit <code className="bg-gray-900 px-1 rounded">src/App.tsx</code> and save to test HMR
        </p>
        <button
          type="button"
          className="btn group relative overflow-hidden w-[200px] h-[60px] bg-gradient-to-r from-[#60a5fa] via-[#4dabf7] to-[#93c5fd] text-white font-bold px-6 py-3 rounded-lg shadow-md hover:scale-105 transition-transform duration-300 ease-in-out"
          onClick={() => setCount((count) => count + 1)}
        >
          <span className="absolute inset-0 bg-black opacity-25 group-hover:opacity-10 transition-opacity duration-300"></span>
          Count is {count}
        </button>
      </div>
    </section>
  )
}

export default HeroSection