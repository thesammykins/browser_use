#!/usr/bin/env python3
"""
Test script to verify Browser Use Agent installation and configuration.

This script checks that all dependencies are properly installed and configured.

Usage:
    python test_setup.py
"""

import sys
import os
import importlib
from pathlib import Path


def print_status(message, status="info"):
    """Print status message with color coding."""
    colors = {
        "info": "\033[0;34m[INFO]\033[0m",
        "success": "\033[0;32m[SUCCESS]\033[0m",
        "warning": "\033[1;33m[WARNING]\033[0m",
        "error": "\033[0;31m[ERROR]\033[0m"
    }
    print(f"{colors.get(status, '')} {message}")


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_status("Checking Python version...")
    version = sys.version_info

    if version.major >= 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} ✓", "success")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+", "error")
        return False


def check_imports():
    """Check if required packages can be imported."""
    print_status("Checking package imports...")

    packages = [
        ("browser_use", "Browser Use library"),
        ("playwright", "Playwright automation library"),
        ("asyncio", "Async support"),
        ("argparse", "Argument parsing"),
        ("logging", "Logging support"),
        ("pathlib", "Path handling"),
    ]

    all_good = True

    for package, description in packages:
        try:
            importlib.import_module(package)
            print_status(f"  {description} ✓", "success")
        except ImportError as e:
            print_status(f"  {description} ✗ - {e}", "error")
            all_good = False

    return all_good


def check_browser_use_components():
    """Check if browser-use components are available."""
    print_status("Checking Browser Use components...")

    try:
        from browser_use import Agent, BrowserSession, BrowserProfile
        print_status("  Core classes ✓", "success")
    except ImportError as e:
        print_status(f"  Core classes ✗ - {e}", "error")
        return False

    try:
        from browser_use.llm import ChatOpenAI, ChatAnthropic
        print_status("  LLM providers ✓", "success")
    except ImportError as e:
        print_status(f"  LLM providers ✗ - {e}", "error")
        return False

    return True


def check_playwright_installation():
    """Check if Playwright browsers are installed."""
    print_status("Checking Playwright installation...")

    try:
        import playwright
        from playwright.sync_api import sync_playwright

        print_status("  Playwright package ✓", "success")

        # Check if chromium is available
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
            print_status("  Chromium browser ✓", "success")
            return True
        except Exception as e:
            print_status(f"  Chromium browser ✗ - {e}", "error")
            print_status("  Run: playwright install chromium", "warning")
            return False

    except ImportError as e:
        print_status(f"  Playwright package ✗ - {e}", "error")
        return False


def check_api_keys():
    """Check if API keys are configured."""
    print_status("Checking API key configuration...")

    api_keys = [
        ("OPENAI_API_KEY", "OpenAI GPT models"),
        ("ANTHROPIC_API_KEY", "Anthropic Claude models"),
        ("GOOGLE_API_KEY", "Google Gemini models"),
        ("GROQ_API_KEY", "Groq models"),
        ("AZURE_OPENAI_API_KEY", "Azure OpenAI models"),
    ]

    found_keys = 0

    for key_name, description in api_keys:
        key_value = os.getenv(key_name)
        if key_value and key_value != "your-api-key-here":
            print_status(f"  {description} ✓", "success")
            found_keys += 1
        else:
            print_status(f"  {description} ✗", "warning")

    if found_keys == 0:
        print_status("  No API keys found. Please configure at least one in .env", "error")
        return False
    elif found_keys >= 1:
        print_status(f"  Found {found_keys} configured API key(s)", "success")
        return True

    return found_keys > 0


def check_model_configuration():
    """Check if model configuration is properly set."""
    print_status("Checking model configuration...")

    # Check preferred provider setting
    preferred_provider = os.getenv('BROWSER_USE_PREFERRED_PROVIDER')
    if preferred_provider:
        valid_providers = ['openai', 'anthropic', 'google', 'groq', 'azure']
        if preferred_provider.lower() in valid_providers:
            print_status(f"  Preferred provider: {preferred_provider} ✓", "success")
        else:
            print_status(f"  Invalid preferred provider: {preferred_provider} ✗", "warning")
    else:
        print_status("  No preferred provider set (will use auto-detection)", "info")

    # Check model configurations
    model_configs = [
        ("BROWSER_USE_OPENAI_MODEL", "OpenAI model", "OPENAI_API_KEY"),
        ("BROWSER_USE_ANTHROPIC_MODEL", "Anthropic model", "ANTHROPIC_API_KEY"),
        ("BROWSER_USE_GOOGLE_MODEL", "Google model", "GOOGLE_API_KEY"),
        ("BROWSER_USE_GROQ_MODEL", "Groq model", "GROQ_API_KEY"),
        ("BROWSER_USE_AZURE_MODEL", "Azure model", "AZURE_OPENAI_API_KEY"),
    ]

    configured_models = 0
    for model_env, description, api_key_env in model_configs:
        model = os.getenv(model_env)
        api_key = os.getenv(api_key_env)

        if model:
            if api_key and api_key != "your-api-key-here":
                print_status(f"  {description}: {model} ✓", "success")
                configured_models += 1
            else:
                print_status(f"  {description}: {model} (no API key) ✗", "warning")
        elif api_key and api_key != "your-api-key-here":
            print_status(f"  {description}: using default ✓", "success")

    if configured_models > 0:
        print_status(f"  Found {configured_models} custom model configuration(s)", "success")

    return True


