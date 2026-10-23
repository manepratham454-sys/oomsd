import React from 'react';

export const TeslaBackground = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0 select-none">
      {/* 4K Cinematic Car Drive YouTube Background Video */}
      <div className="absolute inset-0 w-full h-full overflow-hidden">
        <iframe
          src="https://www.youtube-nocookie.com/embed/WTi1OJfovnk?autoplay=1&mute=1&loop=1&playlist=WTi1OJfovnk&controls=0&showinfo=0&rel=0&iv_load_policy=3&disablekb=1&fs=0&start=22&playsinline=1"
          title="Cinematic Car Drive Background"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[177.77vh] min-w-full h-[56.25vw] min-h-full pointer-events-none filter brightness-75 contrast-110"
          style={{ border: 'none' }}
        />
      </div>

      {/* Modern Cyber Dark Glass Overlay to ensure maximum contrast & executive UI readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#060a14]/92 via-[#091124]/88 to-[#050811]/96 backdrop-blur-sm pointer-events-none"></div>

      {/* Subtle Ambient Radial Glows */}
      <div className="absolute top-0 left-1/4 w-[600px] h-[300px] bg-emerald-500/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute top-1/3 right-10 w-[500px] h-[400px] bg-cyan-500/10 rounded-full blur-[140px] pointer-events-none"></div>

      {/* Cyber Highway Lighting */}
      <div 
        className="absolute bottom-0 w-full h-24 opacity-30 pointer-events-none"
        style={{
          background: 'linear-gradient(to bottom, transparent 0%, rgba(5, 8, 17, 0.98) 100%)',
        }}
      >
        <div className="absolute bottom-3 left-0 w-[200%] h-1 flex gap-16 animate-road-travel opacity-50">
          {Array.from({ length: 30 }).map((_, i) => (
            <div key={i} className="w-14 h-1 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full shrink-0 shadow-[0_0_10px_#10b981]"></div>
          ))}
        </div>
      </div>

      {/* Cruising Tesla EV Overlay Silhouette */}
      <div className="absolute bottom-4 left-[-350px] animate-tesla-drive">
        <div className="relative w-[300px] h-[115px] animate-tesla-suspension">
          {/* Headlight beam */}
          <div 
            className="absolute top-8 right-[-120px] w-40 h-16 pointer-events-none"
            style={{
              background: 'radial-gradient(ellipse at left, rgba(56, 189, 248, 0.4) 0%, rgba(16, 185, 129, 0.12) 50%, transparent 80%)',
              clipPath: 'polygon(0% 40%, 100% 0%, 100% 100%, 0% 60%)',
              filter: 'blur(3px)',
            }}
          ></div>

          {/* Underglow Neon Lighting */}
          <div className="absolute bottom-2 left-6 right-6 h-5 bg-gradient-to-r from-emerald-500/50 via-cyan-400/60 to-emerald-400/50 blur-lg rounded-full animate-pulse"></div>

          {/* Tesla Car Silhouette SVG */}
          <svg
            viewBox="0 0 520 200"
            className="w-full h-full drop-shadow-[0_10px_20px_rgba(16,185,129,0.3)]"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M30 140 C 45 138, 70 140, 95 140 C 105 110, 155 110, 165 140 C 235 140, 310 140, 355 140 C 365 110, 415 110, 425 140 C 465 138, 495 130, 505 118 C 508 114, 506 106, 498 100 C 480 88, 455 84, 430 82 C 400 79, 360 62, 320 50 C 265 34, 195 38, 140 56 C 105 68, 75 88, 50 102 C 32 112, 25 125, 30 140 Z"
              fill="url(#teslaBodyGrad)"
              stroke="#22c55e"
              strokeWidth="2.5"
            />
            <path
              d="M145 58 C 190 42, 260 40, 315 52 C 345 60, 375 74, 395 82 C 350 82, 190 82, 125 78 C 132 70, 138 64, 145 58 Z"
              fill="url(#glassGrad)"
              stroke="#38bdf8"
              strokeWidth="1.5"
            />
            <line x1="225" y1="46" x2="225" y2="82" stroke="#0f172a" strokeWidth="4" />
            <line x1="305" y1="52" x2="315" y2="82" stroke="#0f172a" strokeWidth="4" />
            <rect x="200" y="94" width="22" height="3" rx="1.5" fill="#38bdf8" opacity="0.9" />
            <rect x="290" y="94" width="22" height="3" rx="1.5" fill="#38bdf8" opacity="0.9" />
            <path d="M70 106 Q 260 98 460 92" stroke="rgba(255,255,255,0.25)" strokeWidth="1.5" />
            <path d="M100 125 Q 260 122 360 125" stroke="rgba(16,185,129,0.5)" strokeWidth="1" />
            <path
              d="M480 94 C 496 97, 504 102, 505 106 C 495 107, 475 102, 465 100 Z"
              fill="#e0f2fe"
              className="animate-pulse"
              style={{ filter: 'drop-shadow(0 0 8px #38bdf8)' }}
            />
            <path
              d="M32 120 C 30 124, 32 130, 36 132 C 40 130, 42 126, 42 122 Z"
              fill="#ef4444"
              style={{ filter: 'drop-shadow(0 0 6px #ef4444)' }}
            />
            {/* Wheels */}
            <g transform="translate(130, 140)">
              <circle cx="0" cy="0" r="28" fill="#090d16" stroke="#334155" strokeWidth="3" />
              <circle cx="0" cy="0" r="18" fill="#1e293b" stroke="#10b981" strokeWidth="2" strokeDasharray="6 3" className="animate-spin-wheel" />
              <circle cx="0" cy="0" r="7" fill="#38bdf8" />
              <circle cx="0" cy="0" r="3" fill="#ffffff" />
            </g>
            <g transform="translate(390, 140)">
              <circle cx="0" cy="0" r="28" fill="#090d16" stroke="#334155" strokeWidth="3" />
              <circle cx="0" cy="0" r="18" fill="#1e293b" stroke="#10b981" strokeWidth="2" strokeDasharray="6 3" className="animate-spin-wheel" />
              <circle cx="0" cy="0" r="7" fill="#38bdf8" />
              <circle cx="0" cy="0" r="3" fill="#ffffff" />
            </g>
            <defs>
              <linearGradient id="teslaBodyGrad" x1="0%" y1="0%" x2="100%" y2="50%">
                <stop offset="0%" stopColor="#081021" />
                <stop offset="40%" stopColor="#0f1f3d" />
                <stop offset="75%" stopColor="#13274f" />
                <stop offset="100%" stopColor="#0a1429" />
              </linearGradient>
              <linearGradient id="glassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.6" />
                <stop offset="60%" stopColor="#0369a1" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#082f49" stopOpacity="0.95" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>
    </div>
  );
};
