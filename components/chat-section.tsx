"use client";

import { useState, useRef, useEffect } from "react";
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Send, Loader2, MessageCircle } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatSectionProps {
  uploadedFile: File | null;
  isProcessing: boolean;
}

export default function ChatSection({
  uploadedFile,
  isProcessing,
}: ChatSectionProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isProcessing && messages.length === 0) {
      // Add initial assistant message when file is processed
      const welcomeMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: `I've successfully loaded "${uploadedFile?.name}". What would you like to know about it? You can ask me to summarize, explain concepts, answer questions, or analyze specific sections.`,
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  }, [isProcessing, uploadedFile, messages.length]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate API call to backend
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: generateMockResponse(input),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);

    inputRef.current?.focus();
  };

  const generateMockResponse = (question: string): string => {
    const responses: { [key: string]: string } = {
      summary:
        "The document provides a comprehensive overview of the key concepts. It covers the main topics with detailed explanations and practical examples. The material is structured to help you understand progressively from basic to advanced concepts.",
      summary_lower:
        "The document provides a comprehensive overview of the key concepts. It covers the main topics with detailed explanations and practical examples.",
      explain:
        "This concept refers to the fundamental principles outlined in the material. Based on the document, it involves several key components: 1) The foundational elements, 2) The practical applications, and 3) The real-world implications. Each of these aspects is crucial for understanding the broader topic.",
      explain_lower:
        "This concept refers to the fundamental principles outlined in the material. The document explains it through examples and detailed breakdowns.",
      default:
        "Based on the document you uploaded, this is an interesting question. The material addresses this by explaining that it depends on several factors. Key points include understanding the context, applying relevant principles, and considering practical applications. Would you like me to dive deeper into any specific aspect?",
    };

    const lowerQuestion = question.toLowerCase();
    if (
      lowerQuestion.includes("summary") ||
      lowerQuestion.includes("summarize")
    ) {
      return responses.summary;
    }
    if (
      lowerQuestion.includes("explain") ||
      lowerQuestion.includes("what is")
    ) {
      return responses.explain;
    }
    return responses.default;
  };

  return (
    <Card className="h-full min-h-96 flex flex-col bg-card/50 backdrop-blur-sm border border-border/50 overflow-hidden">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-center">
            <div className="max-w-xs">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <MessageCircle className="w-6 h-6 text-primary" />
              </div>
              <p className="text-muted-foreground text-sm">
                Loading document... Ready to answer your questions about the
                content.
              </p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"} animate-fade-in`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                  message.role === "user"
                    ? "bg-primary text-primary-foreground rounded-br-none"
                    : "bg-muted text-foreground rounded-bl-none"
                }`}
              >
                <p className="text-sm leading-relaxed">{message.content}</p>
                <span
                  className={`text-xs mt-1 block ${
                    message.role === "user"
                      ? "text-primary-foreground/70"
                      : "text-muted-foreground"
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-muted text-foreground px-4 py-3 rounded-lg rounded-bl-none flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-border p-4 bg-background/50">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            placeholder="Ask a question about your document..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading || isProcessing}
            className="flex-1 px-4 py-2 rounded-lg bg-card border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent disabled:opacity-50"
          />
          <Button
            type="submit"
            disabled={isLoading || isProcessing || !input.trim()}
            className="bg-primary hover:bg-primary/90 text-primary-foreground disabled:opacity-50"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </form>
        <p className="text-xs text-muted-foreground mt-2">
          Ask questions about your document. The AI will provide answers based
          on the content.
        </p>
      </div>
    </Card>
  );
}