def check_project_files():
    """Check if required project files exist."""
    print_status("Checking project files...")

    required_files = [
        ("browser_agent.py", "Main agent script"),
        ("examples.py", "Example scenarios"),
        ("requirements.txt", "Dependencies list"),
        (".env.example", "Environment template"),
    ]

    all_present = True

    for filename, description in required_files:
        if Path(filename).exists():
            print_status(f"  {description} ✓", "success")
        else:
            print_status(f"  {description} ✗", "error")
            all_present = False

    # Check for .env file
    if Path(".env").exists():
        print_status("  Environment file (.env) ✓", "success")
    else:
        print_status("  Environment file (.env) ✗ - Copy from .env.example", "warning")

    return all_present


def check_permissions():
    """Check file permissions for executable scripts."""
    print_status("Checking file permissions...")

    executable_files = ["setup.sh"]

    for filename in executable_files:
        filepath = Path(filename)
        if filepath.exists():
            if os.access(filepath, os.X_OK):
                print_status(f"  {filename} executable ✓", "success")
            else:
                print_status(f"  {filename} not executable - Run: chmod +x {filename}", "warning")
        else:
            print_status(f"  {filename} not found", "warning")

    return True


def run_basic_functionality_test():
    """Run a basic functionality test."""
    print_status("Running basic functionality test...")

    try:
        from browser_agent import BrowserAgent

        # Test class instantiation
        agent = BrowserAgent(headless=True)
        print_status("  BrowserAgent instantiation ✓", "success")

        # Test LLM setup (without actually calling it)
        available_keys = [
            'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY',
            'GROQ_API_KEY', 'AZURE_OPENAI_API_KEY'
        ]

        has_api_key = any(os.getenv(key) and os.getenv(key) != "your-api-key-here"
                         for key in available_keys)

        if has_api_key:
            try:
                agent.setup_llm()
                print_status("  LLM configuration ✓", "success")

                # Display which provider was selected
                llm_class_name = type(agent.llm).__name__ if agent.llm else "Unknown"
                print_status(f"  Selected LLM provider: {llm_class_name}", "info")

            except Exception as e:
                print_status(f"  LLM configuration ✗ - {e}", "error")
                return False
        else:
            print_status("  LLM configuration skipped (no valid API key)", "warning")

        return True

    except Exception as e:
        print_status(f"  Functionality test failed - {e}", "error")
        return False


def main():
    """Run all setup verification tests."""
    print("🔧 Browser Use Agent Setup Verification")
    print("=" * 50)
    print()

    tests = [
        ("Python Version", check_python_version),
        ("Package Imports", check_imports),
        ("Browser Use Components", check_browser_use_components),
        ("Playwright Installation", check_playwright_installation),
        ("API Key Configuration", check_api_keys),
        ("Model Configuration", check_model_configuration),
        ("Project Files", check_project_files),
        ("File Permissions", check_permissions),
        ("Basic Functionality", run_basic_functionality_test),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Test failed with exception: {e}", "error")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 SETUP VERIFICATION SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")

    print(f"\nPassed: {passed}/{total} tests")

    if passed == total:
        print_status("\n🎉 All tests passed! Your setup is ready.", "success")
        print("Next steps:")
        print("  1. Make sure you have API keys configured in .env")
        print("  2. Optionally configure preferred provider: BROWSER_USE_PREFERRED_PROVIDER=openai")
        print("  3. Optionally configure specific models: BROWSER_USE_OPENAI_MODEL=gpt-4o-mini")
        print("  4. Try running: python browser_agent.py --url 'https://google.com' --task 'Search for browser automation'")
        print("  5. Or run examples: python examples.py --example search")
        print("  6. Use command-line overrides: --provider anthropic --model claude-3-5-sonnet-20241022")
        return 0
    else:
        print_status(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.", "warning")
        print("\nTroubleshooting tips:")
        print("  - Run ./setup.sh to install dependencies")
        print("  - Configure API keys in .env file")
        print("  - Set model preferences in .env file")
        print("  - Install Playwright browsers: playwright install chromium")
        print("  - Use --provider and --model flags to override defaults")
        return 1


if __name__ == "__main__":
    sys.exit(main())
