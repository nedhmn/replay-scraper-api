## Table of Contents

- [Table of Contents](#table-of-contents)
- [Deployment](#deployment)
- [Railway Setup](#railway-setup)
  - [Create Project \& Service](#create-project--service)
  - [Configure Environment Variables](#configure-environment-variables)
  - [Make Service Public](#make-service-public)
  - [Optional Settings](#optional-settings)
- [GitHub Setup](#github-setup)
  - [Add Railway Token](#add-railway-token)
  - [Deploy](#deploy)
- [Monitor](#monitor)


## Deployment

Railway deployment via GitHub Actions.

## Railway Setup

### Create Project & Service

1. Go to [Railway](https://railway.com)
2. Create new project
3. Create empty service named `replay-scraper-api`

> [!NOTE]
> Service name must match `--service` in [deploy-railway.yml](.github/workflows/deploy-railway.yml)

### Configure Environment Variables

In service settings, add all vars from `.env`:

```
ENVIRONMENT=production
ANTICAPTCHA_API_KEY=<your_key>
SITE_KEY=<your_key>
AWS_REGION=<your_region>
AWS_ACCESS_KEY_ID=<your_key>
AWS_SECRET_ACCESS_KEY=<your_key>
S3_BUCKET_NAME=<your_bucket>
API_KEY_HASH=<generated_hash>
```

> [!IMPORTANT]
> Generate production API key first (see [01-environments.md](./01-environments.md))

### Make Service Public

Service Settings → Networking → Generate Domain

### Optional Settings

Service Settings:
- **Health Check**: `/api/v1/health`
- **Custom Domain**: Configure if needed
- **Scale to Zero**: Enable for cost savings

## GitHub Setup

### Add Railway Token

1. Railway Project Settings → Generate Project Token
2. GitHub Repo → Settings → Secrets → Add `RAILWAY_TOKEN`

### Deploy

Push to `main` branch or trigger manually.

GitHub Actions:
1. Lints & type checks
2. Deploys to Railway via `railway up`

## Monitor

Railway dashboard:
- **Deployments** - build logs, status
- **Metrics** - CPU, memory, requests
- **Logs** - application logs
