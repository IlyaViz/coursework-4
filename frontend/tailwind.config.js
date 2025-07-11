/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  safelist: [...Array.from({ length: 100 }, (_, i) => `sm:grid-cols-${i + 1}`)],
  theme: {
    extend: {},
  },
  plugins: [],
};
