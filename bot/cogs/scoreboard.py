"""Scoreboard commands cog for fetching sports scores."""

import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

import aiohttp
import discord
from discord.ext import commands


SPORTS = {
    "1": {"name": "NFL", "sport": "football", "league": "nfl"},
    "2": {"name": "MLB", "sport": "baseball", "league": "mlb"},
    "3": {"name": "NBA", "sport": "basketball", "league": "nba"},
    "4": {"name": "NHL", "sport": "hockey", "league": "nhl"},
    "5": {"name": "NCAAF", "sport": "football", "league": "college-football"},
    "6": {"name": "NCAAB", "sport": "basketball", "league": "mens-college-basketball"},
    "7": {"name": "MLS", "sport": "soccer", "league": "usa.1"},
    "8": {"name": "EPL", "sport": "soccer", "league": "eng.1"},
}


class Scoreboard(commands.Cog):
    """Sports scoreboard commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the cog."""
        self.bot = bot

    async def fetch_scores(self, sport: str, league: str) -> dict | None:
        """Fetch scores from ESPN API."""
        url = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception:
            return None

    def get_game_status(self, competition: dict, event_date: str | None) -> str:
        """Extract game status from competition data."""
        status = competition.get("status", {})
        status_type = status.get("type", {})
        state = status_type.get("state", "")

        if state == "pre":
            detail = status_type.get("shortDetail", "")
            return detail if detail else "Scheduled"
        elif state == "in":
            detail = status_type.get("shortDetail", "")
            return detail if detail else "In Progress"
        elif state == "post":
            if event_date:
                try:
                    us_tz = ZoneInfo("America/New_York")
                    utc_dt = datetime.fromisoformat(event_date.replace("Z", "+00:00"))
                    local_dt = utc_dt.astimezone(us_tz)
                    date_str = local_dt.strftime("%m/%d %I:%M %p")
                    return f"Final - {date_str}"
                except Exception:
                    pass
            return "Final"

        return status_type.get("shortDetail", "Unknown")

    def format_game_links(self, event: dict) -> str:
        """Format game links as Discord hyperlinks."""
        links = event.get("links", [])
        if not links:
            return ""

        link_texts = []
        for link in links:
            text = link.get("shortText", link.get("text", ""))
            href = link.get("href", "")
            if text and href:
                link_texts.append(f"[{text}](<{href}>)")

        return " | ".join(link_texts)

    def format_scores(self, data: dict, sport_name: str) -> list[str]:
        """Format scores into messages for Discord."""
        us_tz = ZoneInfo("America/New_York")
        today = datetime.now(us_tz).strftime("%A, %B %d, %Y")

        events = data.get("events", [])

        if not events:
            return [f"**{sport_name} Scoreboard - {today}**\n\nNo games scheduled today."]

        messages = []
        messages.append(f"**{sport_name} Scoreboard - {today}**")

        for event in events:
            competitions = event.get("competitions", [])
            if not competitions:
                continue

            competition = competitions[0]
            competitors = competition.get("competitors", [])

            if len(competitors) < 2:
                continue

            away_team = None
            home_team = None

            for team in competitors:
                if team.get("homeAway") == "away":
                    away_team = team
                else:
                    home_team = team

            if not away_team or not home_team:
                continue

            away_name = away_team.get("team", {}).get("abbreviation", "???")
            away_score = away_team.get("score", "-")
            home_name = home_team.get("team", {}).get("abbreviation", "???")
            home_score = home_team.get("score", "-")

            event_date = event.get("date")
            status = self.get_game_status(competition, event_date)
            game_links = self.format_game_links(event)

            game_msg = f"```{away_name:>6}  {away_score:>3}\n{home_name:>6}  {home_score:>3}\n        {status}```\n{game_links}"
            messages.append(game_msg)

        return messages

    @commands.command(name="scoreboard")
    @commands.has_role("men")
    async def scoreboard(self, ctx: commands.Context) -> None:
        """Get live sports scores."""
        options_text = "**What sport?**\n"
        for num, sport in SPORTS.items():
            options_text += f"{num}. {sport['name']}\n"

        await ctx.send(options_text)

        def check(msg: discord.Message) -> bool:
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.strip() in SPORTS
            )

        try:
            response = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Scoreboard selection timed out.")
            return

        selection = response.content.strip()
        sport_info = SPORTS[selection]

        async with ctx.typing():
            data = await self.fetch_scores(sport_info["sport"], sport_info["league"])

        if not data:
            await ctx.send(f"Failed to fetch {sport_info['name']} scores. Please try again later.")
            return

        messages = self.format_scores(data, sport_info["name"])
        await asyncio.gather(*[ctx.send(msg) for msg in messages])


async def setup(bot: commands.Bot) -> None:
    """Load the Scoreboard cog."""
    await bot.add_cog(Scoreboard(bot))
