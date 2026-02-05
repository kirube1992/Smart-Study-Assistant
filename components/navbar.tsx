'use client'

import Link from 'next/link'
import { BookOpen } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { usePathname } from 'next/navigation'
import { ThemeToggle } from '@/components/theme-toggle'

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/documents', label: 'Documents' },
  { href: '/search', label: 'Search' },
  { href: '/qa', label: 'Q&A' },
  { href: '/analytics', label: 'Analytics' },
]

export function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center justify-between px-4 md:px-8 lg:px-12 max-w-7xl mx-auto w-full">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <BookOpen className="w-6 h-6 text-primary" />
          <span>SSA</span>
        </Link>

        <div className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href}>
              <Button
                variant={pathname === item.href ? 'default' : 'ghost'}
                size="sm"
              >
                {item.label}
              </Button>
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <div className="md:hidden">
            <Button variant="ghost" size="sm">
              Menu
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
