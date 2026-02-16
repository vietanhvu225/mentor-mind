# Camofox Browser Setup Guide

## What is Camofox?

Camofox is a headless browser automation server built on **Camoufox** (a Firefox fork with C++ anti-detection). It bypasses bot detection on Facebook, LinkedIn, Instagram, etc.

Our extractor uses it as a **fallback** — when the standard `httpx` + OG meta approach gets blocked.

## Prerequisites

- **Node.js** 18+ (`node --version`)
- **npm** (`npm --version`)

## Installation

```bash
# Clone the repo
git clone https://github.com/jo-inc/camofox-browser
cd camofox-browser

# Install dependencies
npm install

# Start server (downloads Camoufox ~300MB on first run)
npm start
```

Server runs on `http://localhost:9377` by default.

## Verify

```bash
# Health check
curl http://localhost:9377/health
```

## Environment Variables

Add to your `.env` (optional — defaults work fine):

```env
CAMOFOX_URL=http://localhost:9377
CAMOFOX_USER_ID=learning-bot
```

## Cookie Import (Optional — Facebook Login)

To access full Facebook content (comments, full post text):

1. Install browser extension: **"cookies.txt"** (Chrome/Firefox)
2. Export cookies for `facebook.com` in Netscape format
3. Place cookie file:
   ```bash
   mkdir -p ~/.camofox/cookies
   cp ~/Downloads/facebook_cookies.txt ~/.camofox/cookies/facebook.txt
   ```
4. Set API key:
   ```bash
   export CAMOFOX_API_KEY="your-secret-key"
   ```

## How It Works in Our Pipeline

```
URL → is walled garden? (Facebook/LinkedIn/Instagram)
  ↓ yes
  → Try Camofox (full page render + screenshot + links)
  ↓ Camofox not running?
  → Fallback to OG meta tags (httpx, limited content)
  ↓ no walled garden
  → Standard extraction (trafilatura → Jina Reader)
```

**Graceful degradation**: If Camofox server is not running, the bot works exactly as before using OG meta tags.

## Docker (Production)

```bash
docker build -t camofox-browser .
docker run -p 9377:9377 camofox-browser
```
