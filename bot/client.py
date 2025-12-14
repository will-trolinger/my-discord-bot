"""Discord bot client definition."""

import logging
import os
from pathlib import Path

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    """Custom Discord bot class with additional functionality."""

    def __init__(self) -> None:
        """Initialize the bot with default intents and settings."""
        # Configure intents - adjust based on your bot's needs
        intents = discord.Intents.default()
        intents.message_content = True  # Required for reading message content
        intents.members = True  # Required for member-related events

        # Get command prefix from environment or use default
        prefix = os.getenv("COMMAND_PREFIX", "!")

        super().__init__(
            command_prefix=prefix,
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
        )

        self.initial_extensions: list[str] = [
            "bot.cogs.general",
            "bot.cogs.scoreboard",
        ]

    async def setup_hook(self) -> None:
        """Called when the bot is starting up."""
        # Load all cogs
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")

    async def on_ready(self) -> None:
        """Called when the bot is ready and connected."""
        if self.user:
            logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
            logger.info(f"Connected to {len(self.guilds)} guild(s)")
            logger.info("------")

            # Set bot presence/status
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers"
            )
            await self.change_presence(activity=activity)

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: `{error.param.name}`")
            return

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
            return

        if isinstance(error, commands.MissingRole):
            await ctx.send(f"You need the **{error.missing_role}** role to use this command.")
            return

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have permission to do that.")
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.1f}s"
            )
            return

        # Log unexpected errors
        logger.error(f"Unexpected error in command {ctx.command}: {error}")
        await ctx.send("An unexpected error occurred. Please try again later.")
