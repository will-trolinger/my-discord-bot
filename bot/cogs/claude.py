"""Claude AI command cog."""

import os

import anthropic
from discord.ext import commands


def is_guild_owner():
    """Check if the command invoker is the guild owner."""

    async def predicate(ctx: commands.Context) -> bool:
        if not ctx.guild:
            return False
        return ctx.author.id == ctx.guild.owner_id

    return commands.check(predicate)


class Claude(commands.Cog):
    """Claude AI commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the cog."""
        self.bot = bot
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
        self.model = os.getenv("ANTHROPIC_MODEL")

    @commands.command(name="claude")
    @commands.guild_only()
    @is_guild_owner()
    async def claude(self, ctx: commands.Context, *, prompt: str) -> None:
        """Ask Claude a question (server owner only)."""
        if not self.client:
            await ctx.send("Anthropic API key is not configured.")
            return

        async with ctx.typing():
            try:
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": f"{prompt}\n\nBe conversational but professional. No titles or headers.",
                        }
                    ],
                )

                response_text = message.content[0].text

                if len(response_text) > 2000:
                    response_text = response_text[:1997] + "..."

                await ctx.send(response_text)

            except anthropic.APIError as e:
                await ctx.send(f"API error: {e.message}")


async def setup(bot: commands.Bot) -> None:
    """Load the Claude cog."""
    await bot.add_cog(Claude(bot))
