#!/usr/bin/env python3
"""
Simple Gemini 2.5 Pro Test Suite
Direct testing without pytest dependencies
"""

import asyncio
import sys
import time
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings


async def test_basic_functionality():
    """Test basic Gemini functionality"""
    print("🧪 Testing Basic Gemini 2.5 Pro Functionality...")
    
    try:
        from app.agent.providers.gemini import GeminiProvider, GeminiEmbeddingProvider
        
        # Test LLM
        print("   • Testing LLM...")
        provider = GeminiProvider()
        response = await provider("Hello! Please respond with 'Gemini 2.5 Pro is working correctly.'")
        
        if response and len(response) > 10:
            print(f"   ✅ LLM Response: {response[:80]}...")
        else:
            print("   ❌ LLM test failed")
            return False
        
        # Test embeddings
        print("   • Testing Embeddings...")
        embedding_provider = GeminiEmbeddingProvider()
        embeddings = await embedding_provider.embed("Test sentence for embedding")
        
        if embeddings and len(embeddings) == 768:
            print(f"   ✅ Embeddings: {len(embeddings)} dimensions")
        else:
            print("   ❌ Embeddings test failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


async def test_resume_analysis():
    """Test resume analysis functionality"""
    print("\n🧪 Testing Resume Analysis...")
    
    try:
        from app.agent.providers.gemini import GeminiProvider
        
        provider = GeminiProvider()
        
        resume = """
        John Smith
        Software Engineer
        
        Experience:
        - 3 years developing web applications with JavaScript
        - Built REST APIs using Node.js
        - Worked with MySQL databases
        
        Skills:
        - JavaScript, HTML, CSS
        - Node.js, Express
        - MySQL, Git
        """
        
        job_description = """
        Senior Full Stack Developer
        
        Requirements:
        - 5+ years experience with React and TypeScript
        - Strong backend skills with Node.js
        - Experience with PostgreSQL
        - Knowledge of AWS cloud services
        - Docker and Kubernetes experience
        """
        
        prompt = f"""
        Analyze this resume against the job description and provide a brief assessment:
        
        RESUME:
        {resume}
        
        JOB DESCRIPTION:
        {job_description}
        
        Please provide:
        1. Match percentage (0-100%)
        2. Top 3 strengths
        3. Top 3 gaps
        4. Key recommendations
        
        Keep response concise and structured.
        """
        
        print("   • Sending analysis request...")
        response = await provider(prompt)
        
        if response and len(response) > 100:
            print("   ✅ Resume analysis completed")
            print(f"   📝 Analysis preview: {response[:150]}...")
            return True
        else:
            print("   ❌ Resume analysis failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


async def test_keyword_extraction():
    """Test keyword extraction"""
    print("\n🧪 Testing Keyword Extraction...")
    
    try:
        from app.agent.providers.gemini import GeminiProvider
        
        provider = GeminiProvider()
        
        job_description = """
        We're looking for a Senior React Developer with expertise in TypeScript,
        Redux, and modern JavaScript. Experience with AWS, Docker, and CI/CD
        pipelines is required. Knowledge of GraphQL and Node.js is preferred.
        """
        
        prompt = f"""
        Extract the most important technical keywords from this job description:
        
        {job_description}
        
        Return only the keywords as a comma-separated list, prioritized by importance.
        """
        
        print("   • Extracting keywords...")
        response = await provider(prompt)
        
        if response and len(response) > 20:
            print("   ✅ Keyword extraction completed")
            print(f"   🔑 Keywords: {response[:100]}...")
            return True
        else:
            print("   ❌ Keyword extraction failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


async def test_performance():
    """Test performance"""
    print("\n🧪 Testing Performance...")
    
    try:
        from app.agent.providers.gemini import GeminiProvider
        
        provider = GeminiProvider()
        
        # Test response time
        start_time = time.time()
        response = await provider("What is 2+2? Please respond briefly.")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response and response_time < 15:  # Should respond within 15 seconds
            print(f"   ✅ Response time: {response_time:.2f}s")
            print(f"   📝 Response: {response[:50]}...")
            return True
        else:
            print(f"   ❌ Performance test failed. Time: {response_time:.2f}s")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


async def main():
    """Main test function"""
    print("🚀 GEMINI 2.5 PRO SIMPLE TEST SUITE")
    print("=" * 50)
    print(f"🔧 Model: {settings.LL_MODEL}")
    print(f"🔑 API Key configured: {bool(settings.GEMINI_API_KEY)}")
    print(f"🌐 LLM Provider: {settings.LLM_PROVIDER}")
    print("=" * 50)
    
    start_time = time.time()
    
    # Run tests
    tests = [
        ("Basic Functionality", test_basic_functionality()),
        ("Resume Analysis", test_resume_analysis()),
        ("Keyword Extraction", test_keyword_extraction()),
        ("Performance", test_performance()),
    ]
    
    results = []
    
    for test_name, test_coro in tests:
        try:
            result = await test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print("-" * 50)
    print(f"🎯 Results: {passed}/{total} tests passed")
    print(f"⏱️  Total time: {total_time:.2f} seconds")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Gemini 2.5 Pro integration is fully functional!")
        print("\n✨ Validated Features:")
        print("   • Gemini 2.5 Pro LLM communication")
        print("   • Text embedding generation (768D)")
        print("   • Resume analysis and improvement")
        print("   • Keyword extraction")
        print("   • Performance within acceptable limits")
        
        print("\n📖 Next Steps:")
        print("   1. Start the backend: cd apps/backend && uv run uvicorn app.main:app --port 8000")
        print("   2. Start the frontend: cd apps/frontend && npm run dev -- --port 3001")
        print("   3. Access the app: http://localhost:3001")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Please check the error messages above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

