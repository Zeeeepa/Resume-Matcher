#!/usr/bin/env bash
#
# run_with_gemini.sh - Setup and run Resume Matcher with Gemini API
#
# Usage:
#   ./run_with_gemini.sh [GEMINI_API_KEY]
#
# This script will:
#   • Prompt for Gemini API key if not provided
#   • Set up the complete Resume Matcher environment
#   • Configure Gemini as the default LLM and embedding provider
#   • Install all dependencies
#   • Start both backend and frontend servers
#

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis for better UX
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
GEAR="⚙️"
KEY="🔑"
ROBOT="🤖"
FIRE="🔥"
SPARKLES="✨"

print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Resume Matcher + Gemini                  ║"
    echo "║                   Setup & Launch Script                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}${GEAR} $1${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Gemini API key
get_gemini_api_key() {
    local api_key="${1:-}"
    
    if [[ -z "$api_key" ]]; then
        echo -e "${YELLOW}${KEY} Gemini API Key Required${NC}"
        echo -e "${CYAN}Get your free API key from: https://aistudio.google.com/${NC}"
        echo ""
        read -p "Enter your Gemini API key: " -r api_key
        
        if [[ -z "$api_key" ]]; then
            print_error "API key is required to continue"
            exit 1
        fi
    fi
    
    # Basic validation - Gemini API keys start with "AIza"
    if [[ ! "$api_key" =~ ^AIza[A-Za-z0-9_-]{35}$ ]]; then
        print_warning "API key format looks unusual. Gemini API keys typically start with 'AIza' and are 39 characters long."
        read -p "Continue anyway? (y/N): " -r confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    echo "$api_key"
}

# Function to check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check Node.js
    if ! command_exists node; then
        missing_deps+=("node")
    else
        local node_version
        node_version=$(node --version | sed 's/v//')
        local major_version
        major_version=$(echo "$node_version" | cut -d. -f1)
        if [[ "$major_version" -lt 18 ]]; then
            print_error "Node.js version $node_version found, but version 18+ is required"
            missing_deps+=("node (v18+)")
        else
            print_success "Node.js $node_version found"
        fi
    fi
    
    # Check npm
    if ! command_exists npm; then
        missing_deps+=("npm")
    else
        print_success "npm $(npm --version) found"
    fi
    
    # Check Python
    if ! command_exists python3; then
        missing_deps+=("python3")
    else
        local python_version
        python_version=$(python3 --version | cut -d' ' -f2)
        local major_version
        major_version=$(echo "$python_version" | cut -d. -f1)
        local minor_version
        minor_version=$(echo "$python_version" | cut -d. -f2)
        if [[ "$major_version" -lt 3 ]] || [[ "$major_version" -eq 3 && "$minor_version" -lt 8 ]]; then
            print_error "Python $python_version found, but Python 3.8+ is required"
            missing_deps+=("python3 (3.8+)")
        else
            print_success "Python $python_version found"
        fi
    fi
    
    # Check pip
    if ! command_exists pip3; then
        missing_deps+=("pip3")
    else
        print_success "pip3 found"
    fi
    
    # Check uv (will install if missing)
    if ! command_exists uv; then
        print_warning "uv not found - will install automatically"
    else
        print_success "uv $(uv --version | cut -d' ' -f2) found"
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_error "Missing required dependencies:"
        for dep in "${missing_deps[@]}"; do
            echo -e "  ${RED}• $dep${NC}"
        done
        echo ""
        echo -e "${CYAN}Please install the missing dependencies and run this script again.${NC}"
        echo ""
        echo -e "${YELLOW}Installation guides:${NC}"
        echo -e "• Node.js: https://nodejs.org/"
        echo -e "• Python: https://www.python.org/downloads/"
        exit 1
    fi
    
    print_success "All prerequisites satisfied!"
}

# Function to install uv if missing
install_uv() {
    if ! command_exists uv; then
        print_step "Installing uv (Python package manager)..."
        if command_exists curl; then
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
            if command_exists uv; then
                print_success "uv installed successfully"
            else
                print_error "Failed to install uv"
                exit 1
            fi
        else
            print_error "curl is required to install uv"
            exit 1
        fi
    fi
}

