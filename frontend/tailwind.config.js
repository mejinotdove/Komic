/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        base: 'var(--bg-base)',
        surface: {
          DEFAULT: 'var(--bg-surface)',
          hover: 'var(--bg-surface-hover)',
          border: 'var(--border-surface)',
        },
        accent: {
          DEFAULT: 'var(--clr-accent)',
          hover: 'var(--clr-accent-hover)',
        },
        gold: 'var(--clr-gold)',
        input: 'var(--bg-input)',
        card: 'var(--bg-card)',
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
          dim: 'var(--text-dim)',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 1px 2px rgba(0,0,0,0.3)',
        'card-hover': '0 8px 25px rgba(0,0,0,0.4), 0 2px 10px rgba(0,0,0,0.2)',
        'modal': '0 20px 60px rgba(0,0,0,0.5)',
        'accent': '0 4px 14px var(--shadow-accent)',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        'star-pop': {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.35)' },
          '100%': { transform: 'scale(1)' },
        },
        'pulse-ring': {
          '0%': { boxShadow: '0 0 0 0 var(--shadow-accent-ring)' },
          '100%': { boxShadow: '0 0 0 12px transparent' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(8px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'spin-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
      animation: {
        shimmer: 'shimmer 2s infinite',
        'star-pop': 'star-pop 0.35s ease',
        'pulse-ring': 'pulse-ring 1.5s infinite',
        'slide-up': 'slide-up 0.3s ease-out',
        'spin-slow': 'spin-slow 2s linear infinite',
      },
    },
  },
  plugins: [],
}
