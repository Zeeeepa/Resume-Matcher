# Resume-Matcher Testing Suite

Comprehensive testing suite for Resume-Matcher application with Gemini 2.5 Pro integration.

## Overview

This testing suite validates all aspects of the Resume-Matcher application, including:

- ✅ Gemini 2.5 Pro LLM integration
- ✅ Text embedding generation
- ✅ Resume analysis and improvement
- ✅ Keyword extraction and ATS optimization
- ✅ API endpoints and error handling
- ✅ Performance and reliability testing
- ✅ End-to-end workflow validation

## Test Files

### Core Test Suites

1. **`test_comprehensive_gemini.py`** - Comprehensive Gemini 2.5 Pro functionality tests
   - Basic LLM functionality
   - Embedding generation
   - Resume analysis
   - Keyword extraction
   - Resume improvement suggestions
   - ATS optimization
   - Multiple job comparison
   - Performance and reliability
   - Error handling

2. **`test_api_integration.py`** - API integration tests
   - Health check endpoints
   - API documentation validation
   - File upload validation
   - Resume improvement workflows
   - Error handling
   - Performance testing

### Test Runners

3. **`test_runner_comprehensive.py`** - Main test runner
   - Prerequisites checking
   - Service management
   - Comprehensive test execution
   - Detailed reporting
   - Usage instructions

### Utilities

4. **`create_test_files.py`** - Test file generator
   - Sample resume creation
   - Sample job description creation
   - HTML and text format generation
   - PDF generation (if libraries available)

## Quick Start

### 1. Run Basic Tests

```bash
# Navigate to backend directory
cd apps/backend

# Run comprehensive test suite
uv run python test_runner_comprehensive.py
```

### 2. Run Individual Test Suites

```bash
# Run Gemini functionality tests
uv run python -m pytest tests/test_comprehensive_gemini.py -v

# Run API integration tests (requires running backend)
uv run python -m pytest tests/test_api_integration.py -v
```

### 3. Create Test Files

```bash
# Generate sample files for testing
uv run python create_test_files.py
```

## Prerequisites

### Required Configuration

Ensure your `.env` file contains:

```env
GEMINI_API_KEY=your_api_key_here
LL_MODEL=gemini-2.5-pro-preview-06-05
EMBEDDING_MODEL=text-embedding-004
LLM_PROVIDER=gemini
EMBEDDING_PROVIDER=gemini
```

### Required Dependencies

```bash
# Install test dependencies
uv add httpx pytest pytest-asyncio
```

### Optional Dependencies (for PDF generation)

```bash
# For PDF test file generation
uv add weasyprint
# OR
uv add pdfkit
```

## Test Categories

### 1. Basic Functionality Tests

- **LLM Connectivity**: Validates basic Gemini 2.5 Pro communication
- **Embedding Generation**: Tests text-embedding-004 functionality
- **Configuration Validation**: Checks all required settings

### 2. Resume Analysis Tests

- **Resume Parsing**: Validates resume content extraction
- **Job Matching**: Tests resume-job description alignment
- **Gap Analysis**: Identifies missing skills and experience
- **Improvement Suggestions**: Generates actionable recommendations

### 3. Advanced Features Tests

- **Keyword Extraction**: Extracts relevant keywords from job descriptions
- **ATS Optimization**: Provides ATS-friendly formatting suggestions
- **Multi-Job Comparison**: Compares resume against multiple positions
- **Performance Optimization**: Tests response times and reliability

### 4. API Integration Tests

- **Endpoint Validation**: Tests all API endpoints
- **File Upload**: Validates PDF/DOCX upload functionality
- **Error Handling**: Tests various error scenarios
- **Documentation**: Validates OpenAPI specification

### 5. Performance Tests

- **Response Time**: Measures API response times
- **Concurrent Requests**: Tests multiple simultaneous requests
- **Load Testing**: Validates performance under load
- **Memory Usage**: Monitors resource consumption

## Expected Test Results

### Successful Test Run

```
🚀 RESUME-MATCHER COMPREHENSIVE TEST SUITE 🚀
================================================================
📅 Started at: 2024-08-08 12:00:00
🔧 Model: gemini-2.5-pro-preview-06-05
🔑 API Key configured: True
🌐 LLM Provider: gemini
🔍 Embedding Provider: gemini

🔍 Checking prerequisites...
✅ Gemini API Key configured
✅ LLM Model configured: gemini-2.5-pro-preview-06-05
✅ LLM Provider set to Gemini
✅ httpx library available
✅ GeminiProvider importable

🧪 Running Basic Gemini Connectivity Test...
✅ Basic Gemini LLM test passed
✅ Gemini embeddings test passed

🧪 Running Comprehensive Gemini Tests...
✅ Basic LLM Functionality - PASSED
✅ Embedding Functionality - PASSED
✅ Resume Analysis - PASSED
✅ Keyword Extraction - PASSED
✅ Resume Improvement - PASSED
✅ ATS Optimization - PASSED
✅ Multiple Job Comparison - PASSED
✅ Performance & Reliability - PASSED
✅ Error Handling - PASSED

📊 Overall Results: 9/9 test suites passed
🎉 ALL TESTS PASSED!
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   ```
   ❌ Gemini API Key missing
   ```
   **Solution**: Set `GEMINI_API_KEY` in your `.env` file

2. **Import Errors**
   ```
   ❌ GeminiProvider import failed
   ```
   **Solution**: Ensure you're in the correct directory and dependencies are installed

3. **Service Not Running**
   ```
   ⚠️ Backend service not running
   ```
   **Solution**: Start the backend service:
   ```bash
   cd apps/backend
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Timeout Errors**
   ```
   ❌ Request timeout
   ```
   **Solution**: Check internet connection and API key validity

### Debug Mode

Run tests with verbose output:

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose pytest output
uv run python -m pytest tests/ -v -s
```

## Test Data

### Sample Resume Content

The test suite uses realistic resume data including:
- Professional summary
- Technical skills (JavaScript, React, Node.js, Python, AWS, etc.)
- Work experience with quantified achievements
- Education and certifications
- Notable projects

### Sample Job Descriptions

Test job descriptions include:
- Senior Full Stack Developer positions
- Frontend Developer roles
- Backend Developer positions
- DevOps Engineer roles

All with realistic requirements, preferred qualifications, and company information.

## Continuous Integration

### GitHub Actions Integration

```yaml
name: Resume-Matcher Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd apps/backend
          pip install uv
          uv sync
      - name: Run tests
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          cd apps/backend
          uv run python test_runner_comprehensive.py
```

## Contributing

### Adding New Tests

1. Create test files in the `tests/` directory
2. Follow the existing naming convention: `test_*.py`
3. Use async/await for API calls
4. Include comprehensive assertions
5. Add proper error handling
6. Update this README with new test descriptions

### Test Guidelines

- **Descriptive Names**: Use clear, descriptive test function names
- **Comprehensive Coverage**: Test both success and failure scenarios
- **Performance Aware**: Include timing assertions for critical operations
- **Documentation**: Add docstrings explaining test purpose
- **Isolation**: Ensure tests don't depend on each other

## Support

For issues with the testing suite:

1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review the detailed test output for specific error messages
4. Ensure the Gemini API key is valid and has sufficient quota

## License

This testing suite is part of the Resume-Matcher project and follows the same license terms.

