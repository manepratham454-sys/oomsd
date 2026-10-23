/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#060a14',
          900: '#0b1329',
          850: '#0f1b3b',
          800: '#15244d',
          700: '#1e3266',
          600: '#2a4382',
        },
        evgreen: {
          400: '#34d399',
          500: '#10b981',
          600: '#059669',
          glow: 'rgba(16, 185, 129, 0.25)',
        },
        evcyan: {
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'glow-green': '0 0 20px -3px rgba(16, 185, 129, 0.35)',
        'glow-cyan': '0 0 20px -3px rgba(14, 165, 233, 0.35)',
      }
    },
  },
  plugins: [],
}
