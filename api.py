"""
FastAPI Backend for Smart Study Assistant
Phase 5: MLOps & Deployment
Exposes all SSA functionalities via REST API
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
from pathlib import Path

# Import core SSA components
from src.ssa.core.manager import DocumentManager
from src.ssa.agent.simple_agent import StudyBuddyAgent

# Initialize FastAPI app
app = FastAPI(
    title="Smart Study Assistant API",
    description="AI-powered study companion with semantic search, Q&A, and personalized learning",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document manager and agent
document_manager = DocumentManager(storage_file="data/documents.json")
study_buddy_agent = StudyBuddyAgent(document_manager)

# ============================================================================
# Pydantic Models for Request/Response
# ============================================================================

class DocumentInput(BaseModel):
    title: str
    content: str
    document_type: Optional[str] = None
    file_path: Optional[str] = None

class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5
    threshold: Optional[float] = 0.2

class QuestionQuery(BaseModel):
    question: str
    use_agent: Optional[bool] = False

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_path: str
    ingestion_date: str
    content_preview: str
    document_type: Optional[str] = None
    difficulty_score: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_results: int
    query: str

class AgentResponse(BaseModel):
    question: str
    intent: str
    tool_used: str
    result: str
    agent_version: str

class AnalyticsResponse(BaseModel):
    total_documents: int
    average_word_count: float
    common_words: List[tuple]
    document_types: Dict[str, int]

# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.get("/health")
def health_check():
    """Check API health status"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "service": "Smart Study Assistant API"
    }

@app.get("/info")
def get_info():
    """Get API and project information"""
    return {
        "name": "Smart Study Assistant API",
        "description": "AI-powered learning companion",
        "phase": 5,
        "features": [
            "Document Management",
            "Semantic Search",
            "Document Summarization",
            "Q&A System",
            "Difficulty Classification",
            "AI Agent Orchestration"
        ],
        "documents_count": len(document_manager.documents)
    }

# ============================================================================
# Document Management Endpoints
# ============================================================================

