// config/fonts.ts
import localFont from 'next/font/local'
import { Fira_Code as FontMono, Inter as FontSans } from 'next/font/google'

export const fontSans = FontSans({
  subsets: ['latin'],
  variable: '--font-sans',
})

export const fontMono = FontMono({
  subsets: ['latin'],
  variable: '--font-mono',
})

export const fontBebas = localFont({
  src: '../public/fonts/BebasNeue-Regular.ttf',
  weight: '400',
  style: 'normal',
  variable: '--font-bebas',
})
