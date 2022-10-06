const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    content: [
        './assets/**/*.js',
        './assets/**/**/*.js',
        './assets/**/**/**/*.svelte',
        './assets/**/**/**/*.js',
        './assets/*.js',
        './assets/**/*.vue',
        './templates/**/*.html',
        './templates/**/**/*.html',
    ],
    safelist: [
        'alert-success',
        'alert-info',
        'alert-error',
        'alert-warning',
    ],
    daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/colors/themes")["[data-theme=light]"],
          primary: "#2A324B",
          secondary: "#F58F29",
          accent: "#C78283",
          neutral: "#7699D4",
          "base-100": "#F5F5F5",
        },
      },
    ],
  },
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter var', ...defaultTheme.fontFamily.sans],
            },
            aspectRatio: {
                '3/2': '3 / 2',
            },
        },
        container: {
            center: true,
            // padding: '2rem',
        },
    },
    variants: {
        extend: {},
    },


    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require("daisyui"),
        require("tailwindcss-animate"),
    ],
}
