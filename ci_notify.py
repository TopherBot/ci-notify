#!/usr/bin/env python3
"""ci-notify: Send a Telegram message about CI job status.

Required environment variables:
  TELEGRAM_BOT_TOKEN - Bot token from BotFather
  TELEGRAM_CHAT_ID   - Numeric chat ID to receive the message
  CI_STATUS          - Job status string (e.g., "success" or "failure")
  CI_COMMIT          - Commit SHA or identifier (optional)
"""
import os
import sys
import json
import urllib.request

def get_env(name, default=None):
    val = os.getenv(name, default)
    if val is None:
        print(f"[ci-notify] Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return val

TOKEN = get_env('TELEGRAM_BOT_TOKEN')
CHAT_ID = get_env('TELEGRAM_CHAT_ID')
STATUS = get_env('CI_STATUS')
COMMIT = os.getenv('CI_COMMIT', '')

# Build message
emoji = "✅" if STATUS.lower() == 'success' else "❌"
msg = f"{emoji} CI Job {STATUS}\n"
if COMMIT:
    short = COMMIT[:7]
    msg += f"Commit: {short}\n"
msg += f"Time: {os.getenv('CI_RUN_TIME', '')}"

# Telegram API call
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    'chat_id': CHAT_ID,
    'text': msg,
    'parse_mode': 'Markdown'
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
        if not result.get('ok'):
            raise Exception(result)
        print('[ci-notify] Message sent successfully')
except Exception as e:
    print(f'[ci-notify] Failed to send message: {e}', file=sys.stderr)
    sys.exit(1)
