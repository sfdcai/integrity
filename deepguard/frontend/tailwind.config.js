/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        midnight: '#0B1021',
        teal: '#1CD9A1',
        amber: '#FFB020',
        redish: '#FF5A63',
        slate: '#1E2538'
      },
      boxShadow: {
        soft: '0 20px 40px rgba(0,0,0,0.25)',
      },
    },
  },
  plugins: [],
}
