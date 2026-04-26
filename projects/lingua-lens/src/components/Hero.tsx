```tsx
import React from 'react';
import { ArrowRight, Sparkle } from 'lucide-react';

const Hero: React.FC = () => {
  return (
    <section className="min-h-screen bg-[radial-gradient(at_20%_30%,rgba(168,_85,_247,_0.15)_0px,_transparent_50%),radial-gradient(at_80%_20%,rgba(245,_158,_11,_0.12)_0px,_transparent_50%),radial-gradient(at_50%_80%,rgba(20,_184,_166,_0.15)_0px,_transparent_50%),#0a0a0a] pt-32 pb-24 flex items-center justify-center">
      <div className="max-w-4xl mx-auto px-6 text-center space-y-8">
        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-gray-400 backdrop-blur-sm animate-float">
          <Sparkle size={16} />
          AI-Powered Language Learning
        </span>
        <h1 className="text-4xl md:text-7xl font-bold leading-tight">
          Speak Like a{' '}
          <span className="bg-gradient-to-r from-white via-amber-200 to-amber-500 bg-clip-text text-transparent">
            Native
          </span>
        </h1>
        <p className="text-xl md:text-2xl text-gray-400 leading-relaxed max-w-3xl mx-auto">
          Master real-world conversations with industry-specific language packs. From medical terminology to mechanic jargon—speak with confidence.
        </p>
        <button
          className="bg-amber-500 hover:bg-amber-600 text-black font-semibold px-8 py-4 rounded-xl transition-all hover:scale-105 inline-flex items-center gap-2 shadow-lg shadow-amber-500/20"
        >
          Browse Language Packs
          <ArrowRight size={24} />
        </button>
      </div>
    </section>
  );
};

export default Hero;
```