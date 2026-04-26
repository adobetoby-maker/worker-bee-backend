import documentationIcon from '../assets/documentation-icon.svg'

const DocumentationCard = () => {
  return (
    <div className="glass-card bg-white/80 backdrop-blur-[16px] shadow-1 p-8 rounded-lg">
      <svg className="icon w-6 h-6 text-[#60a5fa]" role="presentation" aria-hidden="true">
        <use href={documentationIcon} />
      </svg>
      <h2 className="text-2xl font-bold mt-4 mb-2">Documentation</h2>
      <p className="text-lg text-gray-700 mb-6">Your questions, answered</p>
      <ul className="flex flex-col space-y-4">
        <li>
          <a
            href="https://vite.dev/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-[#111827] hover:scale-102 transition-transform duration-300 ease-in-out"
          >
            <img src={documentationIcon} alt="Documentation icon" className="w-4 h-4" />
            Explore Vite
          </a>
        </li>
        <li>
          <a
            href="https://react.dev/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-[#111827] hover:scale-102 transition-transform duration-300 ease-in-out"
          >
            <img src={documentationIcon} alt="Documentation icon" className="w-4 h-4" />
            Learn more
          </a>
        </li>
      </ul>
    </div>
  )
}

export default DocumentationCard