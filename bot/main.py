"""Main entry point for the Discord bot."""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

from bot.client import Bot

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the bot."""
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        logger.error("DISCORD_TOKEN environment variable is not set!")
        logger.error("Please create a .env file with your bot token.")
        sys.exit(1)

    bot = Bot()

    try:
        logger.info("Starting bot...")
        asyncio.run(bot.start(token))
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.exception(f"Bot crashed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
