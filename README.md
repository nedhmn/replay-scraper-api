# Replay Scraper API

FastAPI service for scraping DuelingBook replay data. Built for personal use.

## Features

- **POST `/api/v1/replays/scrape`**: Scrape DuelingBook replays, bypass captcha with [Anti-Captcha](https://anti-captcha.com/)
- **S3 caching**: Stores scraped replays to avoid re-scraping
- **API key auth**: Single key authentication for trusted users

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- AWS S3 bucket
- [Anti-Captcha](https://anti-captcha.com/) account with API key
- DuelingBook site key for captcha solving

## Setup

1. **Clone and install dependencies**
   ```bash
   git clone <repo-url>
   cd replay-scraper-api
   uv sync
   ```

2. **Generate API key**
   ```bash
   uv run python scripts/generate_api_key.py
   ```
   Copy the `API_KEY` (share with users) and `API_KEY_HASH` (for `.env`)

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Fill in:
   - `ANTICAPTCHA_API_KEY` - Your [Anti-Captcha](https://anti-captcha.com/) API key
   - `SITE_KEY` - DuelingBook captcha site key
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET_NAME` - AWS credentials
   - `API_KEY_HASH` - Hash from step 2

4. **Run locally**
   ```bash
   uv run fastapi dev app/main.py
   ```
   API docs available at `http://localhost:8000/docs`

## Usage

```bash
curl -X POST http://localhost:8000/api/v1/replays/scrape \
  -H "x-api-key: api_..." \
  -H "Content-Type: application/json" \
  -d '{"replay_url": "https://www.duelingbook.com/replay?id=123456"}'
```