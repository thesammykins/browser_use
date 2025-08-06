# Browser Use Agent - Model Configuration Guide

This guide explains how to configure and use different LLM models with the Browser Use Agent.

## Quick Start

### 1. Basic Configuration (Environment Variables)

Edit your `.env` file:

```env
# Choose your preferred provider
BROWSER_USE_PREFERRED_PROVIDER=openai

# Set specific models (optional - uses defaults if not set)
BROWSER_USE_OPENAI_MODEL=gpt-4o
BROWSER_USE_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 2. Command Line Override

```bash
# Override provider and model for a single run
python browser_agent.py \
  --provider anthropic \
  --model claude-3-5-sonnet-20241022 \
  --url "https://example.com" \
  --task "your task"
```

## Supported Providers and Models

### 🤖 OpenAI

**API Key:** `OPENAI_API_KEY`  
**Model Config:** `BROWSER_USE_OPENAI_MODEL`

```env
OPENAI_API_KEY=sk-your-key-here
BROWSER_USE_OPENAI_MODEL=gpt-4o  # Default
```

**Available Models:**
- `gpt-4o` (Recommended - Best performance)
- `gpt-4o-mini` (Faster and cheaper)
- `gpt-4-turbo` (Previous generation)
- `gpt-4` (Standard GPT-4)

**Best for:** General automation, complex reasoning, reliable performance

### 🧠 Anthropic

**API Key:** `ANTHROPIC_API_KEY`  
**Model Config:** `BROWSER_USE_ANTHROPIC_MODEL`

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
BROWSER_USE_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Default
```

**Available Models:**
- `claude-3-5-sonnet-20241022` (Recommended - Latest version)
- `claude-3-5-sonnet-20240620` (Previous version)
- `claude-3-opus-20240229` (Most capable but slower)
- `claude-3-haiku-20240307` (Fastest and cheapest)

**Best for:** Detailed analysis, safety-conscious automation, code generation

### 🔍 Google

**API Key:** `GOOGLE_API_KEY`  
**Model Config:** `BROWSER_USE_GOOGLE_MODEL`

```env
GOOGLE_API_KEY=your-key-here
BROWSER_USE_GOOGLE_MODEL=gemini-2.0-flash-exp  # Default
```

**Available Models:**
- `gemini-2.0-flash-exp` (Recommended - Latest experimental)
- `gemini-1.5-pro` (Pro version)
- `gemini-1.5-flash` (Fast version)

**Best for:** Multi-modal tasks, experimental features

### ⚡ Groq

**API Key:** `GROQ_API_KEY`  
**Model Config:** `BROWSER_USE_GROQ_MODEL`

```env
GROQ_API_KEY=gsk_your-key-here
BROWSER_USE_GROQ_MODEL=llama-3.3-70b-versatile  # Default
```

**Available Models:**
- `llama-3.3-70b-versatile` (Recommended - Latest Llama)
- `llama-3.1-70b-versatile` (Previous version)
- `mixtral-8x7b-32768` (Alternative architecture)

**Best for:** Fast inference, cost-effective automation

### ☁️ Azure OpenAI

**API Key:** `AZURE_OPENAI_API_KEY`  
**Endpoint:** `AZURE_OPENAI_ENDPOINT`  
**Model Config:** `BROWSER_USE_AZURE_MODEL`

```env
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
BROWSER_USE_AZURE_MODEL=gpt-4o  # Default
```

**Available Models:** (Depends on your Azure deployment)
- `gpt-4o`
- `gpt-4-turbo`
- `gpt-4`

**Best for:** Enterprise deployments, data residency requirements

## Configuration Examples

### Example 1: Cost-Optimized Setup

```env
# Use cheaper models for basic tasks
BROWSER_USE_PREFERRED_PROVIDER=openai
BROWSER_USE_OPENAI_MODEL=gpt-4o-mini

# Fallback to Anthropic's fastest model
ANTHROPIC_API_KEY=sk-ant-your-key-here
BROWSER_USE_ANTHROPIC_MODEL=claude-3-haiku-20240307
```

### Example 2: Performance-Optimized Setup

```env
# Use the most capable models
BROWSER_USE_PREFERRED_PROVIDER=anthropic
BROWSER_USE_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Fallback to OpenAI's best model
OPENAI_API_KEY=sk-your-key-here
BROWSER_USE_OPENAI_MODEL=gpt-4o
```

### Example 3: Multi-Provider Setup

```env
# Configure all providers with specific models
BROWSER_USE_PREFERRED_PROVIDER=openai

OPENAI_API_KEY=sk-your-key-here
BROWSER_USE_OPENAI_MODEL=gpt-4o

ANTHROPIC_API_KEY=sk-ant-your-key-here
BROWSER_USE_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

GOOGLE_API_KEY=your-key-here
BROWSER_USE_GOOGLE_MODEL=gemini-1.5-pro

GROQ_API_KEY=gsk-your-key-here
BROWSER_USE_GROQ_MODEL=llama-3.3-70b-versatile
```

## Command Line Usage

### Override Provider Only

```bash
python browser_agent.py --provider anthropic --url "..." --task "..."
```

### Override Model Only (for preferred provider)

```bash
python browser_agent.py --model gpt-4o-mini --url "..." --task "..."
```

### Override Both Provider and Model

```bash
python browser_agent.py --provider anthropic --model claude-3-haiku-20240307 --url "..." --task "..."
```

### Examples Script with Model Override

```bash
python examples.py --example search --provider openai --model gpt-4o-mini
python examples.py --all --provider anthropic --model claude-3-5-sonnet-20241022
```

## Model Selection Strategy

### Provider Priority (if no preference set)
1. OpenAI (most tested)
2. Anthropic (good safety features)
3. Google (experimental features)
4. Groq (fast inference)
5. Azure (enterprise)

### When to Use Each Model

**For Simple Tasks (forms, clicking, basic navigation):**
- `gpt-4o-mini` (OpenAI) - Fast and cheap
- `claude-3-haiku-20240307` (Anthropic) - Very fast

**For Complex Tasks (analysis, multi-step workflows):**
- `gpt-4o` (OpenAI) - Reliable performance
- `claude-3-5-sonnet-20241022` (Anthropic) - Latest capabilities

**For Experimental Features:**
- `gemini-2.0-flash-exp` (Google) - Cutting-edge features

**For High-Volume Automation:**
- `llama-3.3-70b-versatile` (Groq) - Fast inference
- `gpt-4o-mini` (OpenAI) - Cost-effective

## Troubleshooting

### Model Not Found Error

```bash
# Check available models for your provider
python browser_agent.py --provider openai --model invalid-model --url "..." --task "..."
# Error: Model 'invalid-model' not found
```

**Solution:** Use valid model names from the lists above.

### API Key Issues

```bash
# Test your configuration
python test_setup.py
```

**Common Issues:**
- Wrong API key format
- Expired API key
- Missing endpoint for Azure
- Regional restrictions

### Performance Issues

**If model is too slow:**
- Use faster models: `gpt-4o-mini`, `claude-3-haiku-20240307`
- Try Groq for fastest inference
- Use `--headless` mode

**If model gives poor results:**
- Use more capable models: `gpt-4o`, `claude-3-5-sonnet-20241022`
- Check task complexity
- Try different provider

### Provider Fallback

If your preferred provider fails, the agent automatically tries others:

```
OpenAI (preferred) → Failed
Anthropic → Success ✓
```

You'll see this in the logs:
```
[WARNING] Failed to initialize OpenAI: API key invalid
[INFO] Using Anthropic with model: claude-3-5-sonnet-20241022
```

## Best Practices

1. **Set a preferred provider** to ensure consistent behavior
2. **Configure specific models** rather than relying on defaults
3. **Test with different models** to find the best fit for your use case
4. **Use cost-effective models** for development and testing
5. **Keep API keys secure** in environment variables
6. **Monitor usage and costs** across different providers
7. **Use command-line overrides** for quick testing

## Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the key (starts with `sk-`)

### Anthropic
1. Visit https://console.anthropic.com/
2. Go to API Keys section
3. Create new key (starts with `sk-ant-`)

### Google
1. Visit https://makersuite.google.com/app/apikey
2. Create API key
3. Enable the Generative AI API

### Groq
1. Visit https://console.groq.com/keys
2. Create new API key (starts with `gsk_`)

### Azure OpenAI
1. Set up Azure OpenAI service
2. Deploy a model
3. Get endpoint and API key from Azure portal

## Support

- Check `test_setup.py` for configuration validation
- Review logs in `browser_agent.log` for detailed debugging
- Test different models with simple tasks first
- Join Browser Use Discord for community support