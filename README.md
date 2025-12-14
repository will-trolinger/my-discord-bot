# Discord Bot

A Discord bot built with [discord.py](https://discordpy.readthedocs.io/).

## Commands

### General

| Command | Description | Access |
|---------|-------------|--------|
| `!ping` | Check bot latency | Everyone |
| `!info` | Display bot information | Everyone |
| `!serverinfo` | Display server information | Everyone |
| `!hello` | Say hello | Owner only |
| `!help` | Show all available commands | Everyone |

### Scoreboard

| Command | Description | Access |
|---------|-------------|--------|
| `!scoreboard` | Get live sports scores | Requires "men" role |

**Supported leagues:** NFL, MLB, NBA, NHL, NCAAF, NCAAB, MLS, EPL

### Claude

| Command | Description | Access |
|---------|-------------|--------|
| `!claude <prompt>` | Ask Claude AI a question | Server owner only |

## Setup

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your tokens:
```
DISCORD_TOKEN=your_bot_token_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Invite the Bot

Generate an invite URL from the Developer Portal:
1. Go to OAuth2 > URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select bot permissions as needed
4. Use the generated URL to invite the bot

### 5. Run the Bot

```bash
python -m bot.main
```
