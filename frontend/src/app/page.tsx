"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const [booting, setBooting] = useState(true);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("INITIALIZING SYSTEM...");
  const router = useRouter();

  // Boot sequence effectc
  useEffect(() => {
    let current = 0;
    const interval = setInterval(() => {
      const increment = Math.floor(Math.random() * 15) + 1;
      current += increment;
      if (current >= 100) {
        current = 100;
        clearInterval(interval);
        setStatus("SYSTEM ONLINE");
        setTimeout(() => setBooting(false), 800);
      } else {
        if (current < 30) setStatus("LOADING BOOKINGS DATA...");
        else if (current < 60) setStatus("INITIALIZING XGBOOST MODEL...");
        else if (current < 90) setStatus("CONNECTING MINIMAX M3...");
      }
      setProgress(current);
    }, 150);
    return () => clearInterval(interval);
  }, []);

  const heroText = "HOTELPULSE AI".split("");

  return (
    <div className="bg-[#0a0a0a] min-h-screen w-full text-white font-mono overflow-hidden relative">
      {/* SVG Noise Texture */}
      <div className="pointer-events-none fixed inset-0 z-50 h-full w-full opacity-10 mix-blend-overlay">
        <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
          <filter id="noiseFilter">
            <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" />
          </filter>
          <rect width="100%" height="100%" filter="url(#noiseFilter)" />
        </svg>
      </div>

      <AnimatePresence>
        {booting && (
          <motion.div
            exit={{ y: "-100%", transition: { duration: 0.8, ease: "easeInOut" } }}
            className="fixed inset-0 z-40 flex flex-col items-center justify-center bg-[#0a0a0a]"
          >
            <div className="text-[#ebff00] text-6xl font-black mb-4">{progress}%</div>
            <div className="text-sm tracking-widest uppercase">{status}</div>
          </motion.div>
        )}
      </AnimatePresence>

      {!booting && (
        <div className="relative z-10 flex flex-col min-h-screen p-8 justify-between">
          <header className="flex justify-between items-center text-sm font-bold tracking-widest text-[#ebff00]">
            <span>SYSTEM v2.0</span>
            <span>DEMAND FORECASTING</span>
          </header>

          <main className="flex-1 flex flex-col justify-center items-center">
            <h1 className="text-7xl md:text-9xl font-black flex overflow-hidden">
              {heroText.map((char, index) => (
                <motion.span
                  key={index}
                  initial={{ y: 150, rotateX: -90, opacity: 0 }}
                  animate={{ y: 0, rotateX: 0, opacity: 1 }}
                  transition={{
                    duration: 0.8,
                    delay: index * 0.05,
                    ease: [0.2, 0.65, 0.3, 0.9],
                  }}
                  className={char === " " ? "w-6" : "inline-block origin-bottom"}
                >
                  {char}
                </motion.span>
              ))}
            </h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.5 }}
              className="mt-8 text-xl md:text-2xl text-center max-w-2xl text-gray-400"
            >
              ML pipeline combining XGBoost pricing models with Minimax M3 for promotional marketing.
            </motion.p>

            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 2.0 }}
              onClick={() => router.push('/dashboard')}
              className="mt-12 px-8 py-4 bg-[#ebff00] text-[#0a0a0a] font-black text-xl hover:scale-105 transition-transform duration-200 uppercase tracking-widest"
            >
              Initialize Dashboard
            </motion.button>
          </main>

          {/* Marquee */}
          <div className="w-full overflow-hidden whitespace-nowrap py-4 border-t border-[#ebff00] border-opacity-30">
            <motion.div
              animate={{ x: ["0%", "-50%"] }}
              transition={{ ease: "linear", duration: 10, repeat: Infinity }}
              className="inline-block text-[#ebff00] text-lg font-bold tracking-widest"
            >
              PROFIT MAXIMIZATION /// PREDICTIVE ANALYTICS /// DYNAMIC PRICING /// AUTOMATED MARKETING /// PROFIT MAXIMIZATION /// PREDICTIVE ANALYTICS /// DYNAMIC PRICING /// AUTOMATED MARKETING ///
            </motion.div>
          </div>
        </div>
      )}
    </div>
  );
}
