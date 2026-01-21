# src/ssa/ml/prompt_engineer.py
class PromptEngineer:
    def __init__(self):
        self.templates = {
            "qa_detailed": """Provide a detailed answer to this question:

Question: {question}

Include:
1. A clear definition
2. Key characteristics
3. Examples if applicable

Answer:""",
            
            "explain_simple": """Explain this simply as if to a beginner:

Concept: {concept}

Use everyday examples and avoid jargon.
Explain in 3-4 sentences.

Simple explanation:""",
            
            "rag_comprehensive": """Based on the provided information, answer the question thoroughly.

Information:
{context}

Question: {question}

Provide a comprehensive answer that uses the information above.
If the information doesn't fully answer, say what's missing.

Comprehensive answer:"""
        }
    
    def format_context(self, documents, max_chars=300):
        """Format context meaningfully"""
        if not documents:
            return "No information available."
        
        context = "Relevant information:\n"
        for i, doc in enumerate(documents[:3], 1):  # Use top 3 only
            content = doc.get('content', doc.get('content_preview', ''))
            title = doc.get('title', f'Source {i}')
            
            # Truncate intelligently
            if len(content) > max_chars:
                # Try to cut at sentence end
                if '.' in content[max_chars-50:max_chars+50]:
                    cut = content[:max_chars].rfind('.') + 1
                    content = content[:cut] + ".."
                else:
                    content = content[:max_chars-3] + "..."
            
            context += f"{i}. From '{title}': {content}\n"
        
        return context.strip()
    
    def build_prompt(self, template_name, **kwargs):
        """Build prompt from template"""
        template = self.templates.get(template_name, "{question}")
        return template.format(**kwargs)
    
    def qa_detailed(self, question):
        return self.build_prompt("qa_detailed", question=question)
    
    def explain_simple(self, concept):
        return self.build_prompt("explain_simple", concept=concept)
    
    def rag_answer(self, context, question):
        return self.build_prompt("rag_comprehensive", context=context, question=question)