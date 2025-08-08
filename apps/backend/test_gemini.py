#!/usr/bin/env python3
"""
Simple test script to validate Gemini API integration
"""
import asyncio
import os
import sys
import logging
from pathlib import Path

# Set up logging to see debug messages
logging.basicConfig(level=logging.DEBUG)

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.agent.manager import AgentManager, EmbeddingManager
from app.core.config import settings

async def test_gemini_llm():
    """Test Gemini LLM functionality"""
    print("🧪 Testing Gemini LLM...")
    
    try:
        # Create agent manager with Gemini (using md strategy for simple text)
        agent = AgentManager(model_provider="gemini", model=settings.LL_MODEL, strategy="md")
        
        # Test a simple prompt
        result = await agent.run("Hello! Please respond with a brief greeting.")
        
        print(f"✅ LLM Test Successful!")
        print(f"📝 Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ LLM Test Failed: {e}")
        return False

async def test_gemini_embedding():
    """Test Gemini embedding functionality"""
    print("\n🧪 Testing Gemini Embeddings...")
    
    try:
        # Create embedding manager with Gemini
        embedding_manager = EmbeddingManager(
            model_provider="gemini", 
            model=settings.EMBEDDING_MODEL
        )
        
        # Test embedding generation
        embedding = await embedding_manager.embed("This is a test sentence for embedding.")
        
        print(f"✅ Embedding Test Successful!")
        print(f"📊 Embedding dimension: {len(embedding)}")
        print(f"📊 First 5 values: {embedding[:5]}")
        return True
        
    except Exception as e:
        print(f"❌ Embedding Test Failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Gemini API Integration Tests")
    print(f"🔑 API Key configured: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    print(f"🔑 API Key from env: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
    print(f"🔧 LLM Provider: {settings.LLM_PROVIDER}")
    print(f"🔧 Embedding Provider: {settings.EMBEDDING_PROVIDER}")
    print("=" * 50)
    
    # Run tests
    llm_success = await test_gemini_llm()
    embedding_success = await test_gemini_embedding()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   LLM: {'✅ PASS' if llm_success else '❌ FAIL'}")
    print(f"   Embeddings: {'✅ PASS' if embedding_success else '❌ FAIL'}")
    
    if llm_success and embedding_success:
        print("\n🎉 All tests passed! Gemini integration is working correctly.")
        return 0
    else:
        print("\n💥 Some tests failed. Please check the configuration and API key.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
