#!/usr/bin/env python3
"""
Browser Use Agent Examples - Demonstrates various use cases and scenarios

This file contains example functions showing how to use the Browser Agent
for different types of tasks and websites.

Usage:
    python examples.py --example search
    python examples.py --example form_fill
    python examples.py --example data_extraction
"""

import asyncio
import argparse
import os
import sys
from typing import Optional
import os

# Import the browser agent
try:
    from browser_agent import BrowserAgent
except ImportError:
    print("Error: browser_agent.py not found. Please ensure it's in the same directory.")
    sys.exit(1)


class BrowserAgentExamples:
    """Collection of example use cases for the Browser Agent."""

    def __init__(self, headless: bool = False, provider: Optional[str] = None, model: Optional[str] = None):
        self.headless = headless
        self.provider = provider
        self.model = model

    async def search_example(self):
        """Example: Perform a web search and analyze results."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://google.com"
        task = """
        Search for 'browser automation with AI' and then:
        1. Click on the first 3 search results
        2. Read the title and first paragraph of each page
        3. Summarize what you learned about browser automation with AI
        """

        print("🔍 Running search example...")
        result = await agent.run_task(url, task)
        return result

    async def form_filling_example(self):
        """Example: Fill out a contact form."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://httpbin.org/forms/post"
        task = """
        Fill out this form with the following information:
        - Customer name: John Doe
        - Telephone: +1-555-123-4567
        - Email: john.doe@example.com
        - Size: Medium
        - Topping: Cheese
        - Delivery time: ASAP
        - Comments: Please ring the doorbell twice

        Then submit the form and confirm the submission was successful.
        """

        print("📝 Running form filling example...")
        result = await agent.run_task(url, task)
        return result

    async def data_extraction_example(self):
        """Example: Extract structured data from a webpage."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://news.ycombinator.com"
        task = """
        Extract the following information from the Hacker News front page:
        1. Get the top 10 story titles
        2. For each story, get the score/points and number of comments
        3. Organize this information in a structured format
        4. Identify which stories are trending (high score relative to time posted)
        """

        print("📊 Running data extraction example...")
        result = await agent.run_task(url, task)
        return result

    async def navigation_example(self):
        """Example: Navigate through multiple pages and gather information."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://github.com/trending"
        task = """
        Explore GitHub trending repositories:
        1. Look at the trending repositories for today
        2. Click on the top 3 repositories
        3. For each repository, gather:
           - Repository name and description
           - Number of stars and forks
           - Primary programming language
           - Recent commit activity
        4. Create a summary of the most interesting trends you observed
        """

        print("🧭 Running navigation example...")
        result = await agent.run_task(url, task)
        return result

    async def shopping_example(self):
        """Example: Browse and compare products (demo site)."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://demo.opencart.com"
        task = """
        Browse this demo e-commerce site:
        1. Search for 'laptop' products
        2. Compare the first 3 laptops you find
        3. Look at their specifications, prices, and ratings
        4. Add the best value laptop to the shopping cart
        5. Proceed to checkout (but don't complete the purchase)
        6. Provide a summary of your comparison and recommendation
        """

        print("🛒 Running shopping example...")
        result = await agent.run_task(url, task)
        return result

    async def social_media_example(self):
        """Example: Analyze content on a social platform."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://reddit.com/r/programming"
        task = """
        Analyze the r/programming subreddit:
        1. Look at the top 10 hot posts
        2. For each post, note:
           - Title and upvotes
           - Number of comments
           - Main topic/technology discussed
        3. Identify the most discussed programming languages or technologies
        4. Summarize current trends in the programming community
        """

        print("💬 Running social media example...")
        result = await agent.run_task(url, task)
        return result

    async def accessibility_example(self):
        """Example: Test website accessibility features."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://webaim.org"
        task = """
        Explore this accessibility-focused website:
        1. Navigate using keyboard-only controls (Tab key navigation)
        2. Check for alt text on images
        3. Test the contrast and readability of the content
        4. Look for accessibility tools and resources mentioned
        5. Provide an assessment of the site's accessibility features
        """

        print("♿ Running accessibility example...")
        result = await agent.run_task(url, task)
        return result

    async def api_testing_example(self):
        """Example: Test API endpoints through web interface."""
        agent = BrowserAgent(headless=self.headless)
        self._configure_model_overrides()

        url = "https://httpbin.org"
        task = """
        Test various HTTP operations using httpbin:
        1. Test a GET request with parameters
        2. Test a POST request with JSON data
        3. Test file upload functionality
        4. Check response headers and status codes
        5. Test different authentication methods if available
        6. Document what each test revealed about HTTP behavior
        """

        print("🔧 Running API testing example...")
        result = await agent.run_task(url, task)
        return result

    def _configure_model_overrides(self):
        """Configure model overrides from instance settings."""
        if self.provider:
            os.environ['BROWSER_USE_PREFERRED_PROVIDER'] = self.provider

        if self.model:
            # Set model for the preferred provider
            preferred = self.provider or os.getenv('BROWSER_USE_PREFERRED_PROVIDER', 'openai')
            model_env_map = {
                'openai': 'BROWSER_USE_OPENAI_MODEL',
                'anthropic': 'BROWSER_USE_ANTHROPIC_MODEL',
                'google': 'BROWSER_USE_GOOGLE_MODEL',
                'groq': 'BROWSER_USE_GROQ_MODEL',
                'azure': 'BROWSER_USE_AZURE_MODEL'
            }
            if preferred in model_env_map:
                os.environ[model_env_map[preferred]] = self.model


async def run_example(example_name: str, headless: bool = False, provider: Optional[str] = None, model: Optional[str] = None):
    """Run a specific example by name."""
    examples = BrowserAgentExamples(headless=headless, provider=provider, model=model)

    example_methods = {
        'search': examples.search_example,
        'form': examples.form_filling_example,
        'data': examples.data_extraction_example,
        'navigation': examples.navigation_example,
        'shopping': examples.shopping_example,
        'social': examples.social_media_example,
        'accessibility': examples.accessibility_example,
        'api': examples.api_testing_example,
    }

    if example_name not in example_methods:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples: {', '.join(example_methods.keys())}")
        return None

    print(f"🚀 Starting example: {example_name}")
    print("-" * 60)

    try:
        result = await example_methods[example_name]()

        print("-" * 60)
        if result and result.get('success'):
            print("✅ Example completed successfully!")
            print(f"📝 Actions performed: {len(result.get('history', []))}")
        else:
            print("❌ Example failed!")
            if result:
                print(f"Error: {result.get('error', 'Unknown error')}")

        return result

    except Exception as e:
        print(f"❌ Example failed with error: {e}")
        return None


async def run_all_examples(headless: bool = False, provider: Optional[str] = None, model: Optional[str] = None):
    """Run all examples in sequence."""
    examples = BrowserAgentExamples(headless=headless, provider=provider, model=model)

    all_examples = [
        ('search', examples.search_example),
        ('form', examples.form_filling_example),
        ('data', examples.data_extraction_example),
        ('navigation', examples.navigation_example),
        ('shopping', examples.shopping_example),
        ('social', examples.social_media_example),
        ('accessibility', examples.accessibility_example),
        ('api', examples.api_testing_example),
    ]

    results = {}

    print("🚀 Running all examples...")
    print("=" * 60)

    for name, method in all_examples:
        print(f"\n🔄 Starting example: {name}")
        try:
            result = await method()
            results[name] = result

            if result and result.get('success'):
                print(f"✅ {name} completed successfully!")
            else:
                print(f"❌ {name} failed!")

        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
            results[name] = {'success': False, 'error': str(e)}

        print("-" * 40)

    # Summary
    print("\n📊 SUMMARY")
    print("=" * 60)
    successful = sum(1 for r in results.values() if r and r.get('success'))
    total = len(results)

    print(f"Successful examples: {successful}/{total}")

    for name, result in results.items():
        status = "✅" if result and result.get('success') else "❌"
        print(f"{status} {name}")

    return results


def main():
    """Main function to parse arguments and run examples."""
    parser = argparse.ArgumentParser(
        description="Browser Use Agent Examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available examples:
  search       - Web search and result analysis
  form         - Form filling and submission
  data         - Data extraction from web pages
  navigation   - Multi-page navigation and information gathering
  shopping     - E-commerce browsing and comparison
  social       - Social media content analysis
  accessibility - Website accessibility testing
  api          - API testing through web interfaces

Examples:
  python examples.py --example search
  python examples.py --example form --headless
  python examples.py --all
        """
    )

    parser.add_argument(
        '--example',
        help='Specific example to run'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all examples in sequence'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available examples'
    )

    parser.add_argument(
        '--model',
        help='Override LLM model (e.g., gpt-4o, claude-3-5-sonnet-20241022)'
    )

    parser.add_argument(
        '--provider',
        choices=['openai', 'anthropic', 'google', 'groq', 'azure'],
        help='Force specific LLM provider'
    )

    args = parser.parse_args()

    # Check for API keys
    available_keys = [
        'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY',
        'GROQ_API_KEY', 'AZURE_OPENAI_API_KEY'
    ]

    if not any(os.getenv(key) for key in available_keys):
        print("❌ Error: No API key found.")
        print("Please set at least one of the following environment variables:")
        for key in available_keys:
            print(f"  {key}")
        print("\nExample:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)

    if args.list:
        print("Available examples:")
        examples_list = [
            'search', 'form', 'data', 'navigation',
            'shopping', 'social', 'accessibility', 'api'
        ]
        for example in examples_list:
            print(f"  - {example}")
        return

    if args.all:
        print("Running all examples...")
        if args.provider or args.model:
            print(f"🤖 Using provider: {args.provider or 'auto'}")
            if args.model:
                print(f"🧠 Using model: {args.model}")
        asyncio.run(run_all_examples(headless=args.headless, provider=args.provider, model=args.model))
    elif args.example:
        if args.provider or args.model:
            print(f"🤖 Using provider: {args.provider or 'auto'}")
            if args.model:
                print(f"🧠 Using model: {args.model}")
        asyncio.run(run_example(args.example, headless=args.headless, provider=args.provider, model=args.model))
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
