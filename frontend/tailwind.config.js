module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      height: {
        '15': '3.7rem',
        'main': 'calc(100% - 3.7rem)',
      },
      maxHeight: {
        'screen-2/3': '66vh'
      }
    },
  },
  plugins: [],
}
