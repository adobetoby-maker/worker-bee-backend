import React from 'react'
import { Twitter } from 'lucide-react'

const SocialCard: React.FC = () => {
  return (
    <div className="flex flex-col gap-6 p-8 rounded-xl bg-white shadow-lg hover:shadow-2xl transition-shadow duration-200 ease-linear">
      <Twitter className="w-10 h-10 text-accent-500" />
      <h2 className="text-2xl font-bold">Connect with us</h2>
      <p className="text-gray-600">Join the Vite community</p>
      <ul className="list-none flex gap-8">
        <li>
          <a
            href="https://github.com/vitejs/vite"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-blue-500 hover:underline"
          >
            GitHub
          </a>
        </li>
        <li>
          <a
            href="https://twitter.com/vite_js"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-blue-500 hover:underline"
          >
            Twitter
          </a>
        </li>
      </ul>
    </div>
  )
}

export default SocialCard
