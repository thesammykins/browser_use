#!/usr/bin/env python3
"""
Browser Use Agent - A flexible browser automation agent that can navigate to any website
and perform specified tasks using AI.

Usage:
    python browser_agent.py --url "https://example.com" --task "Fill out the contact form"
    python browser_agent.py --url "https://google.com" --task "Search for 'browser automation'" --headless
"""

import asyncio
import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Import browser-use components
try:
    from browser_use import Agent, BrowserSession, BrowserProfile
    from browser_use.llm import ChatOpenAI, ChatAnthropic, ChatGoogle, ChatGroq, ChatAzureOpenAI
except ImportError as e:
    print(f"Error: browser-use package not found. Please install it first:")
    print("pip install browser-use")
    print(f"Import error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('browser_agent.log')
    ]
)
logger = logging.getLogger(__name__)


class BrowserAgent:
    """
    A flexible browser automation agent that can navigate to websites and perform tasks.
    """

    def __init__(
        self,
        headless: bool = False,
        viewport_width: int = 1280,
        viewport_height: int = 1024,
        user_data_dir: Optional[str] = None,
        storage_state: Optional[str] = None
    ):
        """
        Initialize the BrowserAgent.

        Args:
            headless: Whether to run browser in headless mode
            viewport_width: Browser viewport width
            viewport_height: Browser viewport height
            user_data_dir: Directory for browser user data
            storage_state: Path to storage state file for cookies/auth
        """
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.user_data_dir = user_data_dir
        self.storage_state = storage_state
        self.llm = None
        self.browser_session = None

    def setup_llm(self) -> None:
        """Setup the Language Model for the agent based on environment configuration."""
        # Check for preferred provider
        preferred_provider = os.getenv('BROWSER_USE_PREFERRED_PROVIDER', '').lower()

        # Provider configurations with default models
        provider_configs = {
            'openai': {
                'api_key': 'OPENAI_API_KEY',
                'model_env': 'BROWSER_USE_OPENAI_MODEL',
                'default_model': 'gpt-4o',
                'class': ChatOpenAI,
                'name': 'OpenAI'
            },
            'anthropic': {
                'api_key': 'ANTHROPIC_API_KEY',
                'model_env': 'BROWSER_USE_ANTHROPIC_MODEL',
                'default_model': 'claude-3-5-sonnet-20241022',
                'class': ChatAnthropic,
                'name': 'Anthropic'
            },
            'google': {
                'api_key': 'GOOGLE_API_KEY',
                'model_env': 'BROWSER_USE_GOOGLE_MODEL',
                'default_model': 'gemini-2.0-flash-exp',
                'class': ChatGoogle,
                'name': 'Google'
            },
            'groq': {
                'api_key': 'GROQ_API_KEY',
                'model_env': 'BROWSER_USE_GROQ_MODEL',
                'default_model': 'llama-3.3-70b-versatile',
                'class': ChatGroq,
                'name': 'Groq'
            },
            'azure': {
                'api_key': 'AZURE_OPENAI_API_KEY',
                'model_env': 'BROWSER_USE_AZURE_MODEL',
                'default_model': 'gpt-4o',
                'class': ChatAzureOpenAI,
                'name': 'Azure OpenAI'
            }
        }

        # Try preferred provider first if specified and available
        if preferred_provider and preferred_provider in provider_configs:
            if self._try_setup_provider(preferred_provider, provider_configs[preferred_provider]):
                return

        # Try providers in priority order
        priority_order = ['openai', 'anthropic', 'google', 'groq', 'azure']

        for provider in priority_order:
            if provider != preferred_provider:  # Skip if already tried as preferred
                if self._try_setup_provider(provider, provider_configs[provider]):
                    return

        # No valid provider found
        available_providers = [p for p, config in provider_configs.items()
                             if os.getenv(config['api_key'])]

        if available_providers:
            raise ValueError(
                f"API keys found for {available_providers} but failed to initialize LLM. "
                "Please check your API keys and model configurations."
            )
        else:
            raise ValueError(
                "No API key found. Please set at least one of: OPENAI_API_KEY, "
                "ANTHROPIC_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, or AZURE_OPENAI_API_KEY"
            )

    def _try_setup_provider(self, provider: str, config: Dict[str, Any]) -> bool:
        """Try to setup a specific LLM provider."""
        api_key = os.getenv(config['api_key'])
        if not api_key:
            return False

        try:
            # Get model from environment or use default
            model = os.getenv(config['model_env'], config['default_model'])

            # Special handling for Azure OpenAI
            if provider == 'azure':
                endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
                if not endpoint:
                    logger.warning("AZURE_OPENAI_ENDPOINT not set, skipping Azure provider")
                    return False
                self.llm = config['class'](model=model)
            else:
                # Standard initialization
                self.llm = config['class'](model=model)

            logger.info(f"Using {config['name']} with model: {model}")
            return True

        except Exception as e:
            logger.warning(f"Failed to initialize {config['name']}: {e}")
            return False

    def create_browser_profile(self) -> BrowserProfile:
        """Create a browser profile with the specified configuration."""
        profile_config = {
            'headless': self.headless,
            'viewport': {
                'width': self.viewport_width,
                'height': self.viewport_height
            },
            'highlight_elements': True,
            'use_vision': True,
            'wait_for_network_idle_page_load_time': 3.0,
        }

        # Add user data directory if specified
        if self.user_data_dir:
            profile_config['user_data_dir'] = self.user_data_dir

        # Add storage state if specified
        if self.storage_state and Path(self.storage_state).exists():
            profile_config['storage_state'] = self.storage_state

        return BrowserProfile(**profile_config)

    async def run_task(self, url: str, task: str) -> dict:
        """
        Execute the specified task on the given URL.

        Args:
            url: The website URL to navigate to
            task: The task description for the AI agent

        Returns:
            Dictionary containing the execution history and results
        """
        try:
            # Setup LLM
            self.setup_llm()

            # Create browser profile and session
            browser_profile = self.create_browser_profile()
            self.browser_session = BrowserSession(browser_profile=browser_profile)

            # Create enhanced task description
            enhanced_task = f"""
            Navigate to {url} and then {task}

            Please be thorough and methodical in your approach:
            1. First, navigate to the specified URL
            2. Wait for the page to fully load
            3. Analyze the page content and structure
            4. Execute the requested task step by step
            5. Provide clear feedback on what actions were performed

            If you encounter any errors or unexpected behavior, please describe what happened
            and attempt alternative approaches if possible.
            """

            # Create and run agent
            logger.info(f"Starting task: {task}")
            logger.info(f"Target URL: {url}")

            agent = Agent(
                task=enhanced_task,
                llm=self.llm,
                browser_session=self.browser_session,
                use_vision=True,
                max_actions_per_step=10,
                max_failures=3
            )

            # Execute the task
            history = await agent.run()

            logger.info("Task completed successfully")

            return {
                'success': True,
                'history': history.history,
                'final_url': await self.get_current_url(),
                'message': 'Task completed successfully'
            }

        except Exception as e:
            error_msg = f"Error executing task: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'message': 'Task failed to complete'
            }

        finally:
            # Clean up browser session
            if self.browser_session:
                try:
                    await self.browser_session.close()
                except Exception as e:
                    logger.warning(f"Error closing browser session: {e}")

    async def get_current_url(self) -> Optional[str]:
        """Get the current URL from the browser session."""
        try:
            if self.browser_session:
                page = await self.browser_session.get_current_page()
                return page.url
        except Exception as e:
            logger.warning(f"Could not get current URL: {e}")
        return None


