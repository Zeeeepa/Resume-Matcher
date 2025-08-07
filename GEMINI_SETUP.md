# 🚀 Resume Matcher with Gemini API - Quick Setup Guide

This guide will help you set up and run Resume Matcher with Google's Gemini API in just a few simple steps.

## 🔑 Prerequisites

1. **Get a Gemini API Key** (Free!)
   - Visit: https://aistudio.google.com/
   - Sign in with your Google account
   - Click "Get API key" → "Create API key"
   - Copy your API key (starts with `AIza...`)

2. **System Requirements**
   - **Node.js** 18+ (https://nodejs.org/)
   - **Python** 3.8+ (https://python.org/downloads/)
   - **Git** (to clone the repository)

## ⚡ Quick Start (Recommended)

### Option 1: One-Command Setup

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/Resume-Matcher.git
cd Resume-Matcher

# Run the setup script (will prompt for API key)
./run_with_gemini.sh
```

### Option 2: Provide API Key Directly

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/Resume-Matcher.git
cd Resume-Matcher

# Run with your API key
./run_with_gemini.sh AIzaSyBXmhlHudrD4zXiv-5fjxi1gGG-_kdtaZ0
```

## 🛠️ Manual Setup (Step by Step)

If you prefer to run commands manually:

### 1. Clone and Navigate
```bash
git clone https://github.com/Zeeeepa/Resume-Matcher.git
cd Resume-Matcher
```

### 2. Install Dependencies
```bash
# Install Node.js dependencies
npm install

# Install frontend dependencies
cd apps/frontend && npm install && cd ../..

# Install Python dependencies
cd apps/backend
uv venv
uv pip install -r requirements.txt
cd ../..
```

### 3. Configure Environment
```bash
# Create backend environment file
cat > apps/backend/.env << EOF
SESSION_SECRET_KEY="your-secret-key-here"
SYNC_DATABASE_URL="sqlite:///./app.db"
ASYNC_DATABASE_URL="sqlite+aiosqlite:///./app.db"
PYTHONDONTWRITEBYTECODE=1

# Gemini API Configuration
LLM_PROVIDER="gemini"
EMBEDDING_PROVIDER="gemini"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
LL_MODEL="gemini-1.5-flash"
EMBEDDING_MODEL="models/text-embedding-004"
EOF
```

### 4. Test Integration
```bash
cd apps/backend
uv run python test_gemini.py
cd ../..
```

### 5. Start the Application
```bash
# Start both frontend and backend
npm run dev
```

## 🌐 Access the Application

Once running, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Testing Your Setup

The setup script automatically runs integration tests, but you can manually test:

```bash
cd apps/backend
uv run python test_gemini.py
```

Expected output:
```
🚀 Starting Gemini API Integration Tests
🔑 API Key configured: Yes
⚙️ LLM Provider: gemini
⚙️ Embedding Provider: gemini
==================================================
🧪 Testing Gemini LLM...
✅ LLM Test Successful!
📝 Response: ```md
Hello there!
```

🧪 Testing Gemini Embeddings...
✅ Embedding Test Successful!
📊 Embedding dimension: 768
📊 First 5 values: [0.0050402274, 0.018947808, -0.06460995, 0.012052573, 0.039129917]

==================================================
📊 Test Results:
   LLM: ✅ PASS
   Embeddings: ✅ PASS

🎉 All tests passed! Gemini integration is working correctly.
```

## 🔧 Available Commands

After setup, you can use these commands:

```bash
# Start both frontend and backend
npm run dev

# Start only backend
npm run dev:backend

# Start only frontend  
npm run dev:frontend

# Build for production
npm run build

# Run tests
cd apps/backend && uv run python test_gemini.py
```

## 🚨 Troubleshooting

### Common Issues

1. **"Command not found: uv"**
   - The script will auto-install `uv`, or install manually: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **"API key format looks unusual"**
   - Ensure your API key starts with `AIza` and is 39 characters long
   - Get a new key from https://aistudio.google.com/

3. **"Node.js version too old"**
   - Install Node.js 18+ from https://nodejs.org/

4. **"Python version too old"**
   - Install Python 3.8+ from https://python.org/downloads/

5. **Port already in use**
   - Kill existing processes: `pkill -f "node\|python\|uvicorn"`
   - Or use different ports in the configuration

### Getting Help

- **Discord**: https://dsc.gg/resume-matcher
- **GitHub Issues**: https://github.com/Zeeeepa/Resume-Matcher/issues
- **Documentation**: Check `docs/CONFIGURING.md` for advanced configuration

## 🎯 What's Next?

1. **Upload your resume** and a job description
2. **Get AI-powered analysis** using Gemini's advanced language understanding
3. **Receive optimization suggestions** to improve your resume match score
4. **Iterate and improve** your resume for better ATS compatibility

## 🔒 Security Notes

- Your API key is stored locally in `.env` files
- Never commit `.env` files to version control
- The application runs entirely on your machine
- No data is sent to external servers except Google's Gemini API

---

**Happy job hunting! 🎉**
