import React from 'react'
import DocsCard from './DocsCard'
import SocialCard from './SocialCard'

const NextStepsContainer: React.FC = () => {
  return (
    <section className="flex flex-col md:flex-row gap-8 p-12">
      <DocsCard />
      <SocialCard />
    </section>
  )
}

export default NextStepsContainer
