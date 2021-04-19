module.exports = {
  purge: {
    enabled: true,
    content: [
      './site/templates/*.html',
      './site/templates/**/*.html',
      './site/static/js/*.js'
    ]
  },
  theme: {
    extend: {
      boxShadow: {
        blue: 'inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6)',
      },
    }
  },
  variants: {},
  plugins: [],
}