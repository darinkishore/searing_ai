module.exports = {

/*
daisyui: {
        themes: [
            {
                'mytheme': {
                    "primary": "#6D27FA",
                    "secondary": "#D926A9",
                    "accent": "#1FB2A6",
                    "neutral": "#191D24",
                    "base-100": "#2A303C",
                    "info": "#3ABFF8",
                    "success": "#36D399",
                    "warning": "#FBBD23",
                    "error": "#F87272",
            },
        ],
    },
 */
    content: [
        './assets/**/*.js',
        './assets/**/*.vue',
        './templates/**/*.html',
    ],
    safelist: [
        'alert-success',
        'alert-info',
        'alert-error',
        'alert-warning',
    ],
    theme: {
        extend: {
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
    ],
}
