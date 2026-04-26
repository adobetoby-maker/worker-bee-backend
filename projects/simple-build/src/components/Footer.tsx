import { useEffect } from 'react'

const Footer = () => {
  useEffect(() => {
    const footer = document.querySelector('.footer')
    if (footer) {
      footer.style.opacity = '0'
      setTimeout(() => {
        footer.style.opacity = '1'
        footer.style.transform = 'translateY(0)'
      }, 100)
    }
  }, [])

  return (
    <div className="bg-[#0a0a0a] text-white shadow-lg sm:px-6 px-4 mt-8 text-center transition-opacity duration-500 transform-gpu translate-y-2 footer">
      Built with Worker Bee 🐝
    </div>
  )
}

export default Footer