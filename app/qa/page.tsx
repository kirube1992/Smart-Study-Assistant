'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { SendHorizontal } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface QAResponse {
  answer: string
  question: string
  method: string
  tool_used?: string
  intent?: string
}

export default function QAPage() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState<QAResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [useAgent, setUseAgent] = useState(false)
  const { toast } = useToast()

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    try {
      const apiResponse = await fetch('http://localhost:8000/qa/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          use_agent: useAgent
        })
      })

      if (!apiResponse.ok) throw new Error('Q&A failed')

      const data = await apiResponse.json()
      setResponse(data)
    } catch (error) {
      console.error('Q&A error:', error)
      toast({
        title: 'Error',
        description: 'Failed to get answer. Make sure the API server is running.',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8 py-8 px-4 md:px-8 lg:px-12 max-w-4xl mx-auto">
      <div>
        <h1 className="text-4xl font-bold mb-2">Ask a Question</h1>
        <p className="text-muted-foreground">Get intelligent answers from your study materials</p>
      </div>

      <form onSubmit={handleAsk} className="space-y-4">
        <div className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="Ask a question about your study materials..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="text-base"
              disabled={loading}
            />
            <Button type="submit" size="icon" disabled={loading}>
              <SendHorizontal className="w-4 h-4" />
            </Button>
          </div>

          <div className="flex items-center space-x-2">
            <Checkbox
              id="agent"
              checked={useAgent}
              onCheckedChange={(checked) => setUseAgent(checked as boolean)}
            />
            <label htmlFor="agent" className="text-sm font-medium cursor-pointer">
              Use AI Agent (more sophisticated reasoning)
            </label>
          </div>
        </div>
      </form>

      {response && (
        <Card className="border-accent/50 bg-accent/5">
          <CardHeader>
            <CardTitle className="text-lg">Answer</CardTitle>
            <CardDescription>
              Method: {response.method}
              {response.tool_used && ` (Tool: ${response.tool_used})`}
              {response.intent && ` (Intent: ${response.intent})`}
            </CardDescription>
          </CardHeader>
          <CardContent className="prose prose-sm dark:prose-invert max-w-none">
            <p className="text-foreground whitespace-pre-wrap">{response.answer}</p>
          </CardContent>
        </Card>
      )}

      {!response && !loading && (
        <Card className="bg-muted/50">
          <CardContent className="text-center py-12">
            <p className="text-muted-foreground">Ask a question to get started</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
