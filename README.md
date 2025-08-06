# Browser Use Agent 🤖🌐

A flexible and powerful browser automation agent that can navigate to any website and perform specified tasks using AI. Built on top of the [browser-use](https://github.com/browser-use/browser-use) library with support for multiple LLM providers.

## ✨ Features

- **Universal Web Automation**: Navigate to any website and perform complex tasks
- **AI-Powered**: Uses advanced language models (GPT-4, Claude) for intelligent decision making
- **Multiple LLM Support**: OpenAI, Anthropic, Google, Groq, and more
- **Flexible Configuration**: Headless/headful mode, custom viewports, persistent sessions
- **Rich Examples**: Pre-built scenarios for common automation tasks
- **Comprehensive Logging**: Detailed execution logs for debugging and analysis
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

You have **two setup options**. Use `setup.sh` for automated setup or follow manual steps:

### Option 1: Automated Setup (Recommended)

```bash
# Clone or download the project
cd browser_use

# Run the automated setup script
./setup.sh
```

This script will:
- Create virtual environment (`browser_use_env/`)
- Install all dependencies including browser-use and playwright
- Install Chromium browser
- Create `.env` configuration file
- Create activation script (`activate_browser_agent.sh`)

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv browser_use_env
source browser_use_env/bin/activate

# Install dependencies
pip install browser-use
playwright install chromium
playwright install-deps

# Copy environment template
cp .env.example .env
```

### 2. Configure API Keys

Edit the `.env` file and add your API key:

```env
# Choose one or more LLM providers
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Optional: Configure specific models and provider preference
BROWSER_USE_PREFERRED_PROVIDER=openai
BROWSER_USE_OPENAI_MODEL=gpt-4o
BROWSER_USE_ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

### 3. Run Your First Task

```bash
# If you used setup.sh, activate with:
source activate_browser_agent.sh

# If you used manual setup, activate with:
source browser_use_env/bin/activate

# Basic example
python browser_agent.py --url "https://google.com" --task "Search for 'browser automation'"

# Run with examples
python examples.py --example search
```

## 📖 Usage

### Command Line Interface

The main `browser_agent.py` script accepts the following parameters:

```bash
python browser_agent.py [OPTIONS]

Required Arguments:
  --url URL            Target website URL to navigate to
  --task TASK          Task description for the AI agent to perform

Optional Arguments:
  --headless           Run browser in headless mode (no GUI)
  --viewport-width W   Browser viewport width (default: 1280)
  --viewport-height H  Browser viewport height (default: 1024)
  --user-data-dir DIR  Directory for browser user data (persistent sessions)
  --storage-state FILE Path to storage state file (saved cookies/auth)
  --model MODEL        Override LLM model (e.g., gpt-4o, claude-3-5-sonnet-20241022)
  --provider PROVIDER  Force specific LLM provider (openai, anthropic, google, groq, azure)
  --verbose            Enable verbose logging
```

### Basic Examples

```bash
# Web search and analysis
python browser_agent.py \
  --url "https://google.com" \
  --task "Search for 'AI browser automation' and summarize the top 3 results"

# Form filling
python browser_agent.py \
  --url "https://httpbin.org/forms/post" \
  --task "Fill out the form with sample data and submit it"

# Data extraction
python browser_agent.py \
  --url "https://news.ycombinator.com" \
  --task "Extract the titles and scores of the top 10 stories"

# E-commerce interaction
python browser_agent.py \
  --url "https://demo.opencart.com" \
  --task "Search for laptops, compare the first 3 results, and add the best one to cart"
```

### Advanced Usage

```bash
# Headless mode with custom viewport
python browser_agent.py \
  --url "https://example.com" \
  --task "Screenshot the homepage" \
  --headless \
  --viewport-width 1920 \
  --viewport-height 1080

# Persistent session with saved authentication
python browser_agent.py \
  --url "https://github.com" \
  --task "Check my repositories and create a new one" \
  --storage-state "github_auth.json" \
  --user-data-dir "./browser_data"

# Use specific model and provider
python browser_agent.py \
  --url "https://example.com" \
  --task "Analyze the homepage content" \
  --provider anthropic \
  --model claude-3-5-sonnet-20241022
```

## 🎯 Pre-built Examples

The `examples.py` script includes various scenarios:

```bash
# List all available examples
python examples.py --list

# Run specific examples
python examples.py --example search        # Web search
python examples.py --example form          # Form filling
python examples.py --example data          # Data extraction
python examples.py --example navigation    # Multi-page navigation
python examples.py --example shopping      # E-commerce browsing
python examples.py --example social        # Social media analysis
python examples.py --example accessibility # Accessibility testing
python examples.py --example api           # API testing

# Run all examples
python examples.py --all
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project directory:

```env
# LLM Provider (choose one or more)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Optional providers
GOOGLE_API_KEY=your-google-api-key-here
GROQ_API_KEY=your-groq-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-api-key-here

# Model Configuration (optional)
BROWSER_USE_PREFERRED_PROVIDER=openai
BROWSER_USE_OPENAI_MODEL=gpt-4o
BROWSER_USE_ANTHROPIC_MODEL=claude-sonnet-4-20250514
BROWSER_USE_GOOGLE_MODEL=gemini-2.0-flash-exp
BROWSER_USE_GROQ_MODEL=llama-3.3-70b-versatile
BROWSER_USE_AZURE_MODEL=gpt-4o

# Browser Use Settings
BROWSER_USE_LOGGING_LEVEL=info
BROWSER_USE_HEADLESS=false

# Playwright Settings
PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net
```

### Programmatic Usage

You can also use the BrowserAgent class directly in your Python code:

```python
import asyncio
from browser_agent import BrowserAgent

async def main():
    # Create agent
    agent = BrowserAgent(
        headless=False,
        viewport_width=1280,
        viewport_height=1024
    )
    
    # Run task
    result = await agent.run_task(
        url="https://example.com",
        task="Navigate to the about page and extract the company information"
    )
    
    if result['success']:
        print("Task completed successfully!")
        print(f"Actions performed: {len(result['history'])}")
    else:
        print(f"Task failed: {result['error']}")

# Run the agent
asyncio.run(main())
```

## 🔧 Supported LLM Providers

The agent supports multiple LLM providers:

| Provider | Model Examples | API Key | Model Config |
|----------|----------------|---------|--------------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo | `OPENAI_API_KEY` | `BROWSER_USE_OPENAI_MODEL` |
| Anthropic | claude-sonnet-4-20250514, claude-opus-4-20250514, claude-3-7-sonnet-20250219, claude-3-5-sonnet-20241022 | `ANTHROPIC_API_KEY` | `BROWSER_USE_ANTHROPIC_MODEL` |
| Google | gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash | `GOOGLE_API_KEY` | `BROWSER_USE_GOOGLE_MODEL` |
| Groq | llama-3.3-70b-versatile, llama3-70b-8192, mixtral-8x7b-32768 | `GROQ_API_KEY` | `BROWSER_USE_GROQ_MODEL` |
| Azure OpenAI | gpt-4o, gpt-4-turbo | `AZURE_OPENAI_API_KEY` | `BROWSER_USE_AZURE_MODEL` |

### Model Selection Priority

1. **Command line overrides**: `--provider` and `--model` flags take highest priority
2. **Environment variables**: `BROWSER_USE_PREFERRED_PROVIDER` sets the preferred provider
3. **Automatic fallback**: If preferred provider fails, tries others in order: OpenAI → Anthropic → Google → Groq → Azure

### Model Configuration Examples

```bash
# Use specific provider and model via environment
export BROWSER_USE_PREFERRED_PROVIDER=anthropic
export BROWSER_USE_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Or override via command line
python browser_agent.py --provider openai --model gpt-4o-mini --url "..." --task "..."
```

## 📁 Project Structure

```
browser_use/
├── browser_agent.py          # Main agent script
├── examples.py               # Pre-built example scenarios
├── setup.sh                  # Automated setup script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment configuration template
├── README.md                 # This documentation
└── browser_use_env/          # Virtual environment (created by setup)
```

## 🐛 Troubleshooting

### Common Issues

**1. "No API key found" error**
```bash
# Make sure you've edited the .env file with your API keys
# If you used setup.sh, edit the created .env file
# If manual setup, copy from template first:
cp .env.example .env

# Then edit .env with your keys:
OPENAI_API_KEY='your-api-key-here'
# or
ANTHROPIC_API_KEY='your-api-key-here'

# You can also set provider preference
BROWSER_USE_PREFERRED_PROVIDER=openai
BROWSER_USE_OPENAI_MODEL=gpt-4o-mini  # Use cheaper model
```

**2. "browser-use package not found"**
```bash
# Make sure you're in the virtual environment
# If you used setup.sh:
source activate_browser_agent.sh

# If manual setup:
source browser_use_env/bin/activate

# Then install if needed:
pip install browser-use
```

**3. Playwright browser not found**
```bash
# Install Playwright browsers
playwright install chromium
playwright install-deps
```

**4. Permission denied on setup.sh**
```bash
# Make the script executable
chmod +x setup.sh
./setup.sh
```

**5. Task fails with timeout**
```bash
# Try increasing viewport or running in headful mode
python browser_agent.py --url "..." --task "..." --viewport-width 1920

# Or try a different model that might be faster
python browser_agent.py --provider openai --model gpt-4o-mini --url "..." --task "..."
```

**6. Model not working as expected**
```bash
# Try different model for better performance
python browser_agent.py --provider anthropic --model claude-sonnet-4-20250514 --url "..." --task "..."

# Check available models in your .env configuration
```

### Debug Mode

Enable detailed logging:

```bash
# Set environment variable
export BROWSER_USE_LOGGING_LEVEL=debug

# Or use verbose flag
python browser_agent.py --url "..." --task "..." --verbose
```

Check the `browser_agent.log` file for detailed execution logs.

## 📊 Output and Results

The agent provides structured results:

```json
{
  "success": true,
  "history": [
    {"action": "navigate", "url": "https://example.com"},
    {"action": "click", "element": "search button"},
    {"action": "type", "text": "search query"}
  ],
  "final_url": "https://example.com/results",
  "message": "Task completed successfully"
}
```

Logs are saved to `browser_agent.log` with detailed execution information.

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Report bugs or issues
2. Suggest new features or improvements
3. Submit pull requests
4. Add new example scenarios
5. Improve documentation

## 📝 License

This project is built on top of [browser-use](https://github.com/browser-use/browser-use), which is MIT licensed.

## 🔗 Related Links

- [Browser Use Documentation](https://docs.browser-use.com)
- [Browser Use GitHub](https://github.com/browser-use/browser-use)
- [Browser Use Discord Community](https://discord.gg/browser-use)
- [Playwright Documentation](https://playwright.dev/python/)

## 💡 Tips for Success

1. **Use setup.sh for easy installation** - Handles all dependencies automatically
2. **Be Specific**: Provide detailed task descriptions for better results
3. **Use Natural Language**: Describe tasks as you would to a human
4. **Break Down Complex Tasks**: Split large tasks into smaller, manageable steps
5. **Test in Headful Mode**: Use GUI mode first to see what the agent is doing
6. **Check Logs**: Review `browser_agent.log` for detailed execution information
7. **Handle Authentication**: Use `storage_state` for logged-in sessions
8. **Respect Rate Limits**: Be mindful of website rate limiting and terms of service
9. **Choose Right Model**: Use faster models (gpt-4o-mini, claude-3-5-haiku-20241022) for simple tasks, more capable models (claude-sonnet-4-20250514, gpt-4o) for complex workflows

## 📋 Quick Setup Checklist

✅ Run `./setup.sh` (or manual setup)  
✅ Edit `.env` file with your API keys  
✅ Activate environment with `source activate_browser_agent.sh`  
✅ Test with `python browser_agent.py --url "https://google.com" --task "search"`  
✅ Try examples with `python examples.py --example search`  

## 🎉 Getting Help

- Run `python test_setup.py` to verify your installation
- Check the troubleshooting section above
- Review the example scripts for common patterns
- Enable debug logging for detailed information
- Join the [Browser Use Discord](https://discord.gg/browser-use) community
- Open an issue on GitHub for bugs or feature requests

Happy automating! 🚀