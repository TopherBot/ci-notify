# ci-notify

**Instant Telegram alerts for CI pipelines**

## What it does
- Reads `CI_STATUS` (e.g., `success` or `failure`) and `CI_COMMIT` from the environment.
- Sends a formatted message to a Telegram chat via Bot API.
- No dependencies other than `requests` (included in the standard library for many CI images).

## Quick start
1. Create a Telegram bot with [BotFather](https://t.me/botfather) and obtain a **Bot Token**.
2. Get your **Chat ID** (send `/start` to the bot, then use `https://api.telegram.org/bot<token>/getUpdates`).
3. Add the following environment variables to your CI configuration:
   ```bash
   export TELEGRAM_BOT_TOKEN="<your-bot-token>"
   export TELEGRAM_CHAT_ID="<your-chat-id>"
   export CI_STATUS="${{ job.status }}"   # GitHub Actions example
   export CI_COMMIT="${{ github.sha }}"
   ```
4. Add a step to run the script after the job finishes.

## Example (GitHub Actions)
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: echo "building..."
      - name: Notify Telegram
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          CI_STATUS: ${{ job.status }}
          CI_COMMIT: ${{ github.sha }}
        run: python3 ci_notify.py
```