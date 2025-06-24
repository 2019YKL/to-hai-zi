/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./assets/**/*.js",
    "./search.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        'poem': ['LXGW WenKai', 'LXGWWenKai', 'LXGWWenKai-Fallback', 'Noto Serif SC', 'Source Han Serif SC', 'STSong', '宋体', 'Georgia', 'serif'],
        'ui': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'PingFang SC', 'Microsoft YaHei', 'sans-serif']
      },
      colors: {
        'poem-gray': {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a'
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'card-appear': 'cardAppear 0.6s ease-out forwards'
      },
      backdropBlur: {
        'xs': '2px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}