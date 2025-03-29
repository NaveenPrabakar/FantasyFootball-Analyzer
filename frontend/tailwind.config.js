module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nfl-red': '#D50A0A',
        'nfl-blue': '#013369',
        'nfl-gray': '#A5ACAF',
        'nfl-light': '#F5F5F5',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'nfl-pattern': "linear-gradient(45deg, #013369 25%, transparent 25%), linear-gradient(-45deg, #013369 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #013369 75%), linear-gradient(-45deg, transparent 75%, #013369 75%)",
      },
      backgroundSize: {
        'nfl-pattern': '20px 20px',
      },
    },
  },
  plugins: [],
} 