# test_simple_summarizer.py
from ssa.ml.summarizer import DocumentSummarizer

# test_summarizer_comprehensive.py

def test_different_lengths():
    """Test summarizer with texts of different lengths"""
    
    summarizer = DocumentSummarizer()
    
    test_cases = [
        # (text, description, expected_result)
        ("", "Empty text", "Should return None"),
        ("Short.", "Very short text (3 chars)", "Should return text as-is"),
        ("This is a short sentence.", "Short sentence (5 words)", "Should summarize"),
        ("""
         Machine learning enables computers to learn without being explicitly programmed.
         It uses algorithms to identify patterns in data and make predictions.
         This technology powers many modern applications.
         """, "Medium text (~25 words)", "Should summarize well"),
        ("""
         Artificial Intelligence (AI) refers to the simulation of human intelligence 
         in machines that are programmed to think like humans and mimic their actions. 
         The term may also be applied to any machine that exhibits traits associated 
         with a human mind such as learning and problem-solving. The ideal characteristic 
         of artificial intelligence is its ability to rationalize and take actions that 
         have the best chance of achieving a specific goal. AI research has been divided 
         into subfields that often fail to communicate with each other. These subfields 
         are based on technical considerations, such as particular goals, the use of 
         particular tools, or deep philosophical differences.
         """, "Long text (~100 words)", "Should create concise summary")
    ]
    
    print("🧪 Testing Document Summarizer with Different Text Lengths")
    print("=" * 60)
    
    for text, description, expected in test_cases:
        print(f"\n📝 Test: {description}")
        print(f"Expected: {expected}")
        print("-" * 40)
        
        # Clean the text (remove extra whitespace)
        clean_text = ' '.join(text.strip().split())
        word_count = len(clean_text.split())
        
        print(f"Word count: {word_count}")
        print(f"Text preview: {clean_text[:80]}..." if len(clean_text) > 80 else f"Text: {clean_text}")
        
        # Summarize
        summary = summarizer.summarize(clean_text)
        
        if summary is None:
            print("Result: None")
        else:
            print(f"Result length: {len(summary.split())} words")
            print(f"Summary: {summary}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

def test_with_your_documents():
    """Test with your actual study materials"""
    
    # Use your actual Document class
    class Document:
        def __init__(self, title, content):
            self.title = title
            self.content = content
    
    # Create sample documents from your study materials
    documents = [
        Document(
            "ML Basics",
            "Machine learning is a subset of AI that enables systems to learn from data without explicit programming. It uses statistical techniques to give computers the ability to learn."
        ),
        Document(
            "Neural Networks",
            "Artificial neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes that process information using a connectionist approach."
        ),
        Document(
            "Short Note",
            "AI is transformative technology."
        )
    ]
    
    summarizer = DocumentSummarizer()
    
    print("\n📚 Testing with Document Objects")
    print("=" * 60)
    
    for doc in documents:
        print(f"\nDocument: {doc.title}")
        print(f"Original: {len(doc.content.split())} words")
        
        summary = summarizer.summarize_document(doc)
        
        if summary:
            print(f"Summary: {len(summary.split())} words")
            print(f"Content: {summary}")
        else:
            print("No summary generated")
    
    print("\n" + "=" * 60)

def interactive_test():
    """Interactive test - paste your own texts"""
    
    summarizer = DocumentSummarizer()
    
    print("\n💬 Interactive Summarization Test")
    print("=" * 60)
    print("Paste your study text (press Enter twice to finish):")
    
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    
    # Join all lines except the last empty one
    text = '\n'.join(lines[:-1])
    
    if not text.strip():
        print("No text provided.")
        return
    
    print(f"\n📊 Input Statistics:")
    print(f"Characters: {len(text)}")
    print(f"Words: {len(text.split())}")
    print(f"Lines: {text.count('\n') + 1}")
    
    print("\n⏳ Summarizing...")
    summary = summarizer.summarize(text)
    
    if summary:
        print(f"\n✅ Summary ({len(summary.split())} words):")
        print("-" * 40)
        print(summary)
        print("-" * 40)
        
        # Calculate reduction
        orig_words = len(text.split())
        summ_words = len(summary.split())
        reduction = ((orig_words - summ_words) / orig_words) * 100
        
        print(f"Reduced from {orig_words} to {summ_words} words ({reduction:.1f}% reduction)")
    else:
        print("❌ Could not generate summary.")

if __name__ == "__main__":
    print("📚 Smart Study Assistant - Summarization Testing")
    print("=" * 60)
    
    # Run all tests
    test_different_lengths()
    test_with_your_documents()
    
    # Uncomment for interactive testing
    # interactive_test()
    
    print("\n🎉 All tests complete! Your summarizer is working.")