# Function to setup environment files
setup_env_files() {
    local api_key="$1"
    
    print_step "Setting up environment configuration..."
    
    # Setup root .env if it doesn't exist
    if [[ ! -f .env ]]; then
        if [[ -f .env.example ]]; then
            cp .env.example .env
            print_success "Created root .env from .env.example"
        else
            touch .env
            print_success "Created root .env file"
        fi
    fi
    
    # Setup backend .env with Gemini configuration
    local backend_env="apps/backend/.env"
    
    print_step "Configuring Gemini API settings..."
    
    cat > "$backend_env" << EOF
# Session and Database Configuration
SESSION_SECRET_KEY="$(openssl rand -hex 32 2>/dev/null || echo "fallback-secret-key-$(date +%s)")"
SYNC_DATABASE_URL="sqlite:///./app.db"
ASYNC_DATABASE_URL="sqlite+aiosqlite:///./app.db"
PYTHONDONTWRITEBYTECODE=1

# Gemini API Configuration
LLM_PROVIDER="gemini"
EMBEDDING_PROVIDER="gemini"
GEMINI_API_KEY="$api_key"
LL_MODEL="gemini-1.5-flash"
EMBEDDING_MODEL="models/text-embedding-004"

# Optional: Fallback to other providers if needed
# LLM_API_KEY=""
# EMBEDDING_API_KEY=""
EOF
    
    print_success "Backend environment configured with Gemini API"
}

# Function to install dependencies
install_dependencies() {
    print_step "Installing project dependencies..."
    
    # Install root dependencies
    if [[ -f package.json ]]; then
        print_info "Installing root dependencies..."
        npm install
        print_success "Root dependencies installed"
    fi
    
    # Install frontend dependencies
    print_info "Installing frontend dependencies..."
    cd apps/frontend
    npm install
    cd ../..
    print_success "Frontend dependencies installed"
    
    # Install backend dependencies
    print_info "Setting up Python virtual environment and dependencies..."
    cd apps/backend
    
    # Create virtual environment with uv
    uv venv
    
    # Install dependencies
    uv pip install -r requirements.txt
    
    cd ../..
    print_success "Backend dependencies installed"
}

# Function to test Gemini integration
test_gemini_integration() {
    print_step "Testing Gemini API integration..."
    
    cd apps/backend
    
    # Run the test script
    if uv run python test_gemini.py; then
        print_success "Gemini integration test passed!"
    else
        print_error "Gemini integration test failed"
        print_warning "The application may still work, but there might be configuration issues"
        read -p "Continue anyway? (y/N): " -r confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    cd ../..
}

# Function to start the development servers
start_dev_servers() {
    print_step "Starting Resume Matcher with Gemini API..."
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                     🎉 Setup Complete! 🎉                   ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  Frontend: http://localhost:3000                            ║"
    echo "║  Backend:  http://localhost:8000                            ║"
    echo "║  API Docs: http://localhost:8000/docs                       ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  Press Ctrl+C to stop both servers                         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Function to handle cleanup on exit
    cleanup() {
        echo -e "\n${YELLOW}Shutting down servers...${NC}"
        kill 0
        exit 0
    }
    
    # Set up signal handlers
    trap cleanup SIGINT SIGTERM
    
    # Start both servers concurrently
    npm run dev &
    
    # Wait for all background processes
    wait
}

# Function to show usage information
show_usage() {
    echo -e "${CYAN}Usage:${NC}"
    echo "  $0 [GEMINI_API_KEY]"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo "  $0                                    # Will prompt for API key"
    echo "  $0 AIzaSyBXmhlHudrD4zXiv-5fjxi1gGG-_kdtaZ0  # Use provided API key"
    echo ""
    echo -e "${CYAN}Get your Gemini API key from:${NC}"
    echo "  https://aistudio.google.com/"
}

# Main execution
main() {
    print_header
    
    # Handle help flag
    if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
        show_usage
        exit 0
    fi
    
    # Get API key
    local api_key
    api_key=$(get_gemini_api_key "${1:-}")
    
    print_info "Using Gemini API key: ${api_key:0:10}...${api_key: -4}"
    echo ""
    
    # Run setup steps
    check_prerequisites
    install_uv
    setup_env_files "$api_key"
    install_dependencies
    test_gemini_integration
    
    echo ""
    print_success "Setup completed successfully!"
    echo ""
    
    # Ask if user wants to start the servers
    read -p "Start the development servers now? (Y/n): " -r start_servers
    if [[ ! "$start_servers" =~ ^[Nn]$ ]]; then
        echo ""
        start_dev_servers
    else
        echo ""
        print_info "To start the servers later, run:"
        echo -e "${CYAN}  npm run dev${NC}"
        echo ""
        print_info "Or start them individually:"
        echo -e "${CYAN}  npm run dev:backend   # Backend only${NC}"
        echo -e "${CYAN}  npm run dev:frontend  # Frontend only${NC}"
    fi
}

# Run main function with all arguments
main "$@"
