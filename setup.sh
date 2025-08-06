#!/bin/bash

# Browser Use Agent Setup Script
# This script sets up the complete environment for the Browser Use Agent

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python version..."

    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi

    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    required_version="3.8"

    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
        print_success "Python $python_version is installed"
    else
        print_error "Python $python_version is installed, but version 3.8 or higher is required."
        exit 1
    fi
}

# Setup virtual environment
setup_venv() {
    local venv_name="browser_use_env"

    print_status "Setting up virtual environment..."

    if [ -d "$venv_name" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf "$venv_name"
    fi

    python3 -m venv "$venv_name"
    print_success "Virtual environment created: $venv_name"

    # Activate virtual environment
    source "$venv_name/bin/activate"
    print_success "Virtual environment activated"

    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."

    # Install browser-use and its dependencies
    pip install browser-use

    # Install additional dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        print_status "Installing additional requirements from requirements.txt..."
        pip install -r requirements.txt
    fi

    print_success "Python dependencies installed"
}

# Install Playwright browsers
install_playwright() {
    print_status "Installing Playwright browsers..."

    # Install Playwright browsers
    playwright install chromium

    # Install system dependencies for Playwright
    if command -v apt-get &> /dev/null; then
        print_status "Installing system dependencies (Ubuntu/Debian)..."
        playwright install-deps chromium
    elif command -v yum &> /dev/null; then
        print_warning "CentOS/RHEL detected. You may need to manually install system dependencies."
        print_warning "Run: playwright install-deps chromium"
    elif command -v brew &> /dev/null; then
        print_status "macOS detected. System dependencies should be handled automatically."
        playwright install-deps chromium
    else
        print_warning "Unknown system. You may need to manually install Playwright system dependencies."
        print_warning "Run: playwright install-deps chromium"
    fi

    print_success "Playwright browsers installed"
}

# Setup environment file
setup_env_file() {
    print_status "Setting up environment configuration..."

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Created .env file from .env.example"
        else
            cat > .env << EOF
# Browser Use Agent Environment Configuration
# Add your API keys below

# OpenAI API Key (recommended - GPT-4o model)
OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key (alternative - Claude 3.5 Sonnet model)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Browser Use Configuration
BROWSER_USE_LOGGING_LEVEL=info
BROWSER_USE_HEADLESS=false

# Playwright Configuration
PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net
EOF
            print_success "Created .env file with default configuration"
        fi

        print_warning "Please edit .env file and add your API keys!"
    else
        print_warning ".env file already exists. Skipping creation."
    fi
}

# Test the installation
test_installation() {
    print_status "Testing installation..."

    # Test Python imports
    python3 -c "
import browser_use
import playwright
print('✓ All imports successful')
" 2>/dev/null

    if [ $? -eq 0 ]; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed. Please check the error messages above."
        exit 1
    fi
}

# Create activation script
create_activation_script() {
    print_status "Creating activation script..."

    cat > activate_browser_agent.sh << 'EOF'
#!/bin/bash
# Activation script for Browser Use Agent

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/browser_use_env"

if [ -d "$VENV_DIR" ]; then
    echo "Activating Browser Use Agent environment..."
    source "$VENV_DIR/bin/activate"

    # Load environment variables
    if [ -f "$SCRIPT_DIR/.env" ]; then
        export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
    fi

    echo "Environment activated! You can now run:"
    echo "  python browser_agent.py --url 'https://example.com' --task 'your task'"
    echo "  python examples.py --example search"
    echo ""
    echo "To deactivate, run: deactivate"
else
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi
EOF

    chmod +x activate_browser_agent.sh
    print_success "Created activation script: activate_browser_agent.sh"
}

# Print usage instructions
print_usage() {
    print_success "Setup completed successfully!"
    echo ""
    echo "🚀 Getting Started:"
    echo "  1. Edit the .env file and add your API keys"
    echo "  2. Activate the environment: source activate_browser_agent.sh"
    echo "  3. Run an example: python browser_agent.py --url 'https://google.com' --task 'Search for browser automation'"
    echo ""
    echo "📋 Available Commands:"
    echo "  python browser_agent.py --help           # See all options"
    echo "  python examples.py --list               # List example scenarios"
    echo "  python examples.py --example search     # Run search example"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  - Make sure you have set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env"
    echo "  - For headless mode, add --headless flag"
    echo "  - Check browser_agent.log for detailed execution logs"
    echo ""
    echo "📚 Documentation: https://docs.browser-use.com"
    echo "💬 Community: https://discord.gg/browser-use"
}

# Main setup function
main() {
    echo "🔧 Browser Use Agent Setup"
    echo "=========================="
    echo ""

    # Check if we're in the right directory
    if [ ! -f "browser_agent.py" ]; then
        print_error "browser_agent.py not found. Please run this script from the browser_use directory."
        exit 1
    fi

    # Run setup steps
    check_python
    setup_venv
    install_dependencies
    install_playwright
    setup_env_file
    test_installation
    create_activation_script

    echo ""
    print_usage
}

# Run main function
main "$@"
