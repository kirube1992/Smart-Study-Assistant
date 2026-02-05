'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Search as SearchIcon } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface SearchResult {
  id: number
  title: string
  similarity_score: number
  content_preview: string
  document_type?: string
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/documents/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          top_k: 10,
          threshold: 0.2
        })
      })

      if (!response.ok) throw new Error('Search failed')

      const data = await response.json()
      setResults(data.results || [])
    } catch (error) {
      console.error('Search error:', error)
      toast({
        title: 'Search Error',
        description: 'Failed to perform search',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8 py-8 px-4 md:px-8 lg:px-12 max-w-4xl mx-auto">
      <div>
        <h1 className="text-4xl font-bold mb-2">Semantic Search</h1>
        <p className="text-muted-foreground">Search your documents by meaning, not just keywords</p>
      </div>

      <form onSubmit={handleSearch} className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="Search your documents..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="text-lg"
          />
          <Button type="submit" size="icon" disabled={loading}>
            <SearchIcon className="w-4 h-4" />
          </Button>
        </div>
      </form>

      {results.length > 0 && (
        <div className="space-y-4">
          <div className="text-sm text-muted-foreground">
            Found {results.length} relevant documents
          </div>
          
          {results.map((result) => (
            <Card key={result.id} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <CardTitle>{result.title}</CardTitle>
                    {result.document_type && (
                      <CardDescription className="mt-1">
                        Type: {result.document_type}
                      </CardDescription>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold text-accent">
                      {(result.similarity_score * 100).toFixed(1)}% Match
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-sm">
                  {result.content_preview}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {!loading && query && results.length === 0 && (
        <Card className="bg-muted/50">
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">No documents found matching your query</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
