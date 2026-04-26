import HeroSection from './components/HeroSection'
import DocumentationCard from './components/DocumentationCard'
import SocialMediaCard from './components/SocialMediaCard'
import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex flex-col">
      <HeroSection />
      <section className="container mx-auto px-4 sm:px-6 lg:px-8 my-8 grid gap-8 sm:grid-cols-2 grow">
        <DocumentationCard />
        <SocialMediaCard />
      </section>
      <Footer />
    </div>
  )
}

export default App