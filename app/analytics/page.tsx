'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,  ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { useToast } from '@/hooks/use-toast'
import { Loader } from 'lucide-react'

interface AnalyticsData {
  total_documents: number
  average_word_count: number
  common_words: [string, number][]
  document_types: Record<string, number>
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/analytics/dashboard')
      if (!response.ok) throw new Error('Failed to load analytics')
      
      const data = await response.json()
      setAnalytics(data)
    } catch (error) {
      console.error('Error loading analytics:', error)
      toast({
        title: 'Error',
        description: 'Failed to load analytics. Make sure the API server is running.',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-muted-foreground">Failed to load analytics</p>
      </div>
    )
  }

  const commonWordsData = analytics.common_words.map(([word, count]) => ({
    name: word,
    count
  }))

  const documentTypesData = Object.entries(analytics.document_types).map(([type, count]) => ({
    name: type,
    value: count
  }))

  return (
    <div className="space-y-8 py-8 px-4 md:px-8 lg:px-12">
      <div>
        <h1 className="text-4xl font-bold mb-2">Learning Analytics</h1>
        <p className="text-muted-foreground">Insights into your study materials and learning progress</p>
      </div>

      {/* Key Metrics */}
      <div className="grid md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Total Documents</CardTitle>
            <CardDescription>Number of study materials in your knowledge base</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-primary">
              {analytics.total_documents}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Average Document Length</CardTitle>
            <CardDescription>Average word count per document</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-accent">
              {Math.round(analytics.average_word_count).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground mt-2">words</p>
          </CardContent>
        </Card>
      </div>

      {/* Common Words Chart */}
      {commonWordsData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Most Common Words</CardTitle>
            <CardDescription>Top 10 words across your documents</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={commonWordsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Document Types Distribution */}
      {documentTypesData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Document Types Distribution</CardTitle>
            <CardDescription>Breakdown of documents by type</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex justify-center">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={documentTypesData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {documentTypesData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