@app.post("/documents/ingest", response_model=Dict[str, Any])
def ingest_document(doc_input: DocumentInput):
    """Ingest a new document into the knowledge base"""
    try:
        # Add document to manager
        document_manager.add_document(
            title=doc_input.title,
            content=doc_input.content,
            file_path=doc_input.file_path or "",
            document_type=doc_input.document_type
        )
        
        # Save to persistent storage
        document_manager.save_documents()
        
        return {
            "status": "success",
            "message": f"Document '{doc_input.title}' ingested successfully",
            "total_documents": len(document_manager.documents),
            "document_id": len(document_manager.documents) - 1
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to ingest document: {str(e)}")

@app.get("/documents", response_model=Dict[str, Any])
def list_documents(skip: int = 0, limit: int = 10):
    """List all documents with pagination"""
    try:
        all_docs = document_manager.documents
        total = len(all_docs)
        paginated_docs = all_docs[skip:skip + limit]
        
        docs_response = []
        for idx, doc in enumerate(paginated_docs, start=skip):
            docs_response.append({
                "id": idx,
                "title": doc.title,
                "file_path": doc.file_path,
                "ingestion_date": doc.ingestion_date,
                "content_preview": doc.content[:150] + "..." if len(doc.content) > 150 else doc.content,
                "word_count": len(doc.preprocess_text()),
                "document_type": getattr(doc, 'document_type', None),
                "difficulty_score": getattr(doc, 'difficulty_score', None)
            })
        
        return {
            "documents": docs_response,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to list documents: {str(e)}")

@app.get("/documents/{doc_id}", response_model=Dict[str, Any])
def get_document(doc_id: int):
    """Get a specific document by ID"""
    try:
        if doc_id < 0 or doc_id >= len(document_manager.documents):
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc = document_manager.documents[doc_id]
        return {
            "id": doc_id,
            "title": doc.title,
            "content": doc.content,
            "file_path": doc.file_path,
            "ingestion_date": doc.ingestion_date,
            "document_type": getattr(doc, 'document_type', None),
            "difficulty_score": getattr(doc, 'difficulty_score', None),
            "word_count": len(doc.preprocess_text())
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve document: {str(e)}")

# ============================================================================
# Search Endpoints
# ============================================================================

@app.post("/documents/search", response_model=SearchResponse)
def search_documents(search_query: SearchQuery):
    """Perform semantic search on documents"""
    try:
        results = document_manager.semantic_search(
            query=search_query.query,
            top_k=search_query.top_k,
            threshold=search_query.threshold
        )
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": document_manager.documents.index(result['document']),
                "title": result['title'],
                "similarity_score": float(result['similarity']),
                "content_preview": result['content_preview'],
                "document_type": getattr(result['document'], 'document_type', None)
            })
        
        return SearchResponse(
            results=formatted_results,
            total_results=len(formatted_results),
            query=search_query.query
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")

# ============================================================================
# Summarization Endpoints
# ============================================================================

@app.post("/documents/summarize", response_model=Dict[str, Any])
def summarize_documents(search_query: SearchQuery):
    """Get summaries of semantically relevant documents"""
    try:
        results = document_manager.semantic_search(
            query=search_query.query,
            top_k=search_query.top_k,
            threshold=search_query.threshold
        )
        
        summaries = []
        for result in results:
            doc = result['document']
            summary = document_manager.get_summary(doc)
            summaries.append({
                "title": doc.title,
                "summary": summary,
                "similarity_score": float(result['similarity']),
                "content_preview": result['content_preview']
            })
        
        return {
            "query": search_query.query,
            "summaries": summaries,
            "count": len(summaries)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Summarization failed: {str(e)}")

# ============================================================================
# Q&A Endpoints
# ============================================================================

@app.post("/qa/ask", response_model=Dict[str, Any])
def answer_question(question_query: QuestionQuery):
    """Answer a question based on documents"""
    try:
        if question_query.use_agent:
            # Use AI agent for complex queries
            agent_response = study_buddy_agent.ask(question_query.question)
            return {
                "answer": agent_response['result'],
                "question": question_query.question,
                "method": "agent",
                "tool_used": agent_response['tool_used'],
                "intent": agent_response['intent']
            }
        else:
            # Use simple search-based Q&A
            answer_result = document_manager.ask_question(question_query.question)
            return {
                "answer": answer_result,
                "question": question_query.question,
                "method": "search_based"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Q&A failed: {str(e)}")

# ============================================================================
# Analysis Endpoints
# ============================================================================

@app.get("/analytics/dashboard", response_model=AnalyticsResponse)
def get_analytics_dashboard():
    """Get analytics about the knowledge base"""
    try:
        # Get basic stats
        df = document_manager.to_dataframe()
        
        if df is None or len(df) == 0:
            return AnalyticsResponse(
                total_documents=0,
                average_word_count=0.0,
                common_words=[],
                document_types={}
            )
        
        total_docs = len(df)
        avg_word_count = float(df['word_count'].mean())
        
        # Get common words
        from collections import Counter
        all_words = []
        for doc in document_manager.documents:
            if not doc.tokens:
                doc.preprocess_text()
            all_words.extend(doc.tokens)
        
        common_words = Counter(all_words).most_common(10)
        
        # Get document types
        doc_types = {}
        for doc in document_manager.documents:
            doc_type = getattr(doc, 'document_type', 'Unknown')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        return AnalyticsResponse(
            total_documents=total_docs,
            average_word_count=avg_word_count,
            common_words=common_words,
            document_types=doc_types
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analytics failed: {str(e)}")

# ============================================================================
# Classification Endpoints
# ============================================================================

@app.post("/analysis/difficulty", response_model=Dict[str, Any])
def predict_difficulty(doc_input: DocumentInput):
    """Predict difficulty score of content"""
    try:
        difficulty = document_manager.predict_difficulty(doc_input.content)
        return {
            "content_preview": doc_input.content[:100] + "...",
            "predicted_difficulty": str(difficulty),
            "method": "ML Classifier"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Difficulty prediction failed: {str(e)}")

@app.post("/analysis/classify", response_model=Dict[str, Any])
def classify_document(doc_input: DocumentInput):
    """Classify document type"""
    try:
        doc_type = document_manager.predict_document_type(doc_input.content)
        return {
            "content_preview": doc_input.content[:100] + "...",
            "predicted_type": str(doc_type),
            "method": "ML Classifier"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Classification failed: {str(e)}")

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
def root():
    """Root endpoint with API overview"""
    return {
        "service": "Smart Study Assistant API",
        "version": "1.0.0",
        "phase": "Phase 5 - MLOps & Deployment",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "documents": {
                "list": "GET /documents",
                "get": "GET /documents/{doc_id}",
                "ingest": "POST /documents/ingest",
                "search": "POST /documents/search",
                "summarize": "POST /documents/summarize"
            },
            "qa": {
                "ask": "POST /qa/ask"
            },
            "analytics": {
                "dashboard": "GET /analytics/dashboard",
                "difficulty": "POST /analysis/difficulty",
                "classify": "POST /analysis/classify"
            }
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Run with: uvicorn api:app --reload
