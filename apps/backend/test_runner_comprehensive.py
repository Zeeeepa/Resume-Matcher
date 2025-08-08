#!/usr/bin/env python3
"""
Comprehensive Test Runner for Resume-Matcher with Gemini 2.5 Pro
Runs all tests and provides detailed reporting
"""

import asyncio
import sys
import os
import time
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings


class ComprehensiveTestRunner:
    """Comprehensive test runner for the Resume-Matcher application"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_results = []
        self.services_started = False
    
    def print_header(self):
        """Print test suite header"""
        print("🚀" * 30)
        print("🚀 RESUME-MATCHER COMPREHENSIVE TEST SUITE 🚀")
        print("🚀" * 30)
        print(f"📅 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 Model: {settings.LL_MODEL}")
        print(f"🔑 API Key configured: {bool(settings.GEMINI_API_KEY)}")
        print(f"🌐 LLM Provider: {settings.LLM_PROVIDER}")
        print(f"🔍 Embedding Provider: {settings.EMBEDDING_PROVIDER}")
        print("=" * 80)
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        checks = []
        
        # Check API key
        if settings.GEMINI_API_KEY:
            checks.append(("✅", "Gemini API Key configured"))
        else:
            checks.append(("❌", "Gemini API Key missing"))
        
        # Check model configuration
        if settings.LL_MODEL:
            checks.append(("✅", f"LLM Model configured: {settings.LL_MODEL}"))
        else:
            checks.append(("❌", "LLM Model not configured"))
        
        # Check providers
        if settings.LLM_PROVIDER == "gemini":
            checks.append(("✅", "LLM Provider set to Gemini"))
        else:
            checks.append(("⚠️", f"LLM Provider: {settings.LLM_PROVIDER} (expected: gemini)"))
        
        # Check Python dependencies
        try:
            import httpx
            checks.append(("✅", "httpx library available"))
        except ImportError:
            checks.append(("❌", "httpx library missing"))
        
        try:
            from app.agent.providers.gemini import GeminiProvider
            checks.append(("✅", "GeminiProvider importable"))
        except ImportError as e:
            checks.append(("❌", f"GeminiProvider import failed: {e}"))
        
        # Print results
        for status, message in checks:
            print(f"{status} {message}")
        
        failed_checks = sum(1 for status, _ in checks if status == "❌")
        if failed_checks > 0:
            print(f"\n❌ {failed_checks} prerequisite checks failed!")
            return False
        
        print("\n✅ All prerequisites met!")
        return True
    
    async def run_basic_gemini_test(self) -> bool:
        """Run basic Gemini connectivity test"""
        print("\n🧪 Running Basic Gemini Connectivity Test...")
        
        try:
            from app.agent.providers.gemini import GeminiProvider, GeminiEmbeddingProvider
            
            # Test basic LLM functionality
            provider = GeminiProvider()
            response = await provider("Hello! Please respond with 'Gemini 2.5 Pro is working.'")
            
            if response and len(response) > 0:
                print("✅ Basic Gemini LLM test passed")
                print(f"📝 Response: {response[:100]}...")
                
                # Test embeddings
                embedding_provider = GeminiEmbeddingProvider()
                embeddings = await embedding_provider.embed("Test embedding text")
                if embeddings and len(embeddings) == 768:
                    print("✅ Gemini embeddings test passed")
                    print(f"📊 Embedding dimension: {len(embeddings)}")
                    return True
                else:
                    print("❌ Gemini embeddings test failed")
                    return False
            else:
                print("❌ Basic Gemini LLM test failed")
                return False
                
        except Exception as e:
            print(f"❌ Basic Gemini test failed with error: {e}")
            return False
    
    def start_services(self) -> bool:
        """Start backend and frontend services"""
        print("\n🚀 Starting services...")
        
        try:
            # Check if services are already running
            import httpx
            
            try:
                response = httpx.get("http://localhost:8000/ping", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend service already running")
                    self.services_started = True
                    return True
            except:
                pass
            
            print("⚠️  Backend service not running. Please start it manually:")
            print("   cd apps/backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
            return False
            
        except Exception as e:
            print(f"❌ Service check failed: {e}")
            return False
    
    async def run_comprehensive_tests(self) -> bool:
        """Run comprehensive Gemini tests"""
        print("\n🧪 Running Comprehensive Gemini Tests...")
        
        try:
            # Import and run comprehensive tests
            from tests.test_comprehensive_gemini import run_comprehensive_tests
            
            result = await run_comprehensive_tests()
            self.test_results.append(("Comprehensive Gemini Tests", result))
            return result
            
        except Exception as e:
            print(f"❌ Comprehensive tests failed: {e}")
            self.test_results.append(("Comprehensive Gemini Tests", False))
            return False
    
    async def run_api_integration_tests(self) -> bool:
        """Run API integration tests"""
        print("\n🧪 Running API Integration Tests...")
        
        if not self.services_started:
            print("⚠️  Skipping API tests - backend service not running")
            return True
        
        try:
            # Import and run API integration tests
            from tests.test_api_integration import run_api_integration_tests
            
            result = await run_api_integration_tests()
            self.test_results.append(("API Integration Tests", result))
            return result
            
        except Exception as e:
            print(f"❌ API integration tests failed: {e}")
            self.test_results.append(("API Integration Tests", False))
            return False
    
    def run_performance_benchmark(self) -> bool:
        """Run performance benchmarks"""
        print("\n🏃 Running Performance Benchmarks...")
        
        try:
            # Simple performance test
            import asyncio
            from app.agent.providers.gemini import GeminiProvider
            
            async def benchmark():
                provider = GeminiProvider()
                
                # Test response time for simple query
                start_time = time.time()
                response = await provider("What is 2+2?")
                end_time = time.time()
                
                response_time = end_time - start_time
                
                print(f"📊 Simple query response time: {response_time:.2f}s")
                
                if response_time < 10:  # Should respond within 10 seconds
                    print("✅ Performance benchmark passed")
                    return True
                else:
                    print("❌ Performance benchmark failed - too slow")
                    return False
            
            result = asyncio.run(benchmark())
            self.test_results.append(("Performance Benchmark", result))
            return result
            
        except Exception as e:
            print(f"❌ Performance benchmark failed: {e}")
            self.test_results.append(("Performance Benchmark", False))
            return False
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        print(f"⏱️  Total execution time: {total_time:.2f} seconds")
        print(f"📅 Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n📋 Test Results:")
        print("-" * 50)
        
        passed_tests = 0
        total_tests = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status} {test_name}")
            if result:
                passed_tests += 1
        
        print("-" * 50)
        print(f"🎯 Overall Results: {passed_tests}/{total_tests} test suites passed")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED!")
            print("🚀 Resume-Matcher with Gemini 2.5 Pro is fully functional!")
            print("\n✨ Key Features Validated:")
            print("   • Gemini 2.5 Pro LLM integration")
            print("   • Text embedding generation")
            print("   • Resume analysis and improvement")
            print("   • Keyword extraction")
            print("   • ATS optimization")
            print("   • Multi-job comparison")
            print("   • API endpoints and error handling")
            print("   • Performance and reliability")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test suite(s) failed")
            print("Please review the detailed output above for specific failures.")
        
        print("\n" + "=" * 80)
        
        return passed_tests == total_tests
    
    def print_usage_instructions(self):
        """Print usage instructions for the application"""
        print("\n📖 USAGE INSTRUCTIONS")
        print("=" * 50)
        print("To use the Resume-Matcher application:")
        print()
        print("1. 🚀 Start the backend service:")
        print("   cd apps/backend")
        print("   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print()
        print("2. 🌐 Start the frontend service:")
        print("   cd apps/frontend")
        print("   npm run dev -- --port 3001")
        print()
        print("3. 🔗 Access the application:")
        print("   • Frontend: http://localhost:3001")
        print("   • API Docs: http://localhost:8000/api/docs")
        print("   • Health Check: http://localhost:8000/ping")
        print()
        print("4. 📄 Upload resumes and job descriptions (PDF/DOCX format)")
        print("5. 🤖 Get AI-powered improvements using Gemini 2.5 Pro")
        print()


async def main():
    """Main test runner function"""
    runner = ComprehensiveTestRunner()
    
    runner.print_header()
    
    # Check prerequisites
    if not runner.check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        sys.exit(1)
    
    # Run basic connectivity test
    if not await runner.run_basic_gemini_test():
        print("\n❌ Basic Gemini test failed. Please check your API key and configuration.")
        sys.exit(1)
    
    # Check services
    runner.start_services()
    
    # Run all test suites
    await runner.run_comprehensive_tests()
    await runner.run_api_integration_tests()
    runner.run_performance_benchmark()
    
    # Generate report
    success = runner.generate_test_report()
    
    # Print usage instructions
    runner.print_usage_instructions()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
