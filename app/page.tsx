'use client'

import { useState } from 'react'
import FileUploadSection from '@/components/file-upload-section'
import ChatSection from '@/components/chat-section'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BookOpen, Sparkles } from 'lucide-react'

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleFileUpload = (file: File) => {
    setUploadedFile(file)
    setIsProcessing(true)
    // Simulate processing
    setTimeout(() => setIsProcessing(false), 1000)
  }

  const handleClearFile = () => {
    setUploadedFile(null)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-card to-background">
      {/* Header */}
      <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg">
              <BookOpen className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Smart Study</h1>
              <p className="text-xs text-muted-foreground">AI Learning Assistant</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground text-sm">
            <Sparkles className="w-4 h-4" />
            <span>Powered by AI</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: File Upload */}
          <div className="lg:col-span-1">
            <FileUploadSection
              onFileUpload={handleFileUpload}
              uploadedFile={uploadedFile}
              isProcessing={isProcessing}
              onClearFile={handleClearFile}
            />
          </div>

          {/* Right: Chat Interface */}
          <div className="lg:col-span-2">
            {uploadedFile ? (
              <ChatSection uploadedFile={uploadedFile} isProcessing={isProcessing} />
            ) : (
              <Card className="h-full min-h-96 flex flex-col items-center justify-center p-8 text-center bg-card/50 backdrop-blur-sm border border-border/50">
                <div className="max-w-sm">
                  <div className="w-16 h-16 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <BookOpen className="w-8 h-8 text-primary" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground mb-2">No Document Uploaded</h3>
                  <p className="text-muted-foreground text-sm mb-6">
                    Upload a file to start your study session. Ask any question about the content.
                  </p>
                  <div className="flex flex-col gap-2 text-xs text-muted-foreground">
                    <div>Supported formats: PDF, TXT, DOC, DOCX, Images</div>
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>

        {/* Feature Highlights */}
        {!uploadedFile && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12">
            {[
              {
                title: 'Extract Knowledge',
                description: 'Automatically extract key concepts and summaries from any document'
              },
              {
                title: 'Ask Questions',
                description: 'Get instant answers to any question about your uploaded content'
              },
              {
                title: 'Smart Analysis',
                description: 'Receive detailed explanations with context and examples'
              }
            ].map((feature, idx) => (
              <Card key={idx} className="p-6 bg-card/50 backdrop-blur-sm border border-border/50 hover:border-primary/50 transition-colors">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                    <Sparkles className="w-4 h-4 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground mb-1">{feature.title}</h3>
                    <p className="text-sm text-muted-foreground">{feature.description}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}
