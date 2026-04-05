"""
Aussie Slang of the Day
Generates a daily Australian slang term using Claude API and sends it to Discord.
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")


def get_slang() -> dict:
    prompt = """Generate a fun Australian slang term for today. 
Return ONLY a JSON object with these exact fields, no other text:
{
  "term": "the slang word or phrase",
  "pronunciation": "how to pronounce it",
  "meaning": "what it means in 1-2 sentences",
  "example": "one example sentence using the term, with English translation in brackets",
  "emoji": "one relevant emoji"
}
Make it genuinely used in Australia, fun and interesting. Vary between different categories 
(food, greetings, places, activities, people). Never repeat common ones like arvo, barbie, g'day."""

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Anthropic error {e.code}: {e.read().decode('utf-8')}")
        raise

    text = data["content"][0]["text"].strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def send_discord(slang: dict):
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    message = (
        f"## {slang['emoji']} Aussie Slang of the Day — {today}\n\n"
        f"### {slang['term']}\n"
        f"*Pronunciation: {slang['pronunciation']}*\n\n"
        f"{slang['meaning']}\n\n"
        f"**Example:** {slang['example']}"
    )

    payload = json.dumps({
        "embeds": [{
            "title": f"{slang['emoji']} Aussie Slang of the Day",
            "description": (
                f"### {slang['term']}\n"
                f"*Pronunciation: {slang['pronunciation']}*\n\n"
                f"{slang['meaning']}\n\n"
                f"**Example:** {slang['example']}"
            ),
            "color": 16742144,  # Australian gold
            "footer": {"text": today}
        }]
    }).encode("utf-8")

    req = urllib.request.Request(
        DISCORD_WEBHOOK,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com, 1.0)",
        },
        method="POST",
    )

    try:
        urllib.request.urlopen(req, timeout=10)
        print("Discord message sent!")
    except urllib.error.HTTPError as e:
        print(f"Discord error {e.code}: {e.read().decode('utf-8')}")
        raise


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Generating Aussie slang...")

    if not ANTHROPIC_API_KEY:
        raise ValueError("Missing ANTHROPIC_API_KEY")
    if not DISCORD_WEBHOOK:
        raise ValueError("Missing DISCORD_WEBHOOK_URL")

    slang = get_slang()
    print(f"Got slang: {slang['term']} — {slang['meaning']}")

    send_discord(slang)


if __name__ == "__main__":
    main()
