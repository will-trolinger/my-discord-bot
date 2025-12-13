# Discord Bot

A Discord bot built with [discord.py](https://discordpy.readthedocs.io/).

## Project Structure

```
discord-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── client.py        # Bot client class
│   ├── cogs/            # Command modules
│   │   ├── __init__.py
│   │   └── general.py   # General commands
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

## Setup

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your bot token
DISCORD_TOKEN=your_bot_token_here
```

### 3. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install with dev dependencies
pip install -e ".[dev]"
```

### 4. Invite the Bot

Generate an invite URL from the Developer Portal:
1. Go to OAuth2 > URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select bot permissions as needed
4. Use the generated URL to invite the bot

### 5. Run the Bot

```bash
# Run directly
python -m bot.main

# Or using the entry point (after pip install -e .)
bot
```

## Available Commands

- `!ping` - Check bot latency
- `!info` - Display bot information
- `!serverinfo` - Display server information
- `!help` - Show all available commands

## Adding New Commands

Create a new cog in `bot/cogs/`:

```python
# bot/cogs/example.py
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

Then add it to `bot/client.py`:

```python
self.initial_extensions: list[str] = [
    "bot.cogs.general",
    "bot.cogs.example",  # Add your new cog
]
```

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=bot

# Format code
black .

# Lint code
ruff check .

# Type check
mypy bot/
```

## License

MIT
