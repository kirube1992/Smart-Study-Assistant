"""
Test the basic Q&A structure.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test imports
try:
    from ssa.qa.retriever import QARetriever
    from ssa.qa.answer_extractor import AnswerExtractor
    print("✅ Successfully imported QARetriever and AnswerExtractor!")
    
    # Test class instantiation
    retriever = QARetriever(None)
    extractor = AnswerExtractor()
    print("✅ Successfully created instances!")
    
    # Test some methods
    test_text = "Machine learning is artificial intelligence. It helps computers learn."
    sentences = extractor.split_into_sentences(test_text)
    print(f"✅ Sentence splitting works: {len(sentences)} sentences found")
    
    keywords = extractor.extract_keywords(test_text, top_n=5)
    print(f"✅ Keyword extraction works: {keywords}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")