module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  important: true,
  theme: {
    fontSize: {
      '2xs': '1rem',
      xs: '1.25rem',
      sm: '1.5rem',
      base: '1.6rem',
      lg: '1.75rem',
      xl: '1.9rem',
      '2xl': '2rem',
      '3xl': '3rem',
      '4xl': '4rem',
    },
    extend: {
      colors: {
        blue: {
          DEFAULT: '#4082c3',
          primary: '#3d8f9d',
        },
        green: {
          DEFAULT: '#89af5b',
        },
        yellow: {
          DEFAULT: '#d1d156',
        },
        gray: {
          DEFAULT: '#82908d',
          disabled: '#b8b8b8',
        },
        black: {
          DEFAULT: '#262626',
        },
        red: {
          DEFAULT: '#b04846',
        },
        primary: '#3d8f9d',
        white: {
          DEFAULT: '#ffffff',
        },
      },
    },
  },
  plugins: [],
};
