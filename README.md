# Replay Scraper API

FastAPI service for scraping DuelingBook replay data with captcha bypass.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Quick Start](#quick-start)
   - [Prerequisites](#prerequisites)
   - [Local Setup](#local-setup)
   - [Example Request](#example-request)
- [Documentation](#documentation)
- [Performance](#performance)


## Features

- Scrape DuelingBook replays via [Anti-Captcha](https://anti-captcha.com/)
- S3 caching to avoid re-scraping
- (Single) API key authentication 
- Rate limiting (200 req/min)

## Quick Start

### Prerequisites

- Docker + Docker Compose
- AWS S3 bucket + credentials
- [Anti-Captcha](https://anti-captcha.com/) API key
- DuelingBook site key

### Local Setup

```bash
cp .env.example .env
# Fill in required vars (see docs/01-environments.md)

docker compose up -d --build
```

API docs: `http://localhost:8000/docs`

> [!NOTE]
> Auth bypassed in local mode. Use any dummy `x-api-key` value.

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/replays/scrape \
  -H "x-api-key: dummy" \
  -H "Content-Type: application/json" \
  -d '{"replay_url": "https://www.duelingbook.com/replay?id=123456"}'
```

## Documentation

- **[Environments](docs/01-environments.md)** - Local & production setup
- **[Deployment](docs/02-deployment.md)** - Railway deployment via GitHub Actions
- **[Usage](docs/03-usage.md)** - API routes & examples

## Performance

- ~10 seconds per scrape
- High error rate at high request volumes (Anti-Captcha limitations)
- Cached replays return instantly
