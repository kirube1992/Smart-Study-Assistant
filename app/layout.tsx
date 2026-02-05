import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/theme-provider'
import { Navbar } from '@/components/navbar'
import { Toaster } from 'sonner'

const geistSans = Geist({ subsets: ['latin'] })
const geistMono = Geist_Mono({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Smart Study Assistant',
  description: 'AI-powered learning companion with semantic search, Q&A, and personalized learning',
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <style>{`
          :root {
            --background: 0 0% 100%;
            --foreground: 0 0% 3.6%;
            --card: 0 0% 100%;
            --card-foreground: 0 0% 3.6%;
            --primary: 217.2 91.2% 59.8%;
            --primary-foreground: 210 40% 96%;
            --secondary: 217.2 32.6% 17.5%;
            --secondary-foreground: 210 40% 96%;
            --muted: 210 40% 96%;
            --muted-foreground: 215.4 16.3% 46.9%;
            --accent: 142.1 70.6% 45.3%;
            --accent-foreground: 210 40% 96%;
            --destructive: 0 84.2% 60.2%;
            --destructive-foreground: 210 40% 96%;
            --border: 214.3 31.8% 91.4%;
            --input: 214.3 31.8% 91.4%;
            --ring: 217.2 91.2% 59.8%;
            --radius: 0.5rem;
          }
          .dark {
            --background: 222.2 84% 4.9%;
            --foreground: 210 40% 98%;
            --card: 222.2 84% 4.9%;
            --card-foreground: 210 40% 98%;
            --primary: 217.2 91.2% 59.8%;
            --primary-foreground: 222.2 47.4% 11.2%;
            --secondary: 217.2 32.6% 17.5%;
            --secondary-foreground: 210 40% 98%;
            --muted: 217.2 32.6% 17.5%;
            --muted-foreground: 215 20.3% 65.1%;
            --accent: 142.1 70.6% 45.3%;
            --accent-foreground: 222.2 47.4% 11.2%;
            --destructive: 0 62.8% 30.6%;
            --destructive-foreground: 210 40% 98%;
            --border: 217.2 32.6% 17.5%;
            --input: 217.2 32.6% 17.5%;
            --ring: 212.7 26.8% 83.9%;
          }
        `}</style>
      </head>
      <body className={`${geistSans.className} ${geistMono.className}`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <Navbar />
          <main className="min-h-screen bg-background">
            {children}
          </main>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
