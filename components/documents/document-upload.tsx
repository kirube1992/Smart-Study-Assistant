'use client'

import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Upload, Loader } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface DocumentUploadProps {
  onUpload: (formData: FormData) => Promise<void>
  uploading: boolean
}

export function DocumentUpload({ onUpload, uploading }: DocumentUploadProps) {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [documentType, setDocumentType] = useState('')
  const [fileName, setFileName] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { toast } = useToast()

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setFileName(file.name)
    if (!title) {
      setTitle(file.name.replace(/\.[^/.]+$/, ''))
    }

    try {
      const text = await file.text()
      setContent(text)
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to read file',
        variant: 'destructive'
      })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!title.trim() || !content.trim()) {
      toast({
        title: 'Error',
        description: 'Please fill in title and content',
        variant: 'destructive'
      })
      return
    }

    const formData = new FormData()
    formData.append('title', title)
    formData.append('content', content)
    formData.append('documentType', documentType)

    await onUpload(formData)
    
    setTitle('')
    setContent('')
    setDocumentType('')
    setFileName('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Upload a Document</CardTitle>
          <CardDescription>Add a new study material to your knowledge base</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* File Upload Area */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Document File</label>
            <div className="border-2 border-dashed rounded-lg p-6 text-center hover:bg-muted/50 transition-colors">
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt,.pdf,.md"
                onChange={handleFileSelect}
                className="hidden"
                id="file-input"
              />
              <label htmlFor="file-input" className="cursor-pointer">
                <div className="flex flex-col items-center gap-2">
                  <Upload className="w-8 h-8 text-muted-foreground" />
                  <p className="text-sm font-medium">
                    {fileName || 'Click to select or drag and drop'}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Supported: TXT, PDF, Markdown
                  </p>
                </div>
              </label>
            </div>
          </div>

          {/* Title Input */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Title</label>
            <Input
              placeholder="Document title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          {/* Document Type Select */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Document Type (Optional)</label>
            <Select value={documentType} onValueChange={setDocumentType}>
              <SelectTrigger>
                <SelectValue placeholder="Select document type..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="lecture">Lecture Notes</SelectItem>
                <SelectItem value="textbook">Textbook Chapter</SelectItem>
                <SelectItem value="article">Article</SelectItem>
                <SelectItem value="research_paper">Research Paper</SelectItem>
                <SelectItem value="problem_set">Problem Set</SelectItem>
                <SelectItem value="tutorial">Tutorial</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Content Preview */}
          {content && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Content Preview</label>
              <div className="bg-muted p-4 rounded-lg max-h-32 overflow-auto text-sm text-muted-foreground">
                {content.substring(0, 300)}
                {content.length > 300 && '...'}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Button
          type="submit"
          disabled={uploading || !title.trim() || !content.trim()}
          className="gap-2"
        >
          {uploading ? (
            <>
              <Loader className="w-4 h-4 animate-spin" />
              Uploading...
            </>
          ) : (
            <>
              <Upload className="w-4 h-4" />
              Upload Document
            </>
          )}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            setTitle('')
            setContent('')
            setDocumentType('')
            setFileName('')
            if (fileInputRef.current) {
              fileInputRef.current.value = ''
            }
          }}
        >
          Clear
        </Button>
      </div>
    </form>
  )
}
