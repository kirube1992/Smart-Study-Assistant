import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ArrowRight, BookOpen, Brain, BarChart3, Zap } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="space-y-16 py-12 px-4 md:px-8 lg:px-12">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-3xl mx-auto py-12">
        <div className="inline-block">
          <span className="px-4 py-2 rounded-full bg-accent/10 text-accent text-sm font-medium">
            Your AI Learning Companion
          </span>
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
          <span className="text-gradient">Smart Study Assistant</span>
        </h1>
        
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Transform your learning experience with AI-powered semantic search, intelligent Q&A, and personalized study guidance.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link href="/documents">
            <Button size="lg" className="gap-2">
              Get Started <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
          <Link href="/about">
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <BookOpen className="w-8 h-8 text-primary mb-2" />
            <CardTitle>Smart Document Management</CardTitle>
            <CardDescription>
              Organize and store study materials with automatic categorization and metadata extraction
            </CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Upload, organize, and manage all your study materials in one intelligent system
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <Zap className="w-8 h-8 text-accent mb-2" />
            <CardTitle>Semantic Search</CardTitle>
            <CardDescription>
              Find information based on meaning, not just keywords
            </CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Advanced semantic understanding lets you find exactly what you need instantly
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <Brain className="w-8 h-8 text-secondary mb-2" />
            <CardTitle>AI-Powered Q&A</CardTitle>
            <CardDescription>
              Get contextual answers to your questions based on your study materials
            </CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Ask complex questions and receive precise answers with source citations
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <BarChart3 className="w-8 h-8 text-accent mb-2" />
            <CardTitle>Learning Analytics</CardTitle>
            <CardDescription>
              Track your learning progress with detailed insights and recommendations
            </CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Monitor difficulty levels, content clustering, and personalized learning paths
          </CardContent>
        </Card>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary/5 to-accent/5 rounded-lg p-8 text-center max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Learning?</h2>
        <p className="text-muted-foreground mb-6 text-lg">
          Start by uploading your study materials and explore our AI-powered features.
        </p>
        <Link href="/documents">
          <Button size="lg" className="gap-2">
            Upload Documents <ArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </section>
    </div>
  )
}
