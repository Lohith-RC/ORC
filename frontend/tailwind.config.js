/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
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
      },
      boxShadow: {
        'soft-sm': '0 1px 2px 0 rgba(16, 17, 21, 0.04)',
        'soft': '0 2px 8px -2px rgba(16, 17, 21, 0.05), 0 1px 4px -1px rgba(16, 17, 21, 0.03)',
        'soft-md': '0 6px 16px -4px rgba(16, 17, 21, 0.06), 0 2px 6px -1px rgba(16, 17, 21, 0.04)',
        'soft-lg': '0 12px 28px -6px rgba(16, 17, 21, 0.08), 0 4px 10px -2px rgba(16, 17, 21, 0.04)',
        'soft-xl': '0 20px 40px -10px rgba(16, 17, 21, 0.10)',
      },
    },
  },
  plugins: [],
};