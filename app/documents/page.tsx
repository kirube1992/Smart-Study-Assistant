'use client'

import { useState, useEffect } from 'react'
import { DocumentList } from '@/components/documents/document-list'
import { DocumentUpload } from '@/components/documents/document-upload'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useToast } from '@/hooks/use-toast'

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

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/documents?limit=50')
      if (!response.ok) throw new Error('Failed to load documents')
      
      const data = await response.json()
      setDocuments(data.documents || [])
    } catch (error) {
      console.error('Error loading documents:', error)
      toast({
        title: 'Error',
        description: 'Failed to load documents. Make sure the API server is running.',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async (formData: FormData) => {
    setUploading(true)
    try {
      const title = formData.get('title') as string
      const content = formData.get('content') as string
      const documentType = formData.get('documentType') as string

      const response = await fetch('http://localhost:8000/documents/ingest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          content,
          document_type: documentType || undefined
        })
      })

      if (!response.ok) throw new Error('Failed to upload document')

      toast({
        title: 'Success',
        description: 'Document uploaded successfully!'
      })

      await loadDocuments()
    } catch (error) {
      console.error('Error uploading document:', error)
      toast({
        title: 'Error',
        description: 'Failed to upload document',
        variant: 'destructive'
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-8 py-8 px-4 md:px-8 lg:px-12">
      <div>
        <h1 className="text-4xl font-bold mb-2">Documents</h1>
        <p className="text-muted-foreground">Manage and organize your study materials</p>
      </div>

      <Tabs defaultValue="list" className="space-y-4">
        <TabsList>
          <TabsTrigger value="list">Documents ({documents.length})</TabsTrigger>
          <TabsTrigger value="upload">Upload New</TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="space-y-4">
          <DocumentList documents={documents} loading={loading} onRefresh={loadDocuments} />
        </TabsContent>

        <TabsContent value="upload" className="space-y-4">
          <DocumentUpload onUpload={handleUpload} uploading={uploading} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
