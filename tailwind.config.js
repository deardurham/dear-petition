module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
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
        blue: '#4082c3',
        green: '#89af5b',
        yellow: '#d1d156',
        gray: '#82908d',
        black: '#262626',
        red: '#b04846',
        primary: '#3d8f9d',
        white: '#ffffff',
      },
    },
  },
  plugins: [],
};
