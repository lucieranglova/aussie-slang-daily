# aussie-slang-daily
# 🦘 Aussie Slang of the Day

A GitHub Actions bot that generates a daily Australian slang term using the Claude AI API and sends it to a Discord channel every morning.

## Example Discord message

> 🍺 **Aussie Slang of the Day**
> ### Bottle-o
> *Pronunciation: BOT-ul-oh*
>
> A liquor store or bottle shop. An essential part of Australian vocabulary and culture.
>
> **Example:** "I'm heading to the bottle-o, want anything?" [I'm going to the liquor store, want anything?]

## How it works

```
GitHub Actions cron (every day at 8:00 UTC)
        ↓
aussie_slang.py calls Claude API
        ↓
Claude generates a slang term as JSON
        ↓
Script sends a formatted message to Discord
```

## Repository structure

```
├── aussie_slang.py              # Main script
└── .github/
    └── workflows/
        └── aussie_slang.yml     # GitHub Actions cron
```

## Setup

### 1. Fork or clone this repository

### 2. Create a Discord webhook
- Open Discord → channel settings ⚙️ → Integrations → Webhooks
- Click **New Webhook** → copy the URL

### 3. Get an Anthropic API key
- Go to [console.anthropic.com](https://console.anthropic.com)
- Navigate to **API Keys → Create Key**
- Add credits in **Plans & Billing** (minimum $5, lasts several months for this use case)

### 4. Add GitHub Secrets
Go to your repository → **Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Value |
|---|---|
| `DISCORD_WEBHOOK_URL` | Your Discord webhook URL |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 5. Enable Actions write permissions
**Settings → Actions → General → Workflow permissions → Read and write permissions**

### 6. Run manually to test
**Actions → Aussie Slang of the Day → Run workflow**

## Schedule

The bot runs every day at **8:00 UTC** (= 10:00 CEST in summer).

To change the time, edit the cron expression in `.github/workflows/aussie_slang.yml`:

| Time | Cron |
|---|---|
| 8:00 UTC (default) | `0 8 * * *` |
| 7:00 UTC | `0 7 * * *` |
| 20:00 UTC | `0 20 * * *` |

## Cost

Each run makes one API call to Claude. At current Anthropic pricing, 365 calls per year costs approximately **$0.50–1.00** depending on response length — well within the $5 minimum credit.

GitHub Actions are **free** for public repositories.

## Slang categories

The bot varies between different categories each day:
- 🍺 Food & drinks
- 👋 Greetings & expressions
- 🗺️ Places & locations
- 🏄 Activities & hobbies
- 👥 People & personalities
