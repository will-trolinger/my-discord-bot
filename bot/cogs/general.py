"""General commands cog."""

import discord
from discord.ext import commands


class General(commands.Cog):
    """General utility commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the cog."""
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: {latency}ms")

    @commands.command(name="info")
    async def info(self, ctx: commands.Context) -> None:
        """Display information about the bot."""
        embed = discord.Embed(
            title="Bot Information",
            color=discord.Color.blue(),
        )

        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.add_field(name="Name", value=self.bot.user.name, inline=True)

        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(
            name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name="hello")
    @commands.guild_only()
    @commands.is_owner()
    async def hello(self, ctx: commands.Context) -> None:
        """Say hello (owner only)."""
        await ctx.send(f"Hello, {ctx.author.name}!")

    @commands.command(name="helicopter")
    @commands.guild_only()
    @commands.is_owner()
    async def helicopter(self, ctx: commands.Context) -> None:
        """Play the chopper playlist and shuffle it."""
        import asyncio

        try:
            webhooks = await ctx.channel.webhooks()
            webhook = next((w for w in webhooks if w.name == "HelicopterBot"), None)

            if not webhook:
                webhook = await ctx.channel.create_webhook(name="HelicopterBot")

            await webhook.send(
                "m!play https://music.apple.com/us/playlist/chopper/pl.u-9N9LXjLIxqEek06",
                username=ctx.author.display_name,
                avatar_url=ctx.author.display_avatar.url
            )
            await asyncio.sleep(1)
            await webhook.send(
                "m!shuffle",
                username=ctx.author.display_name,
                avatar_url=ctx.author.display_avatar.url
            )
        except discord.Forbidden:
            await ctx.send("I need the **Manage Webhooks** permission in this channel.")

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def server_info(self, ctx: commands.Context) -> None:
        """Display information about the current server."""
        if not ctx.guild:
            return

        guild = ctx.guild
        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.green(),
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(
            name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Load the General cog."""
    await bot.add_cog(General(bot))