async def main():
    """Main function to parse arguments and run the browser agent."""
    parser = argparse.ArgumentParser(
        description="Browser Use Agent - AI-powered browser automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python browser_agent.py --url "https://google.com" --task "Search for 'browser automation'"
  python browser_agent.py --url "https://example.com" --task "Fill out contact form" --headless
  python browser_agent.py --url "https://news.ycombinator.com" --task "Find the top 3 articles"
        """
    )

    parser.add_argument(
        '--url',
        required=True,
        help='Target website URL to navigate to'
    )

    parser.add_argument(
        '--task',
        required=True,
        help='Task description for the AI agent to perform'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no GUI)'
    )

    parser.add_argument(
        '--viewport-width',
        type=int,
        default=1280,
        help='Browser viewport width (default: 1280)'
    )

    parser.add_argument(
        '--viewport-height',
        type=int,
        default=1024,
        help='Browser viewport height (default: 1024)'
    )

    parser.add_argument(
        '--user-data-dir',
        help='Directory for browser user data (for persistent sessions)'
    )

    parser.add_argument(
        '--storage-state',
        help='Path to storage state file (for saved cookies/authentication)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
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

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Override provider and model from command line if specified
    if args.provider:
        os.environ['BROWSER_USE_PREFERRED_PROVIDER'] = args.provider

    if args.model:
        # Set model for the preferred provider
        preferred = args.provider or os.getenv('BROWSER_USE_PREFERRED_PROVIDER', 'openai')
        model_env_map = {
            'openai': 'BROWSER_USE_OPENAI_MODEL',
            'anthropic': 'BROWSER_USE_ANTHROPIC_MODEL',
            'google': 'BROWSER_USE_GOOGLE_MODEL',
            'groq': 'BROWSER_USE_GROQ_MODEL',
            'azure': 'BROWSER_USE_AZURE_MODEL'
        }
        if preferred in model_env_map:
            os.environ[model_env_map[preferred]] = args.model

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"Error: URL must start with http:// or https://")
        sys.exit(1)

    # Check for API keys
    available_keys = [
        'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY',
        'GROQ_API_KEY', 'AZURE_OPENAI_API_KEY'
    ]

    if not any(os.getenv(key) for key in available_keys):
        print("Error: No API key found.")
        print("Please set at least one of the following environment variables:")
        for key in available_keys:
            print(f"  {key}")
        print("\nExample:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("# or")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nYou can also specify preferred provider and model:")
        print("export BROWSER_USE_PREFERRED_PROVIDER=openai")
        print("export BROWSER_USE_OPENAI_MODEL=gpt-4o-mini")
        sys.exit(1)

    # Create and run browser agent
    agent = BrowserAgent(
        headless=args.headless,
        viewport_width=args.viewport_width,
        viewport_height=args.viewport_height,
        user_data_dir=args.user_data_dir,
        storage_state=args.storage_state
    )

    print(f"🚀 Starting Browser Agent...")
    print(f"📍 Target URL: {args.url}")
    print(f"📋 Task: {args.task}")
    print(f"🖥️  Headless mode: {args.headless}")
    print(f"📐 Viewport: {args.viewport_width}x{args.viewport_height}")
    if args.provider:
        print(f"🤖 Forced provider: {args.provider}")
    if args.model:
        print(f"🧠 Model override: {args.model}")
    print("-" * 60)

    # Run the task
    result = await agent.run_task(args.url, args.task)

    print("-" * 60)
    if result['success']:
        print("✅ Task completed successfully!")
        if 'final_url' in result and result['final_url']:
            print(f"🔗 Final URL: {result['final_url']}")
    else:
        print("❌ Task failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")

    # Print history summary if available
    if 'history' in result and result['history']:
        print(f"\n📊 Actions performed: {len(result['history'])}")
        print("📝 Check browser_agent.log for detailed execution log")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Task interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
