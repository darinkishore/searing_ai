const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    content: [
        './assets/**/*.js',
        './assets/**/*.svelte',
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
