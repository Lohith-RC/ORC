/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', '-apple-system', 'sans-serif'],
        serif: ['Newsreader', 'Fraunces', 'Georgia', 'serif'],
        mono: ['"Geist Mono"', 'JetBrains Mono', 'Consolas', 'monospace'],
        display: ['Newsreader', 'Fraunces', 'Georgia', 'serif'],
      },
      colors: {
        parchment: {
          50: '#FDFBF7',
          100: '#F7F4EC',
          200: '#EFEAE0',
          300: '#E4DDD0',
          400: '#D5CCBD',
        },
        ink: {
          700: '#2A2C34',
          800: '#1E2026',
          850: '#15161B',
          900: '#101115',
          950: '#0A0B0E',
        },
        clinical: {
          teal: '#165B51',
          celadon: '#237367',
          sage: '#3A6852',
          terracotta: '#9E3B2E',
          ochre: '#B2761B',
          slate: '#253545',
        },
        teal: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        slate: {
          850: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        }
      }
    },
  },
  plugins: [],
}