module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          navy900: '#131D2F',
          navy800: '#1B2940',
          blue500: '#2B6FE4',
          blue600: '#245FC7',
          green500: '#15C39A',
          green600: '#11AD87'
        },
        surface: {
          page: '#F2F7F7',
          card: '#FFFFFF'
        },
        text: {
          primary: '#142033',
          secondary: '#566476'
        },
        border: {
          DEFAULT: '#D8E2ED'
        }
      },
      fontFamily: {
        sans: ['Segoe UI', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif']
      },
      boxShadow: {
        soft: '0 10px 30px rgba(16, 24, 40, 0.08)'
      }
    }
  },
  plugins: []
}
