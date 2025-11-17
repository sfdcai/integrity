/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        midnight: '#0b1021',
        neon: '#7af0ff',
        ember: '#ff7a7a'
      }
    }
  },
  plugins: [],
}
