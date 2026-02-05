'use client'

import React from 'react'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode
  className?: string
}

export function Card({ children, className = '', ...props }: CardProps) {
  return (
    <div
      className={`rounded-md shadow-sm p-4 bg-white dark:bg-[#0b0b0b] ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
