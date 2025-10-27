## Table of Contents
- [Table of Contents](#table-of-contents)
- [Routes](#routes)
  - [`GET /api/v1/health`](#get-apiv1health)
  - [`POST /api/v1/replays/scrape`](#post-apiv1replaysscrape)
  - [`GET /api/v1/replays/{replay_id}`](#get-apiv1replaysreplay_id)
  - [`GET /api/v1/replays`](#get-apiv1replays)
- [Performance \& Caveats](#performance--caveats)
  - [Scraping Performance](#scraping-performance)
  - [Caching](#caching)
  - [Rate Limiting](#rate-limiting)


## Routes

### `GET /api/v1/health`

Health check endpoint.

**Auth**: None

**Response**:
```json
{
  "status": "ok"
}
```

---

### `POST /api/v1/replays/scrape`

Scrape DuelingBook replay data. Bypasses captcha via Anti-Captcha.

**Auth**: Required (`x-api-key` header)

**Request**:
```json
{
  "replay_url": "https://www.duelingbook.com/replay?id=123456"
}
```

**Response**:
```json
{
  "conceal": false,
  "date": "2024-01-01",
  "plays": [...]
}
```

**Errors**:
- `422` - Invalid URL format, domain, or replay ID
- `401` - Invalid/missing API key
- `429` - Rate limit exceeded
- `500` - Captcha solving or scraping failure

---

### `GET /api/v1/replays/{replay_id}`

Fetch cached replay data by ID.

**Auth**: Required (`x-api-key` header)

**Response**:
```json
{
  "conceal": false,
  "date": "2024-01-01",
  "plays": [...]
}
```

**Errors**:
- `404` - Replay not found in cache
- `401` - Invalid/missing API key

---

### `GET /api/v1/replays`

List cached replay IDs with pagination.

**Auth**: Required (`x-api-key` header)

**Query Params**:
- `page_size` (default: 1000, max: 1000)
- `after` - Cursor for next page (replay ID)

**Response**:
```json
{
  "data": ["123456", "123457", ...],
  "pagination": {
    "page_size": 1000,
    "next_cursor": "123999",
    "has_more": true
  }
}
```

---

## Performance & Caveats

### Scraping Performance

- **~10 seconds per scrape** - Light wrapper over Anti-Captcha
- **High error rate at high rate limits** - Anti-Captcha limitations apply
- **No retry logic** - Handle retries and batching client-side

### Caching

- Scraped replays automatically cached to S3
- Subsequent requests for same replay ID return instantly from cache
- Use `GET /api/v1/replays/{replay_id}` to fetch cached data without scraping

### Rate Limiting

Default: In-memory 200 requests/minute per IP
