# Web Database

## Purpose
Supabase PostgreSQL schema, client setup, TypeScript types, and seed data.

## Requirements

### Requirement: Schema — Core Tables
```sql
-- users_profile (extends Supabase auth.users)
users_profile (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  display_name TEXT,
  avatar_url TEXT,
  language TEXT DEFAULT 'vi',
  timezone TEXT DEFAULT 'Asia/Ho_Chi_Minh',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
)

-- articles
articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT NOT NULL,
  url TEXT,
  source TEXT,
  content TEXT,
  status TEXT DEFAULT 'new' CHECK (status IN ('new', 'analyzing', 'analyzed', 'reflected')),
  raindrop_id BIGINT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
)

-- article_analyses
article_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  persona TEXT NOT NULL CHECK (persona IN ('scout', 'builder', 'debater', 'chief')),
  content TEXT NOT NULL,
  model TEXT,
  tokens_used INTEGER,
  created_at TIMESTAMPTZ DEFAULT now()
)

-- reflections
reflections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id),
  key_insight TEXT,
  action_item TEXT,
  confidence INTEGER CHECK (confidence BETWEEN 1 AND 10),
  tags TEXT[],
  voice_used BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
)

-- tags
tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,
  color TEXT,
  UNIQUE(user_id, name)
)

-- article_tags (many-to-many)
article_tags (
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (article_id, tag_id)
)

-- user_settings
user_settings (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id),
  auth_provider TEXT DEFAULT 'supabase',
  raindrop_sync_enabled BOOLEAN DEFAULT false,
  raindrop_sync_mode TEXT DEFAULT 'whitelist',
  notification_telegram BOOLEAN DEFAULT true,
  notification_email BOOLEAN DEFAULT false,
  notification_browser BOOLEAN DEFAULT false,
  quiet_hours_enabled BOOLEAN DEFAULT false,
  quiet_hours_start TEXT DEFAULT '22:00',
  quiet_hours_end TEXT DEFAULT '07:00',
  backup_enabled BOOLEAN DEFAULT false,
  backup_frequency TEXT DEFAULT 'weekly',
  settings_json JSONB DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ DEFAULT now()
)
```

### Requirement: pgvector Extension
```sql
CREATE EXTENSION IF NOT EXISTS vector;

article_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  embedding vector(1536),
  model TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
)
```

### Requirement: Row Level Security (RLS)
- All tables: users can only read/write their own data
- Policy: `auth.uid() = user_id`
- articles, reflections, tags, user_settings, article_embeddings

### Requirement: Supabase Client
- Browser client (`src/lib/supabase/client.ts`): `createBrowserClient()`
- Server client (`src/lib/supabase/server.ts`): `createServerClient()` for RSC
- Middleware helper (`src/lib/supabase/middleware.ts`): session refresh

### Requirement: TypeScript Types
- Auto-generated via `npx supabase gen types typescript`
- Output to `src/lib/supabase/types.ts`
- Re-generate after schema changes

### Requirement: Seed Data
- Python script `supabase/seed/export-v1.py`: read V1 SQLite → export JSON
- SQL seed file `supabase/seed/seed.sql`: insert exported data into Supabase
- Includes: articles, tags, article_tags, sample analyses
- Dev-only — not deployed to production
