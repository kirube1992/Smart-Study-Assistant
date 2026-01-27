# src/ssa/agent/simple_agent.py (FIXED VERSION)
"""
Week 14: AI Agent from Scratch - FIXED VERSION
No external dependencies - uses your existing code
"""

class StudyBuddyAgent:
    """
    SIMPLE AI AGENT that follows Week 14 roadmap:
    1. Has 3 tools (Week 8, 12)
    2. Decides which tool to use
    3. Can handle complex questions (search → LLM)
    """
    
    def __init__(self, document_manager):
        print("\n" + "=" * 60)
        print("🤖 BUILDING WEEK 14 AGENT FROM SCRATCH")
        print("=" * 60)
        
        self.manager = document_manager
        self.tool_usage_count = {"search": 0, "summary": 0, "classify": 0}
        
        # Show roadmap requirements
        print("\n📋 WEEK 14 ROADMAP:")
        print("   • Agent with 3 tools (Week 8, 12)")
        print("   • Automatic tool selection")
        print("   • Complex questions: search → LLM")
        print("=" * 60)
    
    def ask(self, user_question):
        """
        Main method - processes any user question
        """
        print(f"\n👤 USER: {user_question}")
        print("-" * 50)
        
        # Step 1: UNDERSTAND what user wants
        intent = self._understand_intent(user_question)
        print(f"🤔 AGENT THINKS: '{intent}'")
        
        # Step 2: DECIDE which tool to use
        tool_choice = self._choose_tool(intent, user_question)
        print(f"🔧 AGENT DECIDES: Use {tool_choice['name']}")
        print(f"   Reason: {tool_choice['reason']}")
        
        # Step 3: USE the tool
        print("⚡ AGENT ACTS: Using the tool...")
        tool_result = tool_choice["function"](user_question)
        
        # Step 4: RESPOND
        print("💬 AGENT RESPONDS:")
        print("-" * 40)
        print(tool_result)
        
        # Track usage
        self.tool_usage_count[tool_choice["type"]] += 1
        
        return {
            "question": user_question,
            "intent": intent,
            "tool_used": tool_choice["name"],
            "result": tool_result,
            "agent_version": "SimpleWeek14"
        }
    
    def _understand_intent(self, question):
        """
        Simple intent understanding
        Returns: "search", "summary", "classify", or "complex"
        """
        question_lower = question.lower()
        
        # Fix common spelling mistakes
        corrections = {
            "summerize": "summarize",
            "summarise": "summarize",
            "categorise": "categorize",
            "clasify": "classify"
        }
        
        for wrong, right in corrections.items():
            question_lower = question_lower.replace(wrong, right)
        
        # Check for keywords
        search_keywords = ["search", "find", "look for", "where is", "locate"]
        summary_keywords = ["summarize", "summary", "brief", "overview", "short"]
        classify_keywords = ["categorize", "classify", "type", "category", "sort"]
        
        # Count matches
        search_matches = sum(1 for word in search_keywords if word in question_lower)
        summary_matches = sum(1 for word in summary_keywords if word in question_lower)
        classify_matches = sum(1 for word in classify_keywords if word in question_lower)
        
        # Determine intent
        if search_matches > 0:
            return "search"
        elif summary_matches > 0:
            return "summary"
        elif classify_matches > 0:
            return "classify"
        elif "?" in question or any(word in question_lower for word in ["what", "how", "why", "explain"]):
            return "complex"
        else:
            return "general"
    
    def _choose_tool(self, intent, question):
        """
        Choose the right tool based on intent
        Returns tool information
        """
        if intent == "search":
            return {
                "type": "search",
                "name": "document_search_tool (Week 12)",
                "function": self._use_search_tool,
                "reason": "User is searching for information"
            }
        elif intent == "summary":
            return {
                "type": "summary",
                "name": "document_summary_tool (Week 12)",
                "function": self._use_summary_tool,
                "reason": "User wants a summary"
            }
        elif intent == "classify":
            return {
                "type": "classify",
                "name": "document_categorizer_tool (Week 8)",
                "function": self._use_classify_tool,
                "reason": "User wants to categorize something"
            }
        elif intent == "complex":
            # FIXED: Changed _handle_complex_query to _handle_complex_question
            return {
                "type": "search",  # Complex questions start with search
                "name": "Complex Query Handler",
                "function": self._handle_complex_question,  # FIXED!
                "reason": "Complex question - will search first, then answer"
            }
        else:
            return {
                "type": "search",
                "name": "General Query Handler",
                "function": self._handle_general_query,
                "reason": "General request - starting with search"
            }
    
    def _execute_action(self, action, question):
        """Execute the chosen tool"""
        print(f"🤔 Thought: {action['description']}")
        print(f"🔧 Action: {action['name'].upper()}")
        print(f"📝 Input: {question[:50]}...")
        
        try:
            result = action["tool"](question)
            print(f"✅ Success: {len(str(result))} characters")
            return result
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"Error in {action['name']}: {str(e)}"
    
    # Tool implementations (same as before but simplified)
    def _use_search_tool(self, query):
        """Search for documents"""
        try:
            results = self.manager.semantic_search(query, top_k=3, threshold=0.2)
            
            if not results:
                return "No relevant documents found."
            
            output = ["🔍 **SEARCH RESULTS:**", "=" * 40]
            for i, result in enumerate(results, 1):
                output.append(f"{i}. {result['title']}")
                output.append(f"   Similarity: {result['similarity']:.3f}")
                output.append(f"   Preview: {result['content_preview'][:80]}...")
                output.append("")
            
            return "\n".join(output)
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _use_summary_tool(self, query):
        """Summarize documents on a topic"""
        try:
            # Find relevant documents
            results = self.manager.semantic_search(query, top_k=2, threshold=0.2)
            
            if not results:
                return "No documents to summarize."
            
            output = ["📝 **SUMMARIES:**", "=" * 40]
            for i, result in enumerate(results, 1):
                doc = result["document"]
                # Simple summary (first 150 chars)
                summary = doc.content[:150] + "..." if len(doc.content) > 150 else doc.content
                output.append(f"{i}. {doc.title}")
                output.append(f"   {summary}")
                output.append("")
            
            return "\n".join(output)
        except Exception as e:
            return f"Summarization error: {str(e)}"
    
    def _use_classify_tool(self, query):
        """Use Week 8 classifier"""
        try:
            if hasattr(self.manager, 'predict_document_type'):
                # Check if query is document content or a search term
                if len(query) > 100:  # Likely document content
                    category = self.manager.predict_document_type(query)
                    return f"🏷️ **DOCUMENT CLASSIFICATION:**\nPredicted category: {category}"
                else:
                    # Search for a document first
                    if hasattr(self.manager, 'semantic_search'):
                        results = self.manager.semantic_search(query, top_k=1)
                        if results:
                            doc = results[0]["document"]
                            category = self.manager.predict_document_type(doc.content[:500])
                            return f"🏷️ **DOCUMENT CLASSIFICATION:**\nDocument: {doc.title}\nPredicted category: {category}"
                        else:
                            return "No document found to classify."
                    else:
                        return "Semantic search not available for finding documents."
            else:
                return "Week 8 classifier not trained. Please train document type classifier first."
        except Exception as e:
            return f"Classification error: {str(e)}"
    
    def _handle_complex_question(self, query):
        """Handle complex questions: search → LLM"""
        try:
            print("   🤖 Detected complex question - using search then LLM")
            
            # Step 1: Search for relevant documents
            search_result = self._use_search_tool(query)
            
            # Step 2: Use LLM to answer based on search results
            if hasattr(self.manager, 'ask_llm'):
                llm_result = self.manager.ask_llm(f"Based on these search results: {search_result[:500]}...\n\nQuestion: {query}")
                
                if isinstance(llm_result, dict) and 'answer' in llm_result:
                    answer = llm_result['answer']
                else:
                    answer = str(llm_result)
                
                response = ["🤖 **AI ANSWER**", "=" * 40]
                response.append(f"\n{answer}")
                response.append(f"\n\n🔍 **Search Context:**")
                response.append(search_result[:300] + "..." if len(search_result) > 300 else search_result)
                
                return "\n".join(response)
            else:
                # Fallback to just search results
                return f"🔍 **SEARCH RESULTS FOR YOUR QUESTION:**\n\n{search_result}\n\n💡 Tip: Install LLM features for AI-powered answers."
        except Exception as e:
            return f"Error handling complex question: {str(e)}"
    
    def _handle_general_query(self, query):
        """Handle general queries"""
        return self._use_search_tool(query)
    
    def show_stats(self):
        """Show agent statistics"""
        print("\n📊 AGENT STATISTICS")
        print("=" * 40)
        total = sum(self.tool_usage_count.values())
        
        if total > 0:
            for tool_type, count in self.tool_usage_count.items():
                percentage = (count / total) * 100
                print(f"{tool_type.upper()}: {count} uses ({percentage:.1f}%)")
        else:
            print("No queries processed yet.")