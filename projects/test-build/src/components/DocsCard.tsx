import React from 'react'
import { FileText } from 'lucide-react'

const DocsCard: React.FC = () => {
  return (
    <div className="flex flex-col gap-6 p-8 rounded-xl bg-white shadow-lg hover:shadow-2xl transition-shadow duration-200 ease-linear">
      <FileText className="w-10 h-10 text-accent-500" />
      <h2 className="text-2xl font-bold">Documentation</h2>
      <p className="text-gray-600">Your questions, answered</p>
      <ul className="list-none flex gap-8">
        <li>
          <a
            href="https://vite.dev/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-blue-500 hover:underline"
          >
            Explore Vite
          </a>
        </li>
        <li>
          <a
            href="https://react.dev/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-blue-500 hover:underline"
          >
            Learn more
          </a>
        </li>
      </ul>
    </div>
  )
}

export default DocsCard
