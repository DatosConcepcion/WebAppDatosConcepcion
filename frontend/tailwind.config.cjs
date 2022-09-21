/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,svelte,ts}',
  ],
  theme: {
    extend: {
      fontFamily: {
        'title': ['Raleway'],
        'body': ['Roboto'],
      },
      colors: {
        'gray': '#dbdbdb',
        'gray-333333': '#333333',
        'gray-999999': '#999999',
        'coral': '#b00e57',
      }
    },
  },
  plugins: [],
}
