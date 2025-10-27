## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Local Environment](#local-environment)
  - [Setup](#setup)
  - [Run](#run)
- [Production Environment](#production-environment)
  - [Generate API Key](#generate-api-key)
  - [Configure](#configure)
  - [Run](#run-1)


## Prerequisites

- Docker + Docker Compose
- AWS S3 bucket + credentials
- [Anti-Captcha](https://anti-captcha.com/) account + API key
- DuelingBook site key (inspect clientside code, usually in captcha init)


## Local Environment

### Setup

```bash
cp .env.example .env
```

Fill required vars:
- `ENVIRONMENT=local`
- `ANTICAPTCHA_API_KEY`
- `SITE_KEY`
- `AWS_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET_NAME`

### Run

```bash
docker compose up -d --build
```

API docs: `http://localhost:8000/docs`

> [!NOTE]
> Auth bypassed in local mode. Use any dummy value for `x-api-key` header.


## Production Environment

### Generate API Key

```bash
docker compose run --rm replay-scraper-api python scripts/generate_api_key.py
```

Copy output:
- `API_KEY` - share with users
- `API_KEY_HASH` - for `.env`

### Configure

Update `.env`:
- `ENVIRONMENT=production`
- `API_KEY_HASH=<generated_hash>`

### Run

```bash
docker compose up --build
```

Auth required. Use generated `API_KEY` in `x-api-key` header.
