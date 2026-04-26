import { Twitter, Github } from 'lucide-react'

const SocialMediaCard = () => {
  return (
    <div className="glass-card bg-white/80 backdrop-blur-[16px] shadow-xl hover-shadow-xl p-8 rounded-lg relative group transform transition-transform duration-300 ease-in-out hover:translate-y-[-10px]">
      {/* Header Section */}
      <div className="flex items-center justify-between mb-8 space-x-4">
        <Twitter className="w-6 h-6 text-[#60a5fa]" role="presentation" aria-hidden="true" />
        <h2 className="text-2xl font-bold">Connect with us</h2>
      </div>

      <p className="text-lg text-gray-700 mb-8 max-w-[341px] mx-auto">
        Join the Vite community and stay updated with our latest developments.
      </p>

      {/* Social Links */}
      <ul className="space-y-6">
        {[
          {
            name: 'Twitter',
            href: 'https://twitter.com/vite_js',
            icon: Twitter,
            color: '#60a5fa'
          },
          {
            name: 'GitHub',
            href: 'https://github.com/vitejs/vite',
            icon: Github,
            color: '#ef4444'
          }
        ].map((item, index) => (
          <li key={index} className="flex items-center space-x-4">
            <a
              href={item.href}
              target="_blank"
              rel="noopener noreferrer"
              className="social-link hover-scale"
            >
              <item.icon className="w-4 h-4" style={{ color: item.color }} />
              {item.name}
            </a>
          </li>
        ))}
      </ul>

      {/* Gradient Border */}
      <div className="social-gradient-border"></div>
    </div>
  )
}

export default SocialMediaCard