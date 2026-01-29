import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import './globals.css'

const geistSans = Geist({ subsets: ['latin'] })
const geistMono = Geist_Mono({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Smart Study Assistant',
  description: 'AI-powered learning companion that helps you study better',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=5',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.className} ${geistMono.className} bg-background text-foreground antialiased`}
        suppressHydrationWarning
      >
        <div className="min-h-screen w-full">
          {children}
        </div>
      </body>
    </html>
  )
}
