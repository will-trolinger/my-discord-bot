# Development Guide

## Project Structure

```
discord-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── client.py        # Bot client class
│   ├── cogs/            # Command modules
│   │   ├── __init__.py
│   │   ├── general.py   # General commands
│   │   └── scoreboard.py # Sports scoreboard
│   └── utils/           # Helper functions
│       ├── __init__.py
│       └── helpers.py
├── config/
│   ├── __init__.py
│   └── settings.py      # Configuration management
├── tests/
│   ├── __init__.py
│   └── test_helpers.py
├── .env.example         # Environment template
├── .gitignore
├── pyproject.toml       # Project configuration
├── requirements.txt
└── README.md
```

## Adding New Commands

Create a new cog in `bot/cogs/`:

```python
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send("Hello!")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Example(bot))
```

Then register it in `bot/client.py`:

```python
self.initial_extensions: list[str] = [
    "bot.cogs.general",
    "bot.cogs.example",  # Add your new cog
]
```

## Running Tests

```bash
pytest
pytest --cov=bot
```

## Code Quality

```bash
black .
ruff check .
mypy bot/
```
