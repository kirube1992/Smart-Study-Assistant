# Smart Study Assistant - API Documentation

## Base URL

Local: `http://localhost:8000`  
Production: `https://your-domain.com`

## Authentication

Currently, the API is open (no authentication required). In production, implement JWT or API key authentication.

---

## Endpoints

### Health & Info

#### Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "service": "Smart Study Assistant API"
}
```

#### API Info
```
GET /info
```
**Response:**
```json
{
  "name": "Smart Study Assistant API",
  "description": "AI-powered learning companion",
  "phase": 5,
  "features": [...],
  "documents_count": 10
}
```

---

### Document Management

#### List Documents
```
GET /documents?skip=0&limit=10
```

**Parameters:**
- `skip` (int): Skip first N documents
- `limit` (int): Return at most N documents

**Response:**
```json
{
  "documents": [
    {
      "id": 0,
      "title": "Introduction to ML",
      "file_path": "notes.txt",
      "ingestion_date": "2024-02-05",
      "content_preview": "Machine learning is...",
      "word_count": 1500,
      "document_type": "lecture",
      "difficulty_score": 3.5
    }
  ],
  "total": 15,
  "skip": 0,
  "limit": 10,
  "has_more": true
}
```

#### Get Document
```
GET /documents/{doc_id}
```

**Parameters:**
- `doc_id` (int): Document ID

**Response:**
```json
{
  "id": 0,
  "title": "Introduction to ML",
  "content": "...",
  "file_path": "notes.txt",
  "ingestion_date": "2024-02-05",
  "document_type": "lecture",
  "difficulty_score": 3.5,
  "word_count": 1500
}
```

#### Ingest Document
```
POST /documents/ingest
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "My Lecture Notes",
  "content": "Complete text content of the document...",
  "document_type": "lecture",
  "file_path": "/path/to/file.txt"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Document 'My Lecture Notes' ingested successfully",
  "total_documents": 11,
  "document_id": 10
}
```

**Document Types:**
- `lecture` - Lecture notes
- `textbook` - Textbook chapters
- `article` - Articles or blog posts
- `research_paper` - Academic papers
- `problem_set` - Exercises or problems
- `tutorial` - Learning tutorials
- (custom types supported)

---

### Search

#### Semantic Search
```
POST /documents/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "machine learning algorithms",
  "top_k": 5,
  "threshold": 0.2
}
```

**Parameters:**
- `query` (string, required): Search query
- `top_k` (int): Return top K results (default: 5)
- `threshold` (float): Minimum similarity score (0-1, default: 0.2)

**Response:**
```json
{
  "results": [
    {
      "id": 2,
      "title": "ML Fundamentals",
      "similarity_score": 0.92,
      "content_preview": "Machine learning algorithms...",
      "document_type": "lecture"
    }
  ],
  "total_results": 3,
  "query": "machine learning algorithms"
}
```

---

### Summarization

#### Summarize Documents
```
POST /documents/summarize
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "neural networks",
  "top_k": 3,
  "threshold": 0.2
}
```

**Response:**
```json
{
  "query": "neural networks",
  "summaries": [
    {
      "title": "Deep Learning Intro",
      "summary": "Neural networks are...",
      "similarity_score": 0.89,
      "content_preview": "..."
    }
  ],
  "count": 2
}
```

---

### Q&A System

#### Ask Question
```
POST /qa/ask
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "What is backpropagation?",
  "use_agent": false
}
```

**Parameters:**
- `question` (string, required): Your question
- `use_agent` (boolean): Use AI agent for complex reasoning (default: false)

**Response:**
```json
{
  "answer": "Backpropagation is a method for computing...",
  "question": "What is backpropagation?",
  "method": "search_based",
  "tool_used": "document_search_tool"
}
```

With `use_agent: true`:
```json
{
  "answer": "Backpropagation is a supervised learning algorithm...",
  "question": "What is backpropagation?",
  "method": "agent",
  "tool_used": "document_search_tool",
  "intent": "search"
}
```

---

### Analysis

#### Get Analytics Dashboard
```
GET /analytics/dashboard
```

**Response:**
```json
{
  "total_documents": 15,
  "average_word_count": 1250.5,
  "common_words": [
    ["learning", 45],
    ["machine", 38],
    ["data", 35]
  ],
  "document_types": {
    "lecture": 8,
    "article": 5,
    "research_paper": 2
  }
}
```

#### Predict Difficulty
```
POST /analysis/difficulty
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Complex Paper",
  "content": "The underlying mathematical formulation..."
}
```

**Response:**
```json
{
  "content_preview": "The underlying mathematical...",
  "predicted_difficulty": "4.2",
  "method": "ML Classifier"
}
```

#### Classify Document
```
POST /analysis/classify
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Article",
  "content": "This article discusses recent advances..."
}
```

**Response:**
```json
{
  "content_preview": "This article discusses recent...",
  "predicted_type": "article",
  "method": "ML Classifier"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Not found (document doesn't exist)
- `500` - Server error

### Examples

**Invalid Request:**
```json
{
  "detail": "Failed to ingest document: Invalid input"
}
```

**Document Not Found:**
```json
{
  "detail": "Document not found"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, add rate limiting based on:
- IP address
- API key
- User account

---

## Pagination

Use `skip` and `limit` parameters for pagination:

```bash
# Get first 10 documents
GET /documents?skip=0&limit=10

# Get next 10 documents
GET /documents?skip=10&limit=10

# Get documents 20-30
GET /documents?skip=20&limit=10
```

---

## Batch Operations

Currently not supported. To process multiple documents:

```bash
# Call ingest endpoint multiple times
for doc in documents/*.txt; do
  curl -X POST "http://localhost:8000/documents/ingest" \
    -H "Content-Type: application/json" \
    -d "{...}"
done
```

---

## Performance Tips

1. **Search**: Use `threshold` to filter out low-relevance results
2. **Large Queries**: Increase `top_k` cautiously (higher = slower)
3. **Batch Operations**: Use reasonable batch sizes (10-50 documents)
4. **Caching**: Results are cached automatically

---

## Interactive API Documentation

When running the backend, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive API exploration with try-it-out functionality.

---

## SDK Usage Examples

### Python
```python
import requests

# Search documents
response = requests.post('http://localhost:8000/documents/search', json={
    'query': 'machine learning',
    'top_k': 5
})
results = response.json()
print(results['results'])
```

### JavaScript/TypeScript
```typescript
// Ask a question
const response = await fetch('http://localhost:8000/qa/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What is backpropagation?',
    use_agent: true
  })
});
const data = await response.json();
console.log(data.answer);
```

### cURL
```bash
# Get analytics
curl http://localhost:8000/analytics/dashboard | json_pp
```

---

## Deployment Considerations

### Production Checklist

- [ ] Enable HTTPS/SSL
- [ ] Implement authentication (JWT/API keys)
- [ ] Add rate limiting
- [ ] Enable CORS properly (don't use `*`)
- [ ] Add request validation
- [ ] Setup logging and monitoring
- [ ] Use environment variables for configuration
- [ ] Setup database for persistence
- [ ] Add request/response caching
- [ ] Setup error tracking (Sentry, etc.)

### Environment Variables

```env
API_URL=http://localhost:8000
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000
DATABASE_URL=...
```

---

## Support

For API issues:
1. Check `http://localhost:8000/docs` for interactive testing
2. Check error message in response
3. Review logs in terminal running `uvicorn`
4. Open an issue on GitHub

---

## Version History

- **v1.0.0** (Current) - Initial release with core features
- Planned: v1.1.0 - Batch operations
- Planned: v1.2.0 - Authentication & rate limiting
