"""Common helper functions for the bot."""

import discord
from discord.ext import commands


def create_embed(
    title: str,
    description: str | None = None,
    color: discord.Color = discord.Color.blue(),
    **kwargs,
) -> discord.Embed:
    """Create a standardized embed with common styling.

    Args:
        title: The embed title.
        description: Optional description text.
        color: The embed color (default: blue).
        **kwargs: Additional arguments to pass to discord.Embed.

    Returns:
        A configured Discord embed object.
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        **kwargs,
    )
    return embed


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted duration string (e.g., "1h 23m 45s").
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


async def send_paginated(
    ctx: commands.Context,
    items: list[str],
    title: str,
    per_page: int = 10,
) -> None:
    """Send a paginated list of items as embeds.

    Args:
        ctx: The command context.
        items: List of string items to display.
        title: Title for the embed.
        per_page: Number of items per page.
    """
    if not items:
        await ctx.send("No items to display.")
        return

    pages = [items[i : i + per_page] for i in range(0, len(items), per_page)]

    for i, page in enumerate(pages, 1):
        embed = create_embed(
            title=f"{title} (Page {i}/{len(pages)})",
            description="\n".join(page),
        )
        await ctx.send(embed=embed)
