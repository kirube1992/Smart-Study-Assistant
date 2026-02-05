'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { RefreshCw, Loader } from 'lucide-react'

interface Document {
  id: number
  title: string
  file_path: string
  ingestion_date: string
  content_preview: string
  word_count?: number
  document_type?: string
  difficulty_score?: number
}

interface DocumentListProps {
  documents: Document[]
  loading: boolean
  onRefresh: () => void
}

export function DocumentList({ documents, loading, onRefresh }: DocumentListProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader className="w-8 h-8 text-primary animate-spin" />
      </div>
    )
  }

  if (documents.length === 0) {
    return (
      <Card className="bg-muted/50">
        <CardContent className="text-center py-12">
          <p className="text-muted-foreground mb-4">No documents yet</p>
          <p className="text-sm text-muted-foreground">
            Upload your first document to get started
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <p className="text-sm text-muted-foreground">
          Showing {documents.length} document{documents.length !== 1 ? 's' : ''}
        </p>
        <Button variant="outline" size="sm" onClick={onRefresh}>
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid gap-4">
        {documents.map((doc) => (
          <Card key={doc.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start gap-4">
                <div>
                  <CardTitle className="text-lg">{doc.title}</CardTitle>
                  <CardDescription>
                    {doc.document_type && <span>Type: {doc.document_type} • </span>}
                    {new Date(doc.ingestion_date).toLocaleDateString()}
                  </CardDescription>
                </div>
                {doc.difficulty_score && (
                  <div className="text-right">
                    <div className="text-sm font-semibold text-secondary">
                      Difficulty
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {doc.difficulty_score.toFixed(1)}/5
                    </div>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                {doc.content_preview}
              </p>
              {doc.word_count && (
                <p className="text-xs text-muted-foreground">
                  Word count: {doc.word_count}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
