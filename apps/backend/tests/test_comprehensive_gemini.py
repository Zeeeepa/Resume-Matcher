"""
Comprehensive Test Suite for Gemini 2.5 Pro Integration
Tests all aspects of the Resume-Matcher application with Gemini 2.5 Pro
"""

import asyncio
import json
import pytest
from typing import Dict, Any
import logging

from app.agent.providers.gemini import GeminiProvider
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestGeminiComprehensive:
    """Comprehensive test suite for Gemini 2.5 Pro integration"""
    
    @pytest.fixture
    def provider(self):
        """Initialize Gemini provider"""
        return GeminiProvider()
    
    @pytest.fixture
    def sample_resume(self):
        """Sample resume for testing"""
        return """
        SARAH JOHNSON
        Senior Software Engineer
        
        CONTACT INFORMATION
        Email: sarah.johnson@email.com
        Phone: (555) 123-4567
        LinkedIn: linkedin.com/in/sarahjohnson
        GitHub: github.com/sarahjohnson
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 5+ years developing scalable web applications.
        Proficient in JavaScript, Python, and cloud technologies. Strong background in
        full-stack development and agile methodologies.
        
        TECHNICAL SKILLS
        • Languages: JavaScript (ES6+), Python, TypeScript, Java
        • Frontend: React, Vue.js, HTML5, CSS3, SASS
        • Backend: Node.js, Express, Django, Flask
        • Databases: PostgreSQL, MongoDB, Redis
        • Cloud: AWS (EC2, S3, Lambda), Docker
        • Tools: Git, Jenkins, Webpack, Jest
        
        PROFESSIONAL EXPERIENCE
        
        Senior Software Engineer | TechCorp Inc. | 2021 - Present
        • Led development of microservices architecture serving 100K+ daily users
        • Implemented CI/CD pipelines reducing deployment time by 60%
        • Mentored 3 junior developers and conducted code reviews
        • Built responsive web applications using React and Node.js
        
        Software Engineer | StartupXYZ | 2019 - 2021
        • Developed RESTful APIs handling 50K+ requests per day
        • Optimized database queries improving performance by 40%
        • Collaborated with cross-functional teams in agile environment
        • Implemented automated testing increasing code coverage to 85%
        
        Junior Developer | WebSolutions | 2018 - 2019
        • Built dynamic websites using JavaScript and PHP
        • Maintained legacy systems and performed bug fixes
        • Participated in daily standups and sprint planning
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology | 2018
        
        CERTIFICATIONS
        • AWS Certified Solutions Architect
        • Certified Scrum Master
        """
    
    @pytest.fixture
    def sample_job_description(self):
        """Sample job description for testing"""
        return """
        SENIOR FULL STACK DEVELOPER
        Company: InnovateTech Solutions
        
        POSITION OVERVIEW
        We are seeking a Senior Full Stack Developer to join our growing engineering team.
        The ideal candidate will have extensive experience with modern web technologies
        and a passion for building scalable, high-performance applications.
        
        KEY RESPONSIBILITIES
        • Design and develop full-stack web applications using React and Node.js
        • Build and maintain RESTful APIs and microservices
        • Implement responsive UI/UX designs with modern CSS frameworks
        • Work with cloud platforms (AWS, Azure) for deployment and scaling
        • Collaborate with product managers and designers in agile environment
        • Mentor junior developers and participate in code reviews
        • Optimize application performance and ensure security best practices
        
        REQUIRED QUALIFICATIONS
        • 5+ years of experience in full-stack development
        • Expert-level proficiency in JavaScript/TypeScript and React
        • Strong backend development skills with Node.js or Python
        • Experience with PostgreSQL and database design
        • Proficiency with AWS cloud services (EC2, S3, Lambda, RDS)
        • Experience with containerization (Docker, Kubernetes)
        • Knowledge of CI/CD pipelines and DevOps practices
        • Strong understanding of software architecture patterns
        • Experience with version control (Git) and agile methodologies
        
        PREFERRED QUALIFICATIONS
        • Experience with GraphQL and Apollo
        • Knowledge of machine learning frameworks
        • Familiarity with serverless architecture
        • Experience with monitoring tools (DataDog, New Relic)
        • Contributions to open-source projects
        
        WHAT WE OFFER
        • Competitive salary and equity package
        • Comprehensive health benefits
        • Flexible work arrangements
        • Professional development opportunities
        • Cutting-edge technology stack
        """
    
    async def test_basic_llm_functionality(self, provider):
        """Test basic LLM functionality"""
        logger.info("🧪 Testing basic LLM functionality...")
        
        prompt = "Hello! Please respond with 'Gemini 2.5 Pro is working correctly.'"
        response = await provider(prompt)
        
        assert response is not None
        assert len(response) > 0
        assert "gemini" in response.lower() or "working" in response.lower()
        
        logger.info(f"✅ Basic LLM test passed. Response: {response[:100]}...")
    
    async def test_embedding_functionality(self, provider):
        """Test embedding functionality"""
        logger.info("🧪 Testing embedding functionality...")
        
        from app.agent.providers.gemini import GeminiEmbeddingProvider
        
        embedding_provider = GeminiEmbeddingProvider()
        text = "This is a test sentence for embedding generation."
        embeddings = await embedding_provider.embed(text)
        
        assert embeddings is not None
        assert len(embeddings) == 768  # text-embedding-004 dimension
        assert all(isinstance(x, (int, float)) for x in embeddings)
        
        logger.info(f"✅ Embedding test passed. Dimension: {len(embeddings)}")
    
    async def test_resume_analysis(self, provider, sample_resume, sample_job_description):
        """Test comprehensive resume analysis"""
        logger.info("🧪 Testing resume analysis functionality...")
        
        prompt = f"""
        Analyze this resume against the job description and provide a comprehensive assessment.
        
        RESUME:
        {sample_resume}
        
        JOB DESCRIPTION:
        {sample_job_description}
        
        Please provide a detailed analysis including:
        1. Overall match percentage (0-100%)
        2. Key strengths that align with the job
        3. Areas for improvement
        4. Missing skills or experience
        5. Specific recommendations for enhancement
        
        Format your response as structured text with clear sections.
        """
        
        response = await provider(prompt)
        
        assert response is not None
        assert len(response) > 500  # Expect detailed response
        
        # Check for key analysis components
        response_lower = response.lower()
        assert any(word in response_lower for word in ["match", "percentage", "score"])
        assert any(word in response_lower for word in ["strength", "align", "experience"])
        assert any(word in response_lower for word in ["improvement", "recommendation", "enhance"])
        
        logger.info("✅ Resume analysis test passed")
        logger.info(f"📝 Analysis preview: {response[:200]}...")
    
    async def test_keyword_extraction(self, provider, sample_job_description):
        """Test keyword extraction from job descriptions"""
        logger.info("🧪 Testing keyword extraction...")
        
        prompt = f"""
        Extract the most important keywords and skills from this job description.
        Focus on technical skills, tools, and qualifications.
        
        JOB DESCRIPTION:
        {sample_job_description}
        
        Return the keywords as a comma-separated list, prioritized by importance.
        """
        
        response = await provider(prompt)
        
        assert response is not None
        assert len(response) > 50
        
        # Check for expected technical keywords
        response_lower = response.lower()
        expected_keywords = ["javascript", "react", "node.js", "aws", "docker", "postgresql"]
        found_keywords = sum(1 for keyword in expected_keywords if keyword in response_lower)
        
        assert found_keywords >= 4, f"Expected at least 4 keywords, found {found_keywords}"
        
        logger.info("✅ Keyword extraction test passed")
        logger.info(f"📝 Keywords preview: {response[:150]}...")
    
    async def test_resume_improvement_suggestions(self, provider, sample_resume, sample_job_description):
        """Test resume improvement suggestions"""
        logger.info("🧪 Testing resume improvement suggestions...")
        
        prompt = f"""
        Provide specific, actionable suggestions to improve this resume for the given job.
        
        RESUME:
        {sample_resume}
        
        JOB DESCRIPTION:
        {sample_job_description}
        
        Please provide:
        1. 5 specific improvements to make
        2. Keywords to add or emphasize
        3. Experience descriptions to enhance
        4. Skills to highlight or add
        5. Overall formatting suggestions
        
        Be specific and actionable in your recommendations.
        """
        
        response = await provider(prompt)
        
        assert response is not None
        assert len(response) > 300
        
        # Check for improvement-related content
        response_lower = response.lower()
        improvement_indicators = ["improve", "add", "enhance", "highlight", "emphasize", "include"]
        found_indicators = sum(1 for indicator in improvement_indicators if indicator in response_lower)
        
        assert found_indicators >= 3, f"Expected improvement suggestions, found {found_indicators} indicators"
        
        logger.info("✅ Resume improvement test passed")
        logger.info(f"📝 Suggestions preview: {response[:200]}...")
    
    async def test_ats_optimization(self, provider, sample_resume, sample_job_description):
        """Test ATS (Applicant Tracking System) optimization suggestions"""
        logger.info("🧪 Testing ATS optimization...")
        
        prompt = f"""
        Analyze this resume for ATS (Applicant Tracking System) optimization against the job description.
        
        RESUME:
        {sample_resume}
        
        JOB DESCRIPTION:
        {sample_job_description}
        
        Provide specific ATS optimization recommendations:
        1. Keyword density analysis
        2. Section formatting suggestions
        3. Skills matching assessment
        4. Experience alignment recommendations
        5. Overall ATS compatibility score (1-10)
        
        Focus on making the resume more likely to pass ATS screening.
        """
        
        response = await provider(prompt)
        
        assert response is not None
        assert len(response) > 200
        
        # Check for ATS-related content
        response_lower = response.lower()
        ats_indicators = ["ats", "keyword", "format", "section", "compatibility", "screening"]
        found_indicators = sum(1 for indicator in ats_indicators if indicator in response_lower)
        
        assert found_indicators >= 3, f"Expected ATS optimization content, found {found_indicators} indicators"
        
        logger.info("✅ ATS optimization test passed")
        logger.info(f"📝 ATS analysis preview: {response[:200]}...")
    
    async def test_multiple_job_comparison(self, provider, sample_resume):
        """Test comparing resume against multiple job descriptions"""
        logger.info("🧪 Testing multiple job comparison...")
        
        job1 = "Frontend Developer position requiring React, JavaScript, CSS, and UI/UX design skills."
        job2 = "Backend Developer position requiring Python, Django, PostgreSQL, and API development."
        job3 = "DevOps Engineer position requiring AWS, Docker, Kubernetes, and CI/CD pipeline experience."
        
        prompt = f"""
        Compare this resume against three different job positions and rank them by fit.
        
        RESUME:
        {sample_resume}
        
        JOB 1 - Frontend Developer:
        {job1}
        
        JOB 2 - Backend Developer:
        {job2}
        
        JOB 3 - DevOps Engineer:
        {job3}
        
        Provide:
        1. Ranking of jobs by best fit (1st, 2nd, 3rd)
        2. Match percentage for each position
        3. Key reasons for each ranking
        4. Specific improvements needed for each role
        """
        
        response = await provider(prompt)
        
        assert response is not None
        assert len(response) > 400
        
        # Check for comparison content
        response_lower = response.lower()
        comparison_indicators = ["rank", "match", "percentage", "fit", "comparison", "best"]
        found_indicators = sum(1 for indicator in comparison_indicators if indicator in response_lower)
        
        assert found_indicators >= 3, f"Expected comparison content, found {found_indicators} indicators"
        
        logger.info("✅ Multiple job comparison test passed")
        logger.info(f"📝 Comparison preview: {response[:200]}...")
    
    async def test_performance_and_reliability(self, provider):
        """Test performance and reliability of the Gemini integration"""
        logger.info("🧪 Testing performance and reliability...")
        
        # Test multiple concurrent requests
        prompts = [
            "Analyze the importance of soft skills in software engineering.",
            "Explain the benefits of microservices architecture.",
            "Describe best practices for API design.",
            "What are the key principles of clean code?",
            "How do you optimize database performance?"
        ]
        
        start_time = asyncio.get_event_loop().time()
        
        # Run concurrent requests
        tasks = [provider(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)
        
        end_time = asyncio.get_event_loop().time()
        total_time = end_time - start_time
        
        # Validate all responses
        assert len(responses) == len(prompts)
        assert all(response is not None and len(response) > 50 for response in responses)
        
        # Performance check (should complete within reasonable time)
        assert total_time < 60, f"Concurrent requests took too long: {total_time:.2f}s"
        
        logger.info(f"✅ Performance test passed. {len(prompts)} concurrent requests in {total_time:.2f}s")
    
    async def test_error_handling(self, provider):
        """Test error handling for various edge cases"""
        logger.info("🧪 Testing error handling...")
        
        # Test empty prompt
        try:
            response = await provider("")
            # Should either handle gracefully or raise appropriate error
            assert response is not None
        except Exception as e:
            logger.info(f"Empty prompt handled with exception: {type(e).__name__}")
        
        # Test very long prompt
        long_prompt = "Analyze this resume: " + "x" * 10000
        try:
            response = await provider(long_prompt)
            assert response is not None
        except Exception as e:
            logger.info(f"Long prompt handled with exception: {type(e).__name__}")
        
        logger.info("✅ Error handling test passed")


async def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🚀 Starting Comprehensive Gemini 2.5 Pro Test Suite")
    print(f"🔧 Model: {settings.LL_MODEL}")
    print(f"🔑 API Key configured: {bool(settings.GEMINI_API_KEY)}")
    print("=" * 60)
    
    test_suite = TestGeminiComprehensive()
    provider = GeminiProvider()
    
    # Sample data
    sample_resume = """
    SARAH JOHNSON
    Senior Software Engineer
    
    CONTACT INFORMATION
    Email: sarah.johnson@email.com
    Phone: (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5+ years developing scalable web applications.
    Proficient in JavaScript, Python, and cloud technologies.
    
    TECHNICAL SKILLS
    • Languages: JavaScript (ES6+), Python, TypeScript
    • Frontend: React, Vue.js, HTML5, CSS3
    • Backend: Node.js, Express, Django
    • Databases: PostgreSQL, MongoDB
    • Cloud: AWS (EC2, S3, Lambda), Docker
    
    PROFESSIONAL EXPERIENCE
    Senior Software Engineer | TechCorp Inc. | 2021 - Present
    • Led development of microservices architecture serving 100K+ daily users
    • Implemented CI/CD pipelines reducing deployment time by 60%
    • Built responsive web applications using React and Node.js
    """
    
    sample_job_description = """
    SENIOR FULL STACK DEVELOPER
    
    REQUIRED QUALIFICATIONS
    • 5+ years of experience in full-stack development
    • Expert-level proficiency in JavaScript/TypeScript and React
    • Strong backend development skills with Node.js or Python
    • Experience with PostgreSQL and database design
    • Proficiency with AWS cloud services
    • Experience with containerization (Docker, Kubernetes)
    • Knowledge of CI/CD pipelines and DevOps practices
    """
    
    tests = [
        ("Basic LLM Functionality", test_suite.test_basic_llm_functionality(provider)),
        ("Embedding Functionality", test_suite.test_embedding_functionality(provider)),
        ("Resume Analysis", test_suite.test_resume_analysis(provider, sample_resume, sample_job_description)),
        ("Keyword Extraction", test_suite.test_keyword_extraction(provider, sample_job_description)),
        ("Resume Improvement", test_suite.test_resume_improvement_suggestions(provider, sample_resume, sample_job_description)),
        ("ATS Optimization", test_suite.test_ats_optimization(provider, sample_resume, sample_job_description)),
        ("Multiple Job Comparison", test_suite.test_multiple_job_comparison(provider, sample_resume)),
        ("Performance & Reliability", test_suite.test_performance_and_reliability(provider)),
        ("Error Handling", test_suite.test_error_handling(provider)),
    ]
    
    results = []
    
    for test_name, test_coro in tests:
        try:
            print(f"\n🧪 Running: {test_name}")
            await test_coro
            results.append((test_name, "✅ PASSED"))
            print(f"✅ {test_name} - PASSED")
        except Exception as e:
            results.append((test_name, f"❌ FAILED: {str(e)}"))
            print(f"❌ {test_name} - FAILED: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if "PASSED" in result)
    total = len(results)
    
    for test_name, result in results:
        print(f"{result} {test_name}")
    
    print(f"\n🎯 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Gemini 2.5 Pro integration is fully functional!")
    else:
        print(f"⚠️  {total - passed} tests failed. Please review the failures above.")
    
    return passed == total


if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())
