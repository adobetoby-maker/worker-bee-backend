import React from 'react'
import heroImg from '../assets/hero.png'
import reactLogo from '../assets/react.svg'
import viteLogo from '../assets/vite.svg'

const HeroSection: React.FC = () => {
  return (
    <section className="relative w-full max-w-md mx-auto mt-12">
      <img
        src={heroImg}
        alt=""
        className="object-cover w-[170px] h-[179px]"
        style={{
          transform: 'rotateX(45deg) rotateY(-30deg)',
        }}
      />
      <img
        src={reactLogo}
        alt="React logo"
        className="absolute top-8 left-8 w-12 h-12"
        style={{
          transform:
            'perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg) scale(1.4)',
        }}
      />
      <img
        src={viteLogo}
        alt="Vite logo"
        className="absolute top-28 left-20 w-10 h-10"
        style={{
          transform:
            'perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg) scale(0.8)',
        }}
      />
    </section>
  )
}

export default HeroSection